# 强化学习的数学原理 笔记

#### 先说一个idea
没有一个好用的、给pdf做笔记的软件。
有很多pdf编辑软件，但编辑的都是本地文件，需要一直保存这个文件才行。或者说，构建的是笔记-pdf文件的关系。一旦文件丢失，笔记也丢失。  
读书软件，如微信读书，pdf不能编辑、做笔记。pdf可以自动转成电子书的格式，可以做笔记了，但是转换过来之后排版还是不好，更不用说有的公式会丢失、错误了。这个排版问题可能很难完美解决，再怎么转都不如pdf原生的排版好。这种的笔记属于托管到平台了，平台保证笔记和书的对应关系。  
希望有这么一个软件：  
1. 可以对pdf做笔记，划线写想法那种，类似微信读书。  
2. 构建的是内容块和笔记的关系。也就是说，这个笔记锚住的是内容块——即使这个pdf丢了，我又从网上下载了一个，只要上传，依然可以把保存的笔记和内容对应上。  

谁来做个这样的app，我就不用在另外一个地方记笔记了。  

#### 2.2节引出自举、贝尔曼方程
这节挺有意思。通过一个简单示例，引出了不同状态回报之间的关系，通过自举，很清楚的构建起了各状态回报的方程，展示了贝尔曼方程的要义。

#### 2.3节开头提到，回报不适合评估随机系统，为什么？
随机系统在某个状态下选择的动作是随机的，导致相同状态下获取到的回报不同。  
回报是整个回合的累计奖励，是从回合的视角来评估的，通过比较回报，可以知道这个回合的轨迹更好、那个回合的轨迹差一些。  
但在实际运行过程中，是基于某个状态来选动作的，如果用回报来指导某个状态该如何选择动作，会发现一个状态对应了很多个回报，且由于随机性，这些回报的方差很大，这就很难决策在当前状态下到底哪个动作是最好的了。  
根本原因是，随机系统中，回报只能显示整个轨迹的好坏，且带有很大随机性，导致难找到规律。又无法把这个规律反馈到轨迹中的某一步中去优化决策。

#### 回报和状态价值有什么区别？
回报是整条轨迹的折扣奖励累积：  
``` math
return = R_0 + \gamma R_1 + \gamma^2 R_2 ....
```
而状态价值是某状态之后（t时刻起）折扣奖励累积——的期望：  
```math
v_\pi(s) = E[G_t|S_t=s]
```
```math
  G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3}....
```
有两点不同：
- 状态价值是状态的函数，只和状态之后的奖励相关
- 状态价值是期望

书中也说了，如果策略$`\pi`$是随机的，那获取的奖励就是随机变量，根据大数定律，随机变量会趋于期望。所以用期望评估策略要比随机变量的累加值（回报）更准些。  
个人理解，强化学习就是把问题抽象成一个随机过程，研究如果捕捉到随机过程中的规律，来获取更好的结果。

#### 2.4 为什么贝尔曼方程即时奖励期望和未来奖励期望两部分得到的$`p(?|s,a)`$一个是按$`s'`$展开一个是按r展开？

有这个疑问是因为这里的展开方式和《深度学习入门4：强化学习》的展开方式不同。那本书里把奖励看做一个以$`s、a、s'`$为输入的函数：
```math
r(s,a,s')
```
并没有概率分布。但是本书引入了针对$r$的的概率分布：
```math
p(r|s,a)
```
所以仔细看公式，两本书的推导是不同的。  

仔细看贝尔曼方程的两部分。  
即时奖励部分，由于只涉及当前状态、动作，和奖励的分布，所以公式是通过奖励分布展开。  
而未来奖励部分，由于涉及了未来状态的转移，所以必须引入状态转移概率分布：$`p(s'|s,a)`$.  
最终推导完，两部分各自出现了$`p(r|s,a)`$和$`p(s'|s,a)`$。通过联合概率与边缘概率的关系公式：  
```math
p(s'|s,a) = \sum_{r \in \mathcal{R}} p(s', r | s, a)
```
```math
p(r|s,a) = \sum_{s' \in \mathcal{S}} p(s', r | s, a)
```
统一了两个概率分布到公共部分。  

这个问题描述的不清楚，有点模糊，可能还缺少一些推导。  

#### 公式展开疑问
```math
\mathbb{E}[G_{t+1}|S_{t}=s]=\sum_{s^{\prime}\in\mathcal{S}}\mathbb{E}[G_{t+1}|S_{t}=s,S_{t+1}=s^{\prime}]p(s^{\prime}|s)
```
这里推导依赖的是条件期望的全期望定律。有点没绕过来，mark一下。  

#### 推导下贝尔曼方程
talk is cheap，不推导一下后续变换的时候总是不能快速反应过来。  

```math
v_\pi(s) = \mathbb{E}[G_t|S_t=s]

```
```math
\begin{align}
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3}....\\
G_{t+1} = R_{t+2} + \gamma R_{t+3} + \gamma^2 R_{t+4}...
\end{align}
```
so
```math
G_t = R_{t+1}+\gamma G_{t+1}
```
so
```math
v_\pi(s) = \mathbb{E}[R_{t+1}+\gamma G_{t+1}|S_t=s]
```
由于期望是线性的，于是分成两部分：
```math
v_{\pi}(s) = \mathbb{E}[R_{t+1}|S_t=s] + \gamma \mathbb{E}[G_{t+1}|S_t=s]
```
前半部分是即时奖励，后半部分是未来奖励。先看即使奖励：
```math
\begin{align}
\mathbb{E}[R_{t+1}|S_t=s]
&=\sum_{a\in\mathcal{A}}\pi(a|s)\mathbb{E}[r|S_t=s,A_t=a]\\
&=\sum_{a\in\mathcal{A}}\pi(a|s)\sum_{r\in\mathcal{R}}p(r|S_t=s,A_t=a)r
\end{align}
```

>*推导过程中发现一个错误写法，把书中的$`S_t=s`$写成了$`s=S_t`$，混淆了概念。$`S_t`$是t时刻的随机变量，而s是随机变量的取值。反过来可就大错特错了*  

>再仔细看下这个公式：$`v_\pi(s) = \mathbb{E}[G_t|S_t=s]`$，$`G_t`$和$`S_t`$都是随机变量，$`s`$是一个具体状态值。所以$`v_\pi(s)`$确实是一个状态的函数。和$`\pi`$相关，时间t无关。这点得用心体会。有的公式你以为你会推导了，实际上是在照葫芦画瓢，对于其中的细节没有深入的理解。  

再看未来奖励。
```math
\mathbb{E}[G_{t+1}|S_t=s]
```
是当状态为s时，下一个状态之后的累计奖励的期望。
引入$`S_{t+1}`$，即下一个状态：
```math
\mathbb{E}[G_{t+1}|S_t=s] = \sum_{s'\in\mathcal{S}}\mathbb{E}[G_{t+1}|S_t=s,S_{t+1}=s']p(S_{t+1}=s'|S_t=s)
```
尝试推导了一下上式，但卡住了，最后问了下deepseek，推导过程很详细，直接贴过来了：
```math
\begin{align*}
\mathbb{E}[G_{t+1} \mid S_t = s] 
&= \sum_{g} g \cdot p(G_{t+1} = g \mid S_t = s) & \text{(条件期望定义)} \\
&= \sum_{g} g \cdot \left[ \sum_{s' \in \mathcal{S}} p(G_{t+1} = g, S_{t+1} = s' \mid S_t = s) \right] & \text{(全概率公式)} \\
&= \sum_{g} g \cdot \left[ \sum_{s' \in \mathcal{S}} p(G_{t+1} = g \mid S_t = s, S_{t+1} = s') \cdot p(S_{t+1} = s' \mid S_t = s) \right] & \text{(条件概率分解)} \\
&= \sum_{s' \in \mathcal{S}} \sum_{g} g \cdot p(G_{t+1} = g \mid S_t = s, S_{t+1} = s') \cdot p(S_{t+1} = s' \mid S_t = s) & \text{(交换求和顺序)} \\
&= \sum_{s' \in \mathcal{S}} \left[ \sum_{g} g \cdot p(G_{t+1} = g \mid S_t = s, S_{t+1} = s') \right] \cdot p(S_{t+1} = s' \mid S_t = s) & \text{(提取公因子)} \\
&= \sum_{s' \in \mathcal{S}} \mathbb{E}[G_{t+1} \mid S_t = s, S_{t+1} = s'] \cdot p(S_{t+1} = s' \mid S_t = s) & \text{(条件期望定义)}
\end{align*}
```
>这么直接看答案可能不太好，容易以为懂了，但是自己推还是不会  

以上公式中“条件概率分解”步骤的推导（这回不是deepseek了，自己推的）：
```math
\begin{align}
p(x,y,z) &= p(x|y,z)p(y,z)\\
&= p(x|y,z)p(y|z)p(z)
\end{align}
```
另一种分解法：
```math
p(x,y,z)=p(x,y|z)p(z)
```
消掉$`p(z)`$:
```math
p(x|y,z)p(y|z)=p(x,y|z)
```
  
回到未来奖励，继续：
```math
\begin{align}
\mathbb{E}[G_{t+1}|S_t=s] &= \sum_{s'\in\mathcal{S}}\mathbb{E}[G_{t+1}|S_t=s,S_{t+1}=s']p(S_{t+1}=s'|S_t=s)\\
&=\sum_{s'\in\mathcal{S}}\mathbb{E}[G_{t+1}|S_{t+1}=s']p(S_{t+1}=s'|S_t=s)
\end{align}
```
这里成立是因为马尔科夫过程：
```math
p(s_{t+1} \mid s_t, a_t, s_{t-1}, a_{t-1}, \ldots, s_0, a_0) = p(s_{t+1} \mid s_t, a_t)
```
```math
p(r_{t+1} \mid s_t, a_t, s_{t-1}, a_{t-1}, \ldots, s_0, a_0) = p(r_{t+1} \mid s_t, a_t)
```
$`G_{t+1}`$是状态$`S_{t+1}`$之后获取的累计奖励，和状态$`S_t`$无关，也就是独立。  
继续：
```math
\begin{align}
\mathbb{E}[G_{t+1}|S_t=s] &= \sum_{s'\in\mathcal{S}}\mathbb{E}[G_{t+1}|S_t=s,S_{t+1}=s']p(S_{t+1}=s'|S_t=s)\\
&=\sum_{s'\in\mathcal{S}}\mathbb{E}[G_{t+1}|S_{t+1}=s']p(S_{t+1}=s'|S_t=s)\\
&=\sum_{s'\in\mathcal{S}}v_{\pi}(s')p(S_{t+1}=s'|S_t=s)
\end{align}
```
由于：
```math
\begin{align}
p(S_{t+1}=s'|S_t=s) = \sum_{a\in\mathcal{A}}p(S_{t+1}=s'|S_t=s,A_t=a)\pi(A_t=a|S_t=s)
\end{align}
```
代入后：
```math
\begin{align}
\mathbb{E}[G_{t+1}|S_t=s] &= \sum_{s'\in\mathcal{S}}\mathbb{E}[G_{t+1}|S_t=s,S_{t+1}=s']p(S_{t+1}=s'|S_t=s)\\
&=\sum_{s'\in\mathcal{S}}\mathbb{E}[G_{t+1}|S_{t+1}=s']p(S_{t+1}=s'|S_t=s)\\
&=\sum_{s'\in\mathcal{S}}v_{\pi}(s')p(S_{t+1}=s'|S_t=s)\\
&=\sum_{s'\in\mathcal{S}}v_{\pi}(s')\sum_{a\in\mathcal{A}}p(S_{t+1}=s'|S_t=s,A_t=a)\pi(A_t=a|S_t=s)
\end{align}
```
以上就是未来奖励了。实际上这里推导的核心目标就是引出$`v_\pi(s')`$，也就下一个状态的价值。这样才能组成一个可解的贝尔曼方程。  
将即使奖励和未来奖励放到一起： 
```math
\begin{align}
v_{\pi}(s) &= \mathbb{E}[R_{t+1}|S_t=s] + \gamma \mathbb{E}[G_{t+1}|S_t=s]\\
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)\sum_{r\in\mathcal{R}}p(r|S_t=s,A_t=a)r + \gamma\sum_{s'\in\mathcal{S}}v_{\pi}(s')\sum_{a\in\mathcal{A}}p(S_{t+1}=s'|S_t=s,A_t=a)\pi(A_t=a|S_t=s)\\
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)[\sum_{r\in\mathcal{R}}p(r|S_t=s,A_t=a)r+\gamma\sum_{s'\in\mathcal{S}}v_{\pi}(s')p(S_{t+1}=s'|S_t=s,A_t=a)]
\end{align}
```
以上尽量把所有简写都展开了，忘了展开r，r其实是$`R_t=r`$。其中$`p(r|S_t=s,A_t=a)`$和$`p(S_{t+1}=s'|S_t=s,A_t=a)`$是$`p(S_{t+1}=s',R_t=r|S_t=s,A_t=a)`$的边缘概率：
```math
p(R_t=r|S_t=s,A_t=a)=\sum_{s'\in\mathcal{S}}p(R_t=r,S_{t+1}=s'|S_t=s,A_t=a)
```
```math
p(S_{t+1}=s'|S_t=s,A_t=a)=\sum_{r\in\mathcal{R}}p(R_t=r,S_{t+1}=s'|S_t=s,A_t=a)
```
因此：
```math
\begin{align}
v_{\pi}(s)
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)[\sum_{r\in\mathcal{R}}p(r|S_t=s,A_t=a)r+\gamma\sum_{s'\in\mathcal{S}}v_{\pi}(s')p(S_{t+1}=s'|S_t=s,A_t=a)]\\
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)[\sum_{r\in\mathcal{R}}\sum_{s'\in\mathcal{S}}p(R_t=r,S_{t+1}=s'|S_t=s,A_t=a)r + \gamma\sum_{s'\in\mathcal{S}}v_{\pi}(s')\sum_{r\in\mathcal{R}}p(R_t=r,S_{t+1}=s'|S_t=s,A_t=a)\\
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)\sum_{r\in\mathcal{R}}\sum_{s'\in\mathcal{S}}p(R_t=r,S_{t+1}=s'|S_t=s,A_t=a)[r+\gamma v_\pi(s')]
\end{align}
```
以上就是贝尔曼方程。  
《深度学习入门4：强化学习》中，将奖励看做$`S_t、S_t、S_{t+1}`$的函数。《数学原理》里也提到了这种做法。这种可以对方程进行简化，r只和$`S_{t+1}`$有关：
```math
\begin{align}
v_{\pi}(s)
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)\sum_{s'\in\mathcal{S}}p(S_{t+1}=s'|S_t=s,A_t=a)[r(s')+\gamma v_\pi(s')]
\end{align}
```
