# Skill 回归测试方案：基于 promptfoo

## 问题

Skill 是团队共享的 prompt 模板。当多人协作维护同一个 skill 时，存在一个核心矛盾：

- 用户 A 用得挺好，用户 B 用着可能有问题
- 用户 B 修改 skill 后，自己的场景修复了，但**无法得知是否影响了用户 A 的场景**
- 缺少一套类似单元测试的机制，能在修改后自动验证所有用户的使用场景

本质上，这是一个 **prompt 回归测试** 问题。

## 核心难点

与传统代码的单元测试不同，prompt 测试面临几个特殊挑战：

| 挑战 | 说明 |
|------|------|
| 输出非确定性 | 同一 prompt，LLM 每次输出可能不同，无法 `assertEqual` |
| 评判标准模糊 | "效果好"很难形式化（格式对？内容准确？语气合适？） |
| 上下文依赖 | 同一 skill 在不同代码库、不同对话上下文中表现差异大 |

## 方案：promptfoo

[promptfoo](https://github.com/promptfoo/promptfoo) 是一个开源的 LLM prompt 评测和回归测试框架。

**为什么选它？**

1. **本地运行** — prompt 不会离开本地机器，数据安全
2. **多 provider 支持** — 支持 Claude、OpenAI、Google 等 60+ 模型
3. **CLI + Web UI** — 本地调试方便，CI 集成也简单
4. **断言丰富** — 从简单的字符串匹配到 LLM 评分都支持

**安装**：
```bash
npm install -g promptfoo
# 或
brew install promptfoo
# 或
pip install promptfoo
```

**调用方式**：promptfoo 通过 API 直接调用 LLM，不是通过 Claude Code agent。LLM 执行 prompt 任务，输出结果，然后断言验证。

## 目录结构

```
skills/my-skill/
  prompt.txt                    # skill 的 prompt 模板
  promptfooconfig.yaml          # 测试主配置
  fixtures/                     # 测试用的输入文件
    user-a-component.tsx
    user-b-api.ts
  tests/                        # 各用户维护自己的测例
    user-a-cases.yaml
    user-b-cases.yaml
```

**为什么这样组织？**

按用户分隔测例文件，职责清晰。用户 B 修改 skill 后，只影响自己的测例；用户 A 的测例由用户 A 维护，冲突最小。

## 配置文件

**主配置** `promptfooconfig.yaml`：

```yaml
description: "my-skill 回归测试"

prompts:
  - file://prompt.txt

providers:
  - anthropic:messages:claude-sonnet-4-6

tests:
  - file://tests/user-a-cases.yaml
  - file://tests/user-b-cases.yaml
```

**测例示例** `tests/user-a-cases.yaml`：

```yaml
- description: "[User-A] React hooks 重构"
  vars:
    user_message: "将 class component 转为函数组件"
    code: "file://fixtures/user-a-component.tsx"
  assert:
    - type: contains
      value: "useState"
    - type: not-contains
      value: "componentDidMount"
    - type: llm-rubric
      value: "保留所有原有功能，仅改变组件形式"
```

## 断言类型

promptfoo 提供两大类断言：

### 确定性断言（快、免费、稳定）

| 类型 | 用途 | 示例值 |
|------|------|--------|
| `contains` / `not-contains` | 包含/不包含字符串 | `"async"` |
| `icontains` | 不区分大小写包含 | `"error"` |
| `contains-all` | 同时包含多个字符串 | `["A", "B"]` |
| `regex` | 正则匹配 | `"^export default"` |
| `javascript` / `python` | 自定义表达式 | `"output.length < 500"` |

### LLM 评判断言（处理语义级判断）

| 类型 | 用途 |
|------|------|
| `llm-rubric` | 自由文本描述期望，让 LLM 打分 |
| `factuality` | 检查事实正确性 |
| `similar` | 语义相似度 |

**实用原则**：

- 先用确定性断言覆盖硬性要求（格式、关键词），零成本
- LLM 评分用于语义层面，但要配合 `threshold` 使用，因为 LLM 本身也有波动性

**`llm-rubric` 的特殊性**：它会再次调用 LLM 来评判输出——LLM 既当"运动员"执行任务，又当"裁判"评分。

## 工作流

**第一，修改 skill 后运行测试**：

```bash
cd skills/my-skill
promptfoo eval
```

**第二，查看结果**：

- 用户 A 的测例: 5/5 PASS ✓
- 用户 B 的测例: 3/3 PASS ✓

全部通过才安全合并。

**第三，出现回归怎么办**：

如果用户 A 的测例从 5/5 变成 3/5，说明修改影响了用户 A 的场景。需要分析是哪个用例失败，调整 skill prompt，直到所有测例通过。

**CI 集成示例**：

```yaml
name: Skill Regression Test

on:
  pull_request:
    paths: ['skills/**']

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install -g promptfoo
      - run: cd skills/my-skill && promptfoo eval --no-cache
```

## 实用建议

1. **从简单断言开始** — 先用 `contains` / `not-contains` 覆盖硬性要求
2. **`llm-rubric` 用于语义层面** — 配合 `threshold` 使用以减少波动
3. **每人维护自己的测例文件** — 职责清晰，冲突最小
4. **新增测例前先确认 baseline 通过** — 避免加入本来就不通过的用例
5. **CI 中使用 `--no-cache`** — 确保每次都是真实调用

## 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 规则断言 (contains/regex) | 快、确定、免费 | 只能覆盖粗粒度 | 硬性格式/关键词要求 |
| LLM-as-Judge (llm-rubric) | 能评判语义质量 | 慢、有成本、本身也有波动 | 语义正确性、风格判断 |
| 快照对比 (snapshot) | 能发现任何意外变化 | 需要人工审核 diff | 输出稳定性监控 |

**推荐组合**：规则断言做 hard gate + LLM-as-Judge 做 soft signal + CI 做自动化门禁。

---

## 总结

Skill 回归测试的核心是：**让用户 B 修改 skill 后，能快速得知是否影响了用户 A**。

通过 promptfoo + 分用户测例 + CI 集成，可以实现：
- 修改前：所有测例通过
- 修改后：所有测例仍然通过
- 回归早发现，而不是上线后才发现

**注意**：promptfoo 是 LLM-based 方案，通过 API 直接调用 LLM。如果你的场景需要 Claude Code agent 来执行测试，需要另设计基于 agent 的评测方案。
