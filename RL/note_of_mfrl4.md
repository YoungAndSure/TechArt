### QAC
激动啊，终于到这了，喜极而泣！  
策略梯度法是把策略$`\pi`$中的$`\theta`$搞成了自变量，去最大化平均奖励。其中的行动价值，既可以是蒙特卡洛法用采样值估计，也可以用一个模型估计。  
诶，这时候之前的sarsa就派上用场了。sarsa是介绍method approximation后的算法，那个时候，价值评估和策略提升还是两步。价值评估都是通过迭代法+method approximation去逼近当前策略下的真实状态价值/行动价值。策略提升就是等价值收敛后，采用贪婪策略得出最优策略。  
而现在，在策略梯度法的策略提升过程中，就有一个行动价值需要去估计。自然的，就想到，用sarsa中的价值评估方法，就可以得到当前策略下的真实状态价值。于是自然的，QAC就诞生了。  

#### 为什么要降低样本方差  
终于明白了，之前看鱼书只是知道降方差好，不知道为什么。  
一个随机变量$`X`$，如果$`\mathrm{var}(X)`$低，说明样本都在期望$`\mathbb{E}[X]`$附近波动，只需要几条样本就可以逼近期望。如果$`\mathrm{var}(X)`$高，那就需要更多的样本，才能逼近期望。  
所以，降样本方差可以让模型更快收敛。  

#### A2C(Advantage Actor-Critic)
之前策略梯度法的梯度是：  
```math
\mathbb{E}_{S-\eta,A-\pi}[\nabla_{\theta}\ln\pi(A|S,\theta)q_{\pi}(S,A)]
```
现在改为：  
```math
\mathbb{E}_{S-\eta,A-\pi}[\nabla_{\theta}\ln\pi(A|S,\theta)(q_{\pi}(S,A)-b(S))]
```
让行动价值减去一个$`b(S)`$。  
为什么是$`b(S)`$而不是和行动价值一致的$`b(S,A)`$？这个后面再说。  
引入$`b(S)`$的目的是，在不影响期望的情况下，降低行动价值的方差。为什么，上边说了，方差小，收敛会更快。  
证明下$`b(S)`$的期望等于0。  
```math
\begin{align}
&\mathbb{E}_{S-\eta,A-\pi}[\nabla_{\theta}\ln\pi(A|S,\theta)(q_{\pi}(S,A)-b(S))]\\
&=\mathbb{E}_{S-\eta,A-\pi}[\nabla_{\theta}\ln\pi(A|S,\theta)q_{\pi}(S,A)] - \mathbb{E}_{S-\eta,A-\pi}[\nabla_{\theta}\ln\pi(A|S,\theta)b(S)]
\end{align}
```
```math
\begin{align}
&\mathbb{E}_{S-\eta,A-\pi}[\nabla_{\theta}\ln\pi(A|S,\theta)b(S)]\\
&= \sum_{s\in\mathcal{S}}\eta(s)\sum_{a\in\mathcal{A}}\pi(a|s,\theta)\nabla_{\theta}\ln\pi(a|s,\theta)b(s)\\
&= \sum_{s\in\mathcal{S}}\eta(s)\sum_{a\in\mathcal{A}}\nabla_{\theta}\pi(a|s,\theta)b(s)\\
&= \sum_{s\in\mathcal{S}}\eta(s)b(s)\sum_{a\in\mathcal{A}}\nabla_{\theta}\pi(a|s,\theta)\\
&= \sum_{s\in\mathcal{S}}\eta(s)b(s)\nabla_{\theta}\sum_{a\in\mathcal{A}}\pi(a|s,\theta)\\
&= \sum_{s\in\mathcal{S}}\eta(s)b(s)\nabla_{\theta}1\\
&= 0
\end{align}
```
初看有点神奇，变换都是熟悉的，怎么变着变着就搞成0了。感性理解是，$`b(S)`$和$`\theta`$无关，所以不影响策略$`\pi(A|S,\theta)`$的梯度，所以求梯度的时候会变成0。  
然后回答刚才那个问题，为啥是$`b(S)`$而不是$`b(S,A)`$呢？那显然，$`b(S,A)`$包含了$`A`$，也就和策略$`\pi(A|S,\theta)`$扯上了关系，如果展开：  
```math
\begin{align}
&\mathbb{E}_{S-\eta,A-\pi}[\nabla_{\theta}\ln\pi(A|S,\theta)b(S,A)]\\
&= \sum_{s\in\mathcal{S}}\eta(s)\sum_{a\in\mathcal{A}}\pi(a|s,\theta)\nabla_{\theta}\ln\pi(a|s,\theta)b(s,a)\\
&= \sum_{s\in\mathcal{S}}\eta(s)\sum_{a\in\mathcal{A}}\nabla_{\theta}\pi(a|s,\theta)b(s,a)
\end{align}
```
$`b(s,a)`$和$`a`$有关，就没法移动到前面去了，就不是个常数，没法等于0。  
  
然后，$`b(s)`$等于多少，可以得到最低的方差。  
由于涉及两个随机变量$`S`$和$`A`$，用$`X`$表示一个随机变量向量，则它的方差为一个矩阵。  
比如：  
```math
X=\begin{bmatrix}X_{1}\\X_{2}\end{bmatrix}
```
```math
\begin{align}
\text{Var}(X) &= \begin{bmatrix}\text{Var}(X_{1})&\text{Cov}(X_{1},X_{2})\\\text{Cov}(X_{2},X_{1})&\text{Var}(X_{2})\end{bmatrix} \\
&=\begin{bmatrix}
E[(X_1 - E[X_1])^2] & E[(X_1 - E[X_1])(X_2 - E[X_2])] \\
E[(X_2 - E[X_2])(X_1 - E[X_1])] & E[(X_2 - E[X_2])^2]
\end{bmatrix}
\end{align}
```
可以看到，矩阵对角线是向量中随机变量自己的方差，矩阵中其他部分是随机变量和其他随机变量的协方差。  
既然要最小化方差，就需要一个最小化的目标。这里用矩阵的迹来当做最小化目标。  
迹就是矩阵的对角线和，也就是各个随机变量和自己的方差的和。  
令$`\bar{x}=E[X]`$，$`\mathrm{tr}`$为迹，则：  
```math
\mathrm{tr}[\mathrm{Var}(X)]=\mathrm{tr}\mathbb{E}[(X-\bar{x})(X-\bar{x})^T]
```
分析一下这段，$`X`$是个由$`n`$个随机变量组成的向量，$`\bar{x}`$是它的期望，是个$`n`$个标量组成的向量。则$`(X-\bar{x})(X-\bar{x})^T`$是个$`n\times n`$的随机变量矩阵。$`\mathbb{E}[(X-\bar{x})(X-\bar{x})^T]`$是个$`n\times n`$的标量矩阵。而$`\mathrm{tr}`$意为标量矩阵的对角线和，是个标量。  
继续：  
```math
\mathrm{tr}\mathbb{E}[(X-\bar{x})(X-\bar{x})^T]=\mathrm{tr}\mathbb{E}[XX^T-\bar{x}X^T-X\bar{x}^T+\bar{x}\bar{x}^T]
```
拆开之后每一步都是一个$`n \times n`$的矩阵。继续：  
```math
\mathrm{tr}\mathbb{E}[XX^T-\bar{x}X^T-X\bar{x}^T+\bar{x}\bar{x}^T]=\mathbb{E}[X^TX-X^T\bar{x}-\bar{x}^TX+\bar{x}^T\bar{x}]
```
也就是说，假设有两个n维向量$`Y,Z`$,则$`\mathrm{tr}[YZ^T]=Z^TY`$。举个具体例子：  
```math
Y=\begin{bmatrix}y_{1}\\y_{2}\end{bmatrix},\quad Z=\begin{bmatrix}z_{1}\\z_{2}\end{bmatrix}\\
YZ^{T}={\begin{bmatrix}{y_{1}}\\{y_{2}}\end{bmatrix}}{\begin{bmatrix}{z_{1}}&{z_{2}}\end{bmatrix}}={\begin{bmatrix}{y_{1}z_{1}}&{y_{1}z_{2}}\\{y_{2}z_{1}}&{y_{2}z_{2}}\end{bmatrix}}\\
\mathrm{tr}[YZ^{T}]=y_{1}z_{1}+y_{2}z_{2}\\
Z^{T}Y=\begin{bmatrix}z_{1}&z_{2}\end{bmatrix}\begin{bmatrix}y_{1}\\y_{2}\end{bmatrix}=z_{1}y_{1}+z_{2}y_{2}=y_{1}z_{1}+y_{2}z_{2}\\
\mathrm{tr}[YZ^{T}]=y_{1}z_{1}+y_{2}z_{2}=Z^{T}Y
```
主要是$`tr`$只关心对角线，所以调换顺序并没有改变对角线相乘之和。  
继续：  
```math
\begin{align}
&\mathbb{E}[X^TX-X^T\bar{x}-\bar{x}^TX+\bar{x}^T\bar{x}]\\
&= \mathbb{E}[X^TX]-\mathbb{E}[X^T\bar{x}]-\mathbb{E}[\bar{x}^TX]+\mathbb{E}[\bar{x}^T\bar{x}]\\
&= \mathbb{E}[X^TX] - \bar{x}^T\bar{x}-\bar{x}^T\bar{x} + \bar{x}^T\bar{x}\\
&= \mathbb{E}[X^TX]- \bar{x}^T\bar{x}
\end{align}
```
$`\bar{x}^T\bar{x}`$是固定的，所以只需要优化$`\mathbb{E}[X^TX]`$。  
将$`X`$代入：  
```math
\begin{align}
&\mathbb{E}[X^TX]\\
&=\mathbb{E}[(\nabla_{\theta}\ln\pi(A|S,\theta)(q_{\pi}(S,A)-b(S)))^T(\nabla_{\theta}\ln\pi(A|S,\theta)(q_{\pi}(S,A)-b(S)))]\\
&= \mathbb{E}[||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2 (q_{\pi}(S,A)-b(S))^2]
\end{align}
```
$`q_{\pi}(S,A)-b(S)`$是标量，（为什么呢？$`q_{\pi}`$是矩阵，$`q_{\pi}(S,A)-b(S)`$是其中一个元素了，当然是标量了，不要混淆)，$`\nabla_{\theta}\ln\pi(A|S,\theta)`$是向量（为什么？首先跟$`\pi(S,\theta)`$区分开，这个是action_size维的矩阵，但$`\pi(A|S,\theta)`$是其中一列。$`\theta`$会将一个action拓展到$`\theta`$维，所以。）  
  
现在得到了目标函数公式，其中$`b(S)`$是自变量。为了让目标函数最小，也就是目标函数梯度等于0：  
```math
\begin{align}
\nabla_{b}\mathbb{E}[||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2 (q_{\pi}(S,A)-b(S))^2]=0\\
\mathbb{E}[\nabla_{b} ||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2 (q_{\pi}(S,A)-b(S))^2 = 0\\
-\mathbb{E}[2 ||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2 (q_{\pi}(S,A)-b(S))]=0\\
\mathbb{E}[2 ||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2 q_{\pi}(S,A)] - \mathbb{E}[2 ||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2 b(S)] = 0\\
\mathbb{E}[2 ||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2 q_{\pi}(S,A)]=\mathbb{E}[2 ||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2 b(S)]\\
b(S) = \frac{\mathbb{E}[2 ||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2 q_{\pi}(S,A)]}{\mathbb{E}[2 ||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2]}\\
b(S) = \frac{\mathbb{E}[||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2 q_{\pi}(S,A)]}{\mathbb{E}[||\nabla_{\theta}\ln\pi(A|S,\theta||^2_2]}
\end{align}
```
这就是$`b(S)`$的最优值了。  
>书里是把目标函数按$`S`$展开成$`s`$，我不明白为什么。  
  
这个$`b(S)`$取值过于复杂，不好应用，可以把$`\nabla_{\theta}\ln\pi(A|S,\theta||^2_2`$省略掉，变成:  
```math
\begin{align}
b^{\dagger}(S) &= \mathbb{E}_{A-\pi}q_{\pi}(S,A)\\
&= \sum_{a\in\mathcal{A}}\pi(a|S)q_{\pi}(S,a)\\
&= v_{\pi}(S)
\end{align}
```
就是状态价值。  
  
#### A2C算法描述  
加上baseline之后的迭代公式:  
```math
\begin{align}
\theta_{t+1} &= \theta_t + \nabla_{\theta}\ln\pi(A|S,\theta)(q_{\pi}(S,A) - v_{\pi}(S))\\
&= \theta_t + \nabla_{\theta}\ln\pi(A|S,\theta)\delta_t(S,A)
\end{align}
```
其中$`\delta_t(S,A)=q_{\pi}(S,A) - v_{\pi}(S)`$叫相对优势。啊，终于到相对优势了。  
可以这么理解，$`q_{\pi}(S,A)`$是某个动作的价值，$`v_{\pi}(S)`$是所有动作的价值。这里计算的是某个动作相对于所有动作平均表现的优势。用更有用的相对值代替了绝对值。  
随机梯度版：  
```math
\begin{align}
\theta_{t+1} &= \theta_t + \nabla_{\theta}\ln\pi(a_t|s_t,\theta)(q_{t}(s_t,a_t) - v_{t}(s))\\
&= \theta_t + \nabla_{\theta}\ln\pi(a_t|s_t,\theta)\delta_t(s_t,a_t)
\end{align}
```
其中$`q_{t}(s,a)`$和$`v_{t}(s)`$有两种方法获取到，一种是等回合结束，逐个step计算行动价值和状态价值，代入到公式里迭代，也就是蒙特卡洛法。一种是边行动边计算，用估计值代替，也就是TD法。  
用蒙特卡洛法的叫REINFORCE with baseline，用TD法的叫advantage actor-critic(A2C)。  
TD法，要得到$`q_t(s,a)`$和$`v_t(s)`$可以用两个神经网络来估计，不过那样系统更复杂。由于行动价值可以用估计值代替:  
```math
q_t(s_t,a_t) \approx r_t(s_t,a_t) + \gamma v(s_{t+1})
```
因此：  
```math
\delta_t(s_t,a_t) \approx r_t(s_t,a_t) + \gamma v(s_{t+1}) - v(s_t)
```
这样，只需要一个神经网络用来估计状态价值就可以了，降低了系统复杂度。  

#### 重要度采样  
首先要区分随机变量本身的概率分布，和样本的分布。随机变量本身的分布叫总体分布，通过某种采样得到的样本的分布叫样本分布。i.i.d只是一种采样方式，独立、每个样本采样同分布，具体用哪种分布去采样，不在i.i.d的概念里。  
所以，重要度采样讨论的是：  
有个随机变量$`X`$，他的分布是$`p_0(X)`$，通过i.i.d及分布$`p_0(X)`$得到了一个样本集合$`\{x_i\}_{i=1}^n`$。由于是i.i.d的且采样概率分布和总体分布一致，所以样本的均值等于真实的期望。也就是$`\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i=\mathbb{E}[X]`$。  
但现实中，首先你本来就不知道$`X`$的概率分布，所以才要用蒙特卡洛法逼近。然后，在之前的采样中，都是智能体在环境概率分布$`p(s'|s)`$下按照策略$`\pi(a|s)`$行动，收集每一步获取的奖励，这么采样，一方面根据马尔科夫性，状态间决策无关采样是独立的，一方面过程中遵循的是平稳分布，所以，得到的就是按照总体分布独立同分布采样得到的样本集。这种方法必须是on-policy的，因为策略变化后，采样也要同步变化，才能获取到真实的总体分布。  
现在要解决的是如何利用off-policy的样本。比如策略更新前，分布是$`p_0(X)`$根据策略行动得到了一批样本，策略更新后，分布是$`p_1(X)`$理论上这些样本不能用了，因为概率分布已经发生了变化，用之前的概率分布$`p_0(X)`$无法得到现在的期望。重要度采样要解决的就是这个问题。  
  
```math
\mathbb{E}_{X-p_0}[X] = \sum_{x\in \mathcal{X}}p_0(x)x=\sum_{x\in\mathcal{X}}p_1(x)\frac{p_0(x)}{p_1(x)}x=\sum_{x\in\mathcal{X}}p_1(x)f(x)=\mathbb{E}_{X-p_1}[f(X)]
```
根据大数定律，样本均值可以逼近期望，因此：  
```math
\mathbb{E}_{X-p_1}[f(X)]\approx\frac{1}{n}\sum_{i=1}^nf(x_i)=\frac{1}{n}\sum_{i=1}^n\frac{p_0(x_i)}{p_1(x_i)}x_i
```
这就是重要度采样。  
原理其实就是，假如某个样本$`x_i`$，$`p_0(x_i)\gt p_1(x_i)`$，怎么理解，就是在$`p_0`$分布时采样到的次数多于在$`p_1`$分布时，现在拿到的是$`p_1`$分布时的样本，怎么得到$`p_0`$分布时的期望。因为样本里样本数减少了，所以在求均值的时候就吃亏了，所以要加个权重，提升样本值的大小，权重就是$`\frac{p_0(x_i)}{p_1(x_i)}\gt 1`$。  

#### why deterministic case is naturally off-policy and can effectively handle continuous action spaces?
naturally off-policy:  
之前一直在强调探索和利用。随机策略兼顾了探索和利用，因为每个action都有概率执行到。确定策略就没有探索，因为选中action的概率是1。所以它适合off-policy,用探索策略去采样，然后找最优策略。  
什么是coninuous action spaces?类似"移动x米"这种action。之前都是九宫格这种动作数量确定的任务，可以给每个动作分配个概率。对于动作连续的任务，没法给每个动作分配个概率，只能选中一个动作，比如移动5米。所以deterministic处理连续动作空间更高效。  

