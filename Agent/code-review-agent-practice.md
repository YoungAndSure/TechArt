# 推荐排序策略服务 Agent 实践分享：Code Review

## 前言

本文中 **codeagent** 指具备工具调用能力的 AI 编程助手，如 Claude Code、OpenCode 等。

说到 Agent 落地，我认为首先不是问"模型强不强"，而是先问两个问题：

- **我们要让 Agent 干什么？**
- **Agent 能干什么？**

前者需要从需求出发分析，后者需要在不断用 Agent 解决问题过程中完善能力。

---

## 一、需求背景

推荐排序策略服务团队负责推荐系统稳定性、架构迭代和指标提升等方方面面。推荐排序策略服务的特点是**迭代人数多、迭代强度高、服务规模大**。

从日常任务形态看，可以分为两类：

| 类型 | 描述 | 例子 |
|------|------|------|
| **响应式任务** | 外部已给出明确触发，Agent 补全上下文、理解问题并给出判断或建议 | Code Review、故障分析 |
| **探索式任务** | 无明确触发，需要 Agent 主动寻找系统中的优化空间 | 自动调参、代码清理 |

本文聚焦 **Code Review** 场景。

---

## 二、Code Review 实践

### 2.1 背景与痛点

推荐排序策略服务 Code Review 强度很大：

- **Reviewer 与提交者比例**：6 人对接 150+ 算法工程师，平均每人对接 20+ 个业务方
- **Commit 频率**：单日峰值 54 个提交，P75 达 33 个提交

过去的智能 CR 尝试（如arxiv:2505.17928）存在明显局限：模型所需信息被动整理好再输入，信息量受提示词整理环节的限制。模型只能"看"输入给它的内容，无法主动探索。

### 2.2 为什么用 Agent 重做 Code Review

| 对比维度 | 纯 LLM（提示词驱动） | Agent（工具调用驱动） |
|----------|----------------------|----------------------|
| 信息选择决策权 | 在人 | 在模型 |
| 信息获取方式 | 完全依赖人工输入 | 通过 tool list 不断补足 |
| 处理方式 | 全量代码 diff 和规则一次性输入，需对超长文本做 attention | 边搜边看，更"专注" |
| 效果上限 | 由模型效果和提示词信息量决定 | 随模型能力增强而增强，无需人工改动代码 |

Agent 打破了 LLM 被动输入信息的局限——LLM 是大脑，内化了知识；Agent 给 LLM 装上了手脚，让它能主动获取信息、调用工具。

### 2.3 方案演进

#### 初版方案：全量规则串行 Review

```
MR 触发 → codeagent（加载全量评审规则）→ 逐条检查 → 输出结果
```

评审规则直接放在仓库里（`agents/` 目录下 Markdown 文件），增删规则无需改代码，合入即生效。这解决了经验同步问题：过去 review 中发现的问题需要反复通知其他 reviewer，现在只需把经验转化为提示词并通过几个 case 验证，就能自动同步给所有 reviewer。

**问题**：

- CR 只改了代码库的一部分，但需过全量规则（如精排代码改动也要过预排规则）
- 整个 review 在单次 session 上下文中完成，context 越来越长，注意力越来越分散

#### 最终方案：按模块拆分，多 Agent 并行

核心改进：

1. **规则分层拆分**：按文件类型（filetype，如 cpp）和业务模块（module，如 ranking、prerank、retrieval）划分规则
2. **多 Agent 并行**：每个规则集对应独立 Agent 进程，通过 `router_rules.json` 路由，并发执行（最大 5 个）
3. **全量代码上下文**：每个 Agent 获取全量代码 diff，防止断章取义

```
MR 触发
    │
    ▼
service.py（编排层）
    │ git diff 获取变更文件
    │ router_rules.json 三层路由（global → filetype → module）
    ▼
多 Agent 并行审查（ThreadPoolExecutor，最大 5 并发）
    │ global Agent（security / performance）
    │ filetype Agent（cpp / python）
    │ module Agent（ranking / prerank / retrieval / ab / merchant）
    ▼
汇总结果 → 生成 HTML 报告
    │
    ▼
上传至 CR 平台 → 一键创建 CR 单
```

**执行流程**：

1. `service.py` 通过 `git diff` 获取变更文件列表
2. 读取 `router_rules.json`，按三层规则分类文件
3. 对每个命中的 Agent，启动独立 codeagent 进程执行审查（最大 5 并发）
4. 每个 Agent 运行时获取**全量**代码 diff，对照自己层级的规则输出审查结果
5. 汇总所有 Agent 结果，生成 HTML 报告上传至 CR 平台

### 2.4 流水线集成与使用流程

智能 CR 流水线与 MR 联动，完整使用流程如下：

```
提交 MR
    │
    ▼
智能 CodeReview 流水线自动触发
    │
    ▼
点击流水线【报告】-【智能评审报告】
    │
    ▼
进入 CR 平台查看智能评审报告
    │
    ├── 有问题 → 参考报告自行修复 → 提交代码 → 再次触发智能 CR
    │
    └── 无问题/已修复 → 点击右上角【创建 CR 单】→ 填写业务方向（选推荐排序策略服务）→ 确定
    │
    ▼
审核人收到 CR 单 → 审阅评论 → 提交者解决评论 → 点击【通知审核人评论已解决】
    │
    ▼
审核人点击通过 → CR 单通过审核
```

**关键步骤说明**：

1. **MR 创建/更新时自动触发**智能 CR 流水线，也支持单分支手动触发
2. 智能评审报告以 HTML 形式上传至 CR 平台，可查看每个 Agent 的审查结果
3. 若一个 MR 多次触发流水线，请从**最新一次**的智能评审报告处提单
4. 业务方向暂未细分，选择【推荐排序策略服务】即可
5. 审核人完成评论后，IM 会收到提示消息；解决评论后需点击【通知审核人评论已解决】通知审核人

### 2.5 关键设计决策

#### 1. 脚本驱动，减少模型决策

设计原则：**能用脚本尽量别用模型做决策**。

- `service.py` 承担所有编排逻辑：获取 diff、路由分类、并发启动子进程、收集汇总结果
- 模型只负责"看代码、对照规则、输出问题"
- 执行失败时实现 3 次自动重试，每次打印详细的 stdout/stderr 和退出码

**并行执行模型**：使用 `ThreadPoolExecutor`，最大 5 个 worker 并发执行 Agent 审查任务。每个 Agent 是独立的 codeagent 进程，通过 `codeagent -q` 调用，传入 prompt 后等待 stdout 输出。

**输出格式支持**：summary（摘要文本）、json、html、both，按需生成。

#### 2. 分层 Agent 配置体系

路由配置为三层结构 `global` → `filetype` → `module`：

```json
{
  "global": ["security", "performance"],
  "filetype": {
    "cpp": {"patterns": ["*.h", "*.cpp", "*.cc"]},
    "python": {"patterns": ["*.py"]}
  },
  "module": {
    "ranking": {"patterns": ["*/ranking/*", "modules/ranking/*"]},
    "prerank": {"patterns": ["*/prerank/*"]}
  }
}
```

- **global**：所有文件都会跑，用于安全、性能等通用规则（对应 `agents/global/code-reviewer-*.md`）
- **filetype**：按文件类型分流，如 cpp 文件走 `code-reviewer-cpp.md`
- **module**：按业务模块分流，如 ranking 模块走 `code-reviewer-ranking.md`

global 层的 patterns 为空数组 `[]`，表示匹配所有文件；filetype 和 module 层的 patterns 定义文件路径匹配规则，使用 `fnmatch` 通配符 + 路径包含匹配。一个文件可同时命中多个 Agent（如 `binary/module/ranking/es/common_queue/new_queue.cc` 同时命中 cpp 和 ranking）。

路由规则外置为 `router_rules.json`，新增模块只需在 `agents/module/` 下新建文件并在路由配置中添加 patterns，**完全不需要改动 service.py**。

```
agents/
  router_rules.json          # 路由规则：文件路径 → Agent
  global/                    # 通用规则（所有文件都执行）
    code-reviewer-security.md
    code-reviewer-performance.md
  filetype/
    code-reviewer-cpp.md     # C++ 代码通用规则
  module/
    code-reviewer-ranking.md
    code-reviewer-prerank.md
    code-reviewer-retrieval.md
    code-reviewer-ab.md
    code-reviewer-merchant.md
    code-reviewer-common.md  # 跨模块通用规范
```

**规则与 Agent 的对应关系**：
- `code-reviewer-security.md` / `code-reviewer-performance.md` → global 层，作用于所有文件
- `code-reviewer-cpp.md` → filetype 层，只作用于 cpp/cc/h 文件
- `code-reviewer-ranking.md` → module 层，只作用于 ranking 相关路径
- `code-reviewer-common.md` → module 层，跨模块通用规范

**关键设计：每个 Agent 获取全量 diff**。虽然文件按规则分流到不同 Agent，但每个 Agent 运行时拿到的都是全量代码 diff，防止 Agent 对代码的断章取义——比如精排的 Agent 在审核精排代码时，可能依赖预排的字段，需要看到完整的上下文。

#### 3. codeagent 调用与 prompt 示例

service.py 通过 `codeagent -q <prompt>` 调用 codeagent，将 Agent 配置内容和变更文件列表注入 prompt，驱动 codeagent 执行审查。简化示例：

```
[Agent 配置内容 - 来自 code-reviewer-ranking.md]

---

请审查以下代码变更。

需要审查的文件：
- binary/module/ranking/es/common_queue/new_queue.cc
- modules/ranking/module/consume/ranking_score_calculate_module.py

请使用 bash 工具执行 git diff 命令查看具体变更。

请直接输出审查结果：
- 如果发现问题，输出：
【问题类型】规范X
【文件位置】文件名:行号
【问题描述】具体描述
【修复建议】如何修复
【严重程度】高/中/低

- 如果没有发现问题，输出"未发现问题"。
```

实际调用时会注入具体命令提示，如 `git diff {branch}...HEAD -- <文件路径>`，帮助 Agent 定位变更。Agent 根据规则和全量 diff 自主调用工具探索代码，输出结构化审查结果。

#### 4. 规则沉淀示例

已沉淀的典型规则包括：

**C++ 安全类**：
- 容器访问前必须判空（`top()`/`front()`/`back()`/`pop()` 前需 `empty()` 保护）
- 指针访问判空、数组越界、除 0 检查
- 禁止使用会抛异常的方法（如 `std::stol`）

**C++ 性能类**：
- 禁用 `std::unordered_map`，应使用 `folly::F14FastMap`
- `string_view` vs `string` 拷贝问题
- 禁止在 item 粒度调用 `perf`、`MemoryDataMapSingleton` 等

**精排模块**（对应 `code-reviewer-ranking.md`）：
- 严禁覆盖主模型产出的分数字段
- 避免在 ranking 阶段重复抽取 prerank 已抽取的字段

### 2.6 遇到的问题及解法

| 问题 | 原因 | 解法 |
|------|------|------|
| 全量规则导致上下文膨胀，注意力分散 | 单次 session 输入所有规则 | 按 global/filetype/module 拆分，多 Agent 并行 |
| 改动局部代码需遍历所有规则 | 路由规则硬编码 | 引入 router_rules.json，外置路由配置 |
| 某些 case 被"遗忘"漏检 | context 过长超出模型有效注意力范围 | 缩短每个 Agent 上下文，保持专注 |
| codeagent 偶发空输出或异常 | CLI 边界情况 | 3 次自动重试 + 详细日志 |
| IDC 镜像无法直接运行 codeagent | CentOS 7 glibc 版本为 2.17，官方新版 Node.js 链接了更高版本 glibc 符号 | 使用 unofficial-builds.nodejs.org 重新编译的 Node.js v18.20.5（只依赖 glibc 2.17 及以下），安装到独立目录并通过软链切换 |

### 2.7 效果验证

当前系统刚建起来，尚未收集使用指标，但可以用一个真实 Case 说明 Agent 的优势。

**Case：如何发现"覆盖主模型分数字段"的问题**

某策略提交的 MR，试图覆盖主模型产出的分数字段。review 规范中写明了严禁覆盖主模型的分数字段。但主模型产出该字段的位置，和策略写覆盖逻辑的位置，中间相隔 48 个 Module，距离很远。

**纯 LLM 方案的问题**：如果要发现这个问题，需要：
1. 通过静态扫描发现 MR 有产出字段
2. 在代码切片部分反查该字段是否和主模型产出的字段有关系
3. 或者配置主动切出主模型的字段列表，和产出的字段进行匹配

总之，这是一个**需要人工反复调试、写代码**的过程——每次发现新的覆盖模式，就要写新的静态规则。

**Agent 方案**：只需一条提示词：

```
检查是否有代码覆盖主模型产出的分数字段
```

Agent 会自动执行一系列工具调用：

1. **抓取接口文件**：通过工具调用找到所有可能覆盖字段的接口定义
2. **分析接口能力**：识别哪些接口会覆盖分数字段
3. **扫描代码 diff**：在变更文件中查找是否调用了这些接口
4. **字段匹配**：将接口覆盖的字段与主模型产出的字段列表做比对

整个过程是一系列由 LLM 决策的工具调用，代码更新后依然有效，**无需人写新的静态规则去适配**。

这条规则已在 `code-reviewer-ranking.md` 中沉淀（见 2.5.4 规则沉淀示例）。

**对比**：纯 LLM 方案靠人整理信息、定义规则；Agent 方案靠模型自主探索和推理。随着规则增加，纯 LLM 方案的 prompt 会越来越长、效果越来越差；Agent 方案只需补充提示词，效果随模型能力提升而提升。

---

## 三、总结

**本文做了什么**：

设计并落地了一套基于分层 Agent 的智能 Code Review 方案。通过 router_rules.json 实现三层路由（global → filetype → module），多 Agent 并行审查，每个 Agent 获取全量 diff 上下文。评审规则以 Markdown 文件沉淀在仓库中，增删规则无需改代码、合入即生效。流水线与 MR 联动，报告上传至 CR 平台，支持一键创建 CR 单。

**下一步方向**：

1. **效果评估体系**：建立指标收集体系，收集 reviewer 使用反馈（有效问题率、误报率），量化 CR 效果
2. **自循环建设**：自动抓取线上 bad case，对审核规则进行补充，形成规则→验证的闭环。人的作用仅是补充信息（发现新问题 → 写成提示词规则），其他环节均无需人干预

---

## 附录：目录结构

```
.codeagent/skills/code-review/
  SKILL.md                    # Skill 入口，交互式 CR 的编排指令
  service.py                  # 非交互式服务，流水线调用入口
  agents/
    router_rules.json         # 三层路由规则（global/filetype/module）
    global/                   # 通用规则（所有文件都执行）
      code-reviewer-security.md
      code-reviewer-performance.md
    filetype/
      code-reviewer-cpp.md    # C++ 审查规则
    module/
      code-reviewer-ranking.md
      code-reviewer-prerank.md
      code-reviewer-retrieval.md
      code-reviewer-ab.md
      code-reviewer-merchant.md
      code-reviewer-common.md
```
