# 强化学习的数学原理 笔记

#### 先说一个idea
没有一个好用的、给pdf做笔记的软件。
有很多pdf编辑软件，但编辑的都是本地文件，需要一直保存这个文件才行。或者说，构建的是笔记-pdf文件的关系。一旦文件丢失，笔记也丢失。  
读书软件，如微信读书，pdf不能编辑、做笔记。pdf可以自动转成电子书的格式，可以做笔记了，但是转换过来之后排版还是不好，更不用说有的公式会丢失、错误了。这个排版问题可能很难完美解决，再怎么转都不如pdf原生的排版好。这种的笔记属于托管到平台了，平台保证笔记和书的对应关系。  
希望有这么一个软件：  
1. 可以对pdf做笔记，划线写想法那种，类似微信读书。  
2. 构建的是内容块和笔记的关系。也就是说，这个笔记锚住的是内容块——即使这个pdf丢了，我又从网上下载了一个，只要上传，依然可以把保存的笔记和内容对应上。  

谁来做个这样的app，我就不用在另外一个地方记笔记了。  

#### 2.1
回报可以评估整个回合所使用的策略（没有概率分布哦，全是已固定的策略）的好坏。  
剧透：每个状态都有个策略概率分布，所有状态的策略概率分布合一起，就是策略模型，后边用神经网络来保存策略，并通过梯度下降找到最优策略。  
回报是真实的折扣奖励加和得出的值，不存在任何概率分布。文中举例$`return_3`$通过概率分布计算了回报，这实际是$`s_1`$的状态价值，而不是回报。回报的策略一定是固定的。只有状态价值是期望，包含了概率分布。

#### 2.2引出自举、贝尔曼方程
这节挺有意思。通过一个简单示例，引出了不同状态回报之间的关系，通过自举，很清楚的构建起了各状态回报的方程，展示了贝尔曼方程的要义。

举的例子比较特殊，形成了一个循环，所以能很清楚的写出一个线性方程组。  
比较复杂的真实场景下，虽然不是这么直接一个循环，但状态一定在这些状态间转移（建模时候应该必须保证不会跳到其他状态，至少也得跳到一个unknown状态），所以一定可以写出一个线性方程组。但，是否所有写出的线性方程组都有解呢？  

>线代小课堂

解方程：  
```math
v = r + \gamma P v\\
v - \gamma P v = r
```
引入单位矩阵，单位矩阵就是线代界类似标量界的1，单位矩阵乘以任何矩阵，都等于矩阵本身。  
单位矩阵是对称矩阵，shape一定是(n,n)的，n>0。对于shape是(m,n)的矩阵：
```math
I_mv = v\\
vI_n = v
```
在矩阵左边和矩阵右边的单位矩阵shape是不一样的。  
因此：
```math
v - \gamma P v = r\\
Iv - \gamma P v = r \\
(I - \gamma P) v = r
```
这里，v的shape是(state_size, 1),P的shape是(state_size, state_size)，I的shape也是(state_size, state_size)，因此可以做减法。  
引入逆矩阵：
一个矩阵和逆矩阵乘结果是单位矩阵：
```math
AA^{-1}=I
```
因此：
```math
(I - \gamma P)^{-1}(I - \gamma P) v = (I - \gamma P)^{-1}r\\
v = (I - \gamma P)^{-1}r
```
并非任何矩阵都有逆矩阵，所以是否存在满足上式的逆矩阵，就意味着贝尔曼方程是否可解。  


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
  
补充：  
- 状态奖励是期望，期望的value是从当前状态开始到回合结束的折扣奖励
- 回报是单回合从头到尾的折扣奖励，不涉及多回合

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
>为什么要搞这个变形呢？公式看多了，就发现，这种变形实际上是为了“对问题做分解”，分解成两部分分开处理，可以让概念更清晰或者更易处理等等。这里已经开始将折扣奖励分开成即时奖励和未来奖励了。即时奖励只和本状态有关，未来奖励和未来的状态有关，分开处理。

so
```math
v_\pi(s) = \mathbb{E}[R_{t+1}+\gamma G_{t+1}|S_t=s]
```
由于期望是线性的，于是分成两部分：
```math
v_{\pi}(s) = \mathbb{E}[R_{t+1}|S_t=s] + \gamma \mathbb{E}[G_{t+1}|S_t=s]
```
前半部分是即时奖励期望，后半部分是未来奖励期望。先看即时奖励：
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
将即时奖励和未来奖励放到一起： 
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
《深度学习入门4：强化学习》中，将奖励看做$`s`$的函数。《数学原理》里也提到了这种做法。这种可以对方程进行简化，r只和$`S_{t+1}`$有关：
```math
\begin{align}
v_{\pi}(s)
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)\sum_{s'\in\mathcal{S}}p(S_{t+1}=s'|S_t=s,A_t=a)[r(s')+\gamma v_\pi(s')]
\end{align}
```

整体推导思路梳理：  
- 展开为即时奖励和未来奖励两部分
- 未来奖励主要引出$`v_\pi(s')`$，从而建立起$`v_\pi(s)`$和$`v_\pi(s')`$的联系
    - 引入$`S_{t+1}`$
    - 通过马尔科夫过程消掉多余的$`S_t`$
- 通过将边缘概率转换为联合概率，整合公式公共项

#### 矩阵化
之前推导出的贝尔曼方程：
```math
\begin{align}
v_{\pi}(s)
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)\sum_{s'\in\mathcal{S}}p(S_{t+1}=s'|S_t=s,A_t=a)[r(s')+\gamma v_\pi(s')]
\end{align}
```
拆分成即时奖励和未来奖励：
```math
\begin{align}
v_{\pi}(s)
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)\sum_{s'\in\mathcal{S}}p(S_{t+1}=s'|S_t=s,A_t=a)r(s')+\gamma \sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)\sum_{s'\in\mathcal{S}}p(S_{t+1}=s'|S_t=s,A_t=a)v_\pi(s')
\end{align}
```
书里对公式做了简化，以更清晰的表示矩阵。  
```math
\begin{align}
r_\pi(s)
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)\sum_{s'\in\mathcal{S}}p(S_{t+1}=s'|S_t=s,A_t=a)r(s')
\end{align}
```
```math
\begin{align}
p_{\pi}(s'|s)
&=\sum_{a\in\mathcal{A}}\pi(A_t=a|S_t=s)p(S_{t+1}=s'|S_t=s,A_t=a)
\end{align}
```
简化为：
```math
\begin{align}
v_{\pi}(s)
&=r_\pi(s)+\gamma \sum_{s'\in\mathcal{S}}p_{\pi}(s'|s)v_\pi(s')
\end{align}
```
为啥要这么简化？公式的每一次简化/拆分，都是想突出重点。  
公式中的即时奖励部分，想想，其实当前状态$`s`$确定了，即时奖励也就能计算出来了，所以它是一个向量，每个状态一个值。未来奖励部分，输入是当前状态$`s`$，输出是下一个可能的状态$`s'`$，所以针对每个$`s,s'`$对，都有一个系数，所以是个矩阵。而$`v_\pi(s)`$和$`v_\pi(s')`$，都是向量，长度是状态个数。  
把不同的状态通过i,j表示出来，就是：
```math
\begin{align}
v_{\pi}(s_i)
&=r_\pi(s_i)+\gamma P_{\pi}(s_j|s_i)v_\pi(s_j)
\end{align}
```
其中$`P_{\pi}(s_j|s_i)=\sum_{s_j\in\mathcal{S}}p_{\pi}(s_j|s_i)`$  
这么一简化状态之间的关系就很清楚了。  

$`P_\pi`$的性质挺有意思，满足概率的性质，即大于等于0，且合为1.

#### 贝尔曼方程有解的证明
搞不懂了，还用到了盖尔圆定理，查了下，超出了线性代数基础教材的范畴，属于高等工程数学。  
先跳过。2.7.1节。

#### 迭代法
就是鱼书中的DP法。  
```math
v_{k+1}=r_\pi + \gamma P_\pi(s'|s)v_{k}\ \ \ (k=0,1,2...\infty)
```
注意，这里是$`v_{k+1}`$，不是$`v_\pi(s)`$，不是个函数了，而是个向量。本身这是个未知量，Closed-form solution中使用线性代数的方法解未知量。这里使用了迭代法逐步更新解未知量。k代表迭代次数，趋于无穷。  
需要证明当$`k->\infty`$时$`v_k->v_\pi`$，$`v_\pi`$是贝尔曼方程的解，也是个向量。  
设：
```math
\delta_k=v_\pi - v_k
```
等价于证明$`\delta_k->0`$

```math
\begin{align}
\delta_{k+1} &= v_\pi - v_{k+1}\\
&=v_\pi - (r_\pi + \gamma P_\pi(s'|s)v_k)\\
&=v_\pi - r_\pi - \gamma P_\pi(s'|s)v_k \\
&=v_\pi - r_\pi - \gamma P_\pi(s'|s)(v_\pi - \delta_k)\\
&=v_\pi - r_\pi - \gamma P_\pi(s'|s)v_\pi +  \gamma P_\pi(s'|s)\delta_k \\
&=\gamma P_\pi(s'|s)\delta_k + v_\pi - (r_\pi + \gamma P_\pi(s'|s)v_\pi)
\end{align}
```
由于
```math
v_\pi = r_\pi + \gamma P_\pi(s'|s)v_\pi
```
因此：
```math
\delta_{k+1} = \gamma P_\pi(s'|s)\delta_k
```
是个递归结构，又已知$`\gamma`$和$`P_\pi(s'|s)`$都小于1大于0，所以当$`k->\infty`$时$`\delta_{k+1}->0`$

>感觉这个证明是一种套路，问了下deepseek这里证明的方法是什么方法，deepseek:"证明本质是应用巴拿赫不动点定理:若一个算子 T 在完备度量空间上是压缩映射​（即存在 $`\gamma<1`$ 满足$`||T(v)−T(w)||≤\gamma||v−w||）`$，则其不动点存在唯一，且任意初始值迭代$`v_{k+1}=T(v_k)`$ 均收敛到该不动点。"不太理解，先记下了。

#### 2.8行动价值
这个看鱼书时候比较懵逼，但是代码上比较清晰：状态价值state当key，行为价值拿(state,action)当key，这是我能理解到的。但是缺乏一种感性上的和状态价值的连接，总觉得引出它比较突兀。  
>越发感觉，虽然数学都是推导，但是有时候“理解了”却是一种“感觉”。只有捕捉到那种“哦，这样啊”的感觉的时候，这个疑问才彻底终止，否则总是觉得像有根刺没拔下来，后续的推理也都模糊。  

状态价值和行动价值之间的关系：
```math
\begin{align}
v_\pi(s) &= \sum_{a\in\mathcal{A}}\mathbb{E}[S_{t+1}=s'|S_t=s,A_t=a]\pi(A_t=a|S_t=s)\\
&= \sum_{a\in\mathcal{A}}q_\pi(A_t=a,S_t=s)\pi(A_t=a|S_t=s)
\end{align}
```
```math
q_\pi(a|s) = \sum_{r\in\mathcal{R}}p(R_t=r|A_t=a,S_t=s)r + \gamma \sum_{s'\in\mathcal{S}}p(S_{t+1}=s'|S_t=s,A_t=a)v_\pi(s')
```
对比行动价值和状态价值的公式，只是少了抽出来的公共项$`\sum_{a\in\mathcal{A}}\pi(a|s)`$。严重怀疑，这个行动价值的定义就是为了把外边这层去掉。  

#### 2.8.1不能因为策略中不执行某个action就不计算这个action的行为价值
区分一下，是策略中不执行这个action，而不是环境限制了不能执行这个action。  
如果是环境限制了不能执行这个action，是不用计算行为价值的。  
如果是策略显示这个action的概率是0，可能只是策略不够好，有可能随着迭代，这个action变成了最优action。  
策略本身是要迭代优化的对象，所以不能根据策略来做剪枝。  

#### 2.8.2 矩阵形式的行动价值
```math
q_{\pi}(s,a)=\sum_{r\in\mathcal{R}}p(r|s,a)r+\gamma\sum_{s^{\prime}\in\mathcal{S}}p(s^{\prime}|s,a)\sum_{a^{\prime}\in\mathcal{A}(s^{\prime})}\pi(a^{\prime}|s^{\prime})q_{\pi}(s^{\prime},a^{\prime})
```
更深刻的意识到公式和矩阵的联系了。  
你看$`p(s'|s,a)`$，s,a下s'的概率，用矩阵就是(状态，行动)组合数个行、状态数个列的矩阵。这个矩阵要通过((状态，行动)，状态)来定位到转移的概率。  
再看$`\pi(a'|s')`$，就是行是状态数，列是行动数的矩阵。  
这两个矩阵相乘，shape也对得上。结果是行是(状态，行动)列是行动的矩阵，表明从(s,a)转移到a'的概率。  
所以解贝尔曼方程就是解这个线性变换有没有最优解。  

#### 3.1 优化策略
意识到，之前的例子都是一个策略，通过策略和环境模型可以通过贝尔曼方程解出状态价值或者行动价值，然后通过价值评估策略好坏。只有评估，没有改进。这里的一句"improve policies"点醒了我。不但要有方法评估，还要有方法改进。  
动态规划法是解决解贝尔曼方程计算量大的问题。
后面蒙特卡洛法是解决环境模型不可知的问题。  

#### 3.3 理解了为什么有最优方程
鱼书的时候这里比较懵逼，最优不就是取行动价值最大那个行动吗，这里搞个方程在说什么。  
数学原理这里点出来了。之前的贝尔曼方程只有一个未知变量状态价值，策略是不变的，所以都是常数，要解这个方程求出状态价值。  
现在为了找“最优策略”，策略本身也成了一个变量，要解方程找一个最优的变量。所以是一个方程解两个变量。  

#### 柯西序列$`||x_m−x_n||<ε, m,n>N.`$和$`x_{n+1}−x_n →0`$有什么区别？

注意，柯西序列中，m,n是>N的任意m,n，并不是相邻的。意味着存在一个N，从超过N的n开始到正无穷，$`x_n`$也就增长了不到$`ε`$。这是真正的收敛，这个函数的增长有尽头。  
而$`x_{n+1}`$和$`x_n`$是相邻项。相邻项的增长很小，但如果每个相邻项都增长很小的一点，累积起来还是会超过ε。  
只有前者这种增长有尽头的，才会找到一个“不动点”。

#### 如何理解max算子？
$`\pi`$可以认为是所有状态可执行的行动的概率分布的集合。可以用一个状态数行行动数列的矩阵表示。矩阵中每一项都是大于0的浮点数，且每行的合为1。$`\pi`$表示的是这个矩阵所有可能取值的集合。  
而max算子，就是取这个集合中的一个。也就是通过max算子后，$`\pi`$矩阵固定下来了。这个矩阵是让每个状态价值最大的矩阵。  
最优方程的求解过程，就是从$`\pi`$的所有可能取值集合中找到那个让状态价值最优的取值。所以这时候$`\pi`$是个变量。  

这时候就引入了两个变量，$`\pi`$和$`s`$。3.3.1在介绍如何解这种两个变量的方程：先定住$`s`$求$`max(\pi)`$，然后再求$`s`$。然后又证明了，$`max(\pi)`$就是让行动价值最大的行动概率为1。  
这里状态价值和行动价值来回穿插，搞得有点乱。  

以上的理解，实际上是以将贝尔曼方程分解为$`\pi`$和$`q(s,a)`$的形式理解的，这种比较好理解。  
后面证明压缩映射换回了状态价值的贝尔曼方程:
```math
v=\mathrm{max}_{\pi\in\Pi}(r_{\pi}+\gamma P_{\pi}v)
```
这时候$`\pi`$隐藏在了$`r_\pi`$和$`P\pi`$里，就不是那么能get到max算子的含义了。$`\pi`$明明是方程里一个变量，但是公式里你又看不到这个变量，所以捉急。  
但为了证明贝尔曼方程是个压缩映射，这种方式更清晰些。  

#### 范数
"将数学对象（如数值、向量、函数）映射到非负实数的函数".对于标量来说就是取绝对值，对于向量来说，有几种可选。压缩映射对所有类型的范数都应该是有效的。  

#### 第三章行文思路
3.1 先给了具体例子，首先设定一个固定的策略，求不同状态的价值，然后根据求出的各状态状态价值，求出了一个状态不同行动的行动价值，并且能看出来，有一个行动的行动价值最高，从而选出了这个状态的最优策略。这其实就是后续寻找最优策略的方法：先给随机策略，然后计算状态价值，然后得出最佳行动策略，然后再计算状态价值，以此循环，最终得出最优策略。能得出最优策略的理论依据是压缩映射。  
3.2 给出最优状态价值和最优策略的定义，引出后续的证明。  
3.3 结合贝尔曼方程和3.2定义给出贝尔曼最优方程公式。3.3.1给出示例，怎么解有两个变量的方程，导出如何解贝尔曼最优方程。3.3.2 

#### 解贝尔曼最优方程
两种形式的贝尔曼方程：
```math
\begin{align}
v_(s)
&=r_\pi(s)+\gamma \sum_{s'\in\mathcal{S}}p_{\pi}(s'|s)v_\pi(s')
\end{align}
```
```math
\begin{align}
v_(s) 
&= \sum_{a\in\mathcal{A}}\pi(a|s)q_\pi(a,s)\\
&= \sum_{a\in\mathcal{A}}\pi(a|s)[\sum_{r\in\mathcal{R}}p(r|s,a)r + \gamma \sum_{s'\in\mathcal{S}}p(s'|s,a)v(s')]
\end{align}
```
一种是状态价值形式的，一种是行动价值形式的，后者在有的场景下更有利于理解。这里就是用的行动价值形式的贝尔曼方程。  
贝尔曼最优方程就是选择让状态价值最大的策略，也就是：
```math
\begin{align}
v_(s) 
&= \mathrm{max}_{\pi(s)\in \mathcal{\Pi(s)}}\sum_{a\in\mathcal{A}}\pi(a|s)[\sum_{r\in\mathcal{R}}p(r|s,a)r + \gamma \sum_{s'\in\mathcal{S}}p(s'|s,a)v(s')]
\end{align}
```
s和s'是同一个向量的不同取值，是个要求解的变量。$`\Pi(s)`$是个集合，max算子要从集合中选出可以让状态价值最大的，也是个要求解的变量。  
等于是要求两个变量的方程。理论上应该是解不出来的，不过由于其中一个是max，有方法能解开。  
  
比如这个方程：
```math
x = \mathrm{max}_{y\in \mathcal{R}}(2x-1-y^2)
```
先忽略x求右边的y什么时候最大，对y求导，导数等于0，可解y=0时2x-1-y^2最大。  
此时：
```math
x = 2x -1\\
x = 1
```
因此，方程的解为x=1,y=0.  

对贝尔曼最优方程也是一样的方法。  
```math
\begin{align}
v_(s) 
&= \mathrm{max}_{\pi(s)\in \mathcal{\Pi(s)}}\sum_{a\in\mathcal{A}}\pi(a|s)q_\pi(a,s)
\end{align}
```
先解max。$`\pi(s)`$等于多少的时候$`v(s)`$最大？这个问题等同于问：
```math
\sum_{i=1}^{3}c_iq_i = c_1q_1 + c_2q_2 + c_3q_3
```
且$`\sum_{i=1}^{3}c_i=1`$，在$`c_i`$取值为多少时值最大。  
假设$`q_3=\mathrm{max}(q_1,q_2,q_3)`$，则$`c_3=1,c_1=0,c_2=0`$是解。  
因为：
```math
\begin{align}
q_3 - (c_1q_1 + c_2q_2 + c_3q_3) &= (c_1+c_2+c_3)q_3 - (c_1q_1 + c_2q_2 + c_3q_3)\\
&= c_1q_3+c_2q_3+c_3q_3 - c_1q_1 - c_2q_2 - c_3q_3 \\
&= c_1(q_3-q_1)+c2(q_3 - q_2)+c3(q_3-q_3)\\
&\ge 0
\end{align}
```
在c1,c2,c3取任何大于等于0的值时，等式都大于0，因此$`c_3=1,c_1=0,c_2=0`$是解。  
再转回贝尔曼最优方程，解为让$`q_\pi(a,s)`$最大的行动的概率为1，其他行动概率为0。
```math
\begin{align}
v_(s) 
&= \max_{a\in\mathcal{A}} \sum_{a\in\mathcal{A}}\pi(a|s)q_\pi(a,s)\\
&= \max_{a\in\mathcal{A}} q_\pi(a,s)\\
&= \max_{a\in\mathcal{A}} [\sum_{r\in\mathcal{R}}p(r|s,a)r + \gamma \sum_{s'\in\mathcal{S}}p(s'|s,a)v(s')]
\end{align}
```
$`\pi(a|s)`$为什么不见了？因为之前是概率分布，找到解之后是具体值了，代入具体值之后也就不见了。
```math
\pi(a|s) = 
\begin{cases}
1, a = \argmax_a q(s,a)\\
0, a \ne \argmax_a q(s,a)
\end{cases}
```
至此，我们解出了贝尔曼最优方程两个变量之一的$`\pi(s)`$。
>这段不知道是干什么用的，确实理解了max算子，但是也没有解出来整个方程

#### 压缩映射
又叫不动点理论。  
不动点说的是：
假如有一个$`x\in R^d`$（注意可以是标量，也可以是向量）,一个$`f,R^d->R^d`$（是相同维度的映射），存在一个点$`x^*`$使得：  
```math
f(x^*) = x^*
```
这个点$`x^*`$叫不动点。也就是经过映射后的输出等于输入。  
什么样的$`f`$会存在不动点呢？  
如果存在一个$`\gamma \in (0,1)`$，满足任意的$`x_0,x_1\in R^d`$：$`||f(x_0) - f(x_1)|| < \gamma||x_0 - x_1||`$，则$`f`$称为压缩映射，一定会存在一个不动点。  
一旦证明一个$`f`$是压缩映射，就可以得出以下结论：  
存在性：一定存在一个不动点  
唯一性：不动点唯一  
获取不动点的算法：  
```math
x_{k+1} = f(x_k)
```
$`k=0,1,2...`$，当$`k \to \infty`$时，$`x_k \to x^*`$，可以得到不动点，$`x_0`$可以是任意值。且收敛速度是指数级的。  
##### 举几个例子：  
$`f(x)=0.5x, x\in R`$  
可以直接看出来$`x=0`$是不动点。可以按照公式推导下。  
```math
\begin{align}
||f(x_0) - f(x_1)|| < \gamma||x_0 - x_1||\\
||0.5x_0 - 0.5x_1 || < \gamma ||x_0 - x_1||\\
||0.5(x_0 - x_1) || < \gamma ||x_0 - x_1||
\end{align}
```
当$`\gamma \in (0.5,1)`$时，不等式成立。因此这是一个压缩映射。  
$`0.5x`$是一条穿过原点的直线，且斜率不为1，所以很容易得出不动点存在和唯一的结论。  
然后是算法。假设$`x_0=2`$，看下能否收敛到不动点：
```math
x_1 = 0.5 * 2 = 1\\
x_2 = 0.5 * 1 = 0.5 \\
x_3 = 0.5 * 0.5 = 0.25 \\
x_4 = 0.5 * 0.25 = 0.125\\
....
```
可以看出来数值会一直降低，直到0。其实这么写比较蠢，可以通过公式很容易看出来：
```math
x_{k} = 0.5x_{k-1}\\
x_{k} = 0.5^2x_{k-2}\\
....\\
x_{k} = 0.5^kx_0 = 0.5^k*2
```
当$`k\to\infty`$时，$`x_{k}`$必然等于0。  
##### 再来一个例子：  
$`f(x)=0.5\sin(x),x\in R`$  
先看满不满足压缩映射：  
```math
\begin{align}
||f(x_0) - f(x_1)|| &< \gamma||x_0 - x_1||\\
||0.5\sin(x_0)-0.5\sin(x_1)|| &< \gamma ||x_0 - x_1||\\
\frac{||0.5\sin(x_0)-0.5\sin(x_1)||}{||x_0 - x_1||} < \gamma \\
\end{align}
```
根据拉格朗日中值定理：
```math
f'(c) = \frac{f(b)-f(a)}{b-a}
```
可得：  
```math
\frac{||0.5\sin(x_0)-0.5\sin(x_1)||}{||x_0 - x_1||}=0.5\cos(x_2) \leq 0.5
```
也就是当$`\gamma \in (0,0.5)`$时，不等式成立。函数满足压缩映射条件。  
不动点的求解，就不能像上一个例子那样求了，有几种方法，这不再赘述。x=0是不动点。  
通过算法：
```math
x_k = 0.5\sin(x_{k-1})
```
最终会收敛到不动点。  


