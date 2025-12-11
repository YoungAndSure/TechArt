#### 函数逼近法应用到蒙特卡洛和TD法推导
问题是这样的，每个状态都有一个状态价值$`v_{\pi}(S)`$。它的计算方法两种，一种是蒙特卡洛法，收集大量样本之后，计算均值，逼近$`v_{\pi}(S)`$。另一种是TD法，通过即时奖励和下一状态的状态价值更新状态价值，逼近$`v_{\pi}(S)`$。两种都需要存储每个状态$`s \in S`$的状态价值。  
函数逼近法是说，不存了，用函数估计。也就是弄个状态的函数（或其他特征代表状态）$`\hat{v}(S)`$，输入状态$`s`$可以输出状态价值$`\hat{v}(s)`$。这个$`\hat{v}(S)`$的参数记为$`w`$，所以可以写为$`\hat{v}(S,w)`$。  
之前TD法，是通过RM算法的思路建模。解的是求$`g(v_{\pi}(s))=v_{\pi}(s_t)-\mathbb{E}[R_{t+1}+\gamma v_{\pi}(S_{t+1})|S_t=s_t]`$的根的问题。函数逼近法是通过随机梯度下降法建模。解的是让估计值$`\hat{v}(S,w)`$和"真实值"$`v_{\pi}(S)`$最小的问题。  
首先是如何衡量预估值和真实值的问题。可以用MSE来评估：  
```math
J(w) = \mathbb{E}[(v_{\pi}(S) - \hat{v}(S,w))^2]
```
这里每个状态执行占比遵循一个分布，因此对损失的贡献不同。所以引出了“稳定分布”的概念。见上文。总之，各状态的损失要按照状态的稳定分布$`d_{\pi}(S)`$作为权重加和：   
```math
J(w) = \sum_{s\in S}d_{\pi}(s) (v_{\pi}(S) - \hat{v}(S,w))^2
```
梯度下降法要对$`J(w)`$求导：  
```math
\begin{align}
\nabla_w J(w) &= \nabla_w\mathbb{E}[(v_{\pi}(S) - \hat{v}(S,w))^2]\\
&= \mathbb{E}[\nabla_w (v_{\pi}(S) - \hat{v}(S,w))^2]\\
&= \mathbb{E}[2(v_{\pi}(S) - \hat{v}(S,w))(- \nabla_w\hat{v}(S,w))]
\end{align}
```
根据梯度下降法：  
```math
\begin{align}
w_{k+1} &= w_k - \alpha_k \nabla_wJ(w_k)\\
&= w_k - \alpha_k \mathbb{E}[2(v_{\pi}(S) - \hat{v}(S,w_k))(- \nabla_w\hat{v}(S,w_k))]\\
&= w_k + 2\alpha_k \mathbb{E}[(v_{\pi}(S) - \hat{v}(S,w))\nabla_w\hat{v}(S,w_k)]
\end{align}
```
根据随机梯度下降法，其中的期望可以替换为采样样本：  
```math
w_{t+1} = w_t + \alpha_t  (v_{\pi}(s_t) - \hat{v}(s_t,w_t))\nabla_w\hat{v}(s_t,w_t)
```
通过以上随机梯度下降法，可以让函数的估计状态价值和真实状态价值差距最小。  
但真实状态价值是一个理想值，需要一个label来引导。  
label有两种。  
一种是蒙特卡洛法，用回合结束后计算出的真实的累积奖励来做真实状态价值，引导估计函数收敛。  
```math
w_{t+1} = w_t + \alpha_t  (g_t - \hat{v}(s_t,w_t))\nabla_w\hat{v}(s_t,w_t)
```
一种是TD法，用有偏的估计值$`r_{t+1}+\gamma v(s_{t+1})`$来做真实状态价值，引导估计函数收敛。有趣的是，在之前的TD法里，下一状态的状态价值，是用样本算出来的估计值，这里也要用函数逼近，所以$`v(s_{t+1})`$要替换成$`\hat{v}(s_{t+1},w_t)`$  
```math
w_{t+1} = w_t + \alpha_t  (r_{t+1}+\gamma \hat{v}(s_{t+1},w_t) - \hat{v}(s_t,w_t))\nabla_w\hat{v}(s_t,w_t)
```
需要注意的是：  
蒙特卡洛法不是增量算法，这里的随机梯度下降中的迭代，是要让估计函数收敛，而不是状态价值收敛。蒙特卡洛法里的状态价值是根据策略$`\pi`$生成的样本算出来的，没有什么收敛不收敛的。  
而TD法是增量算法，本身状态价值就是个估计值，涉及收敛的问题。只是，之前估计值依赖的是其他状态的估计值，是通过样本增量更新得来的，这里是用一个函数估计得来的。所以TD法里的收敛，我理解有两个，一个是状态价值逼近函数的收敛，让估计值逼近TD目标；一个是状态价值的收敛，让状态价值逼近根据期望计算出来的状态价值。  

#### 函数选择
从概念上，我理解$`\hat{v}(S,w)`$是一个函数，输入是状态$`s`$，经过参数$`w`$调整后输出状态价值。实现这个功能有两种方法：  
非线性法(人工神经网络)。理论上线性法更简单直观，但是深度学习多了之后非线性法反倒似乎更直观些。就是搞一个神经网络，输入状态，经过几个全连接层，输出状态价值。如果直接输入的是状态，首层全连接层也就是个embedding层，对应的向量代表状态向量。如果输入的是状态相关的几个特征，则可能要转成多个embeding，最后相加表征一个状态向量。训练过程中embedding也会调整。  
线性法。$`w`$应该是一个m维向量，表示参数。这样的话，状态$`s`$也得是一个m维向量，才能和参数$`w`$乘。因此，需要一个函数将状态转成向量，记为$`\phi(s)`$。我理解这个转换是手工的，比如定义m维每维的含义。其实也就类似神经网络里的embedding了，只是embedding是训练出来的，这里$`\phi(s)`$是人工定义的。因此，状态价值函数为：  
```math
\hat{v}(S,w) = \phi^T(S)w
```
梯度为：  
```math
\nabla_w \hat{v}(S,w)=\phi(S)
```
代入到迭代公式中：  
```math
w_{t+1} = w_t + \alpha_t  (r_{t+1}+\gamma \phi^T(s_{t+1})w_t - \phi^T(s_t)w_t)\phi(s_t)
```
检查下，shape也对得上。加号右面是m维向量，w也是个m维向量，相加没问题。  

#### 为什么最终的迭代公式里没有稳定分布$`d_{\pi}(s)`$？
前边说了，损失函数是所有状态的损失的加和，而所有状态加和的权重是不同的，遵循稳定分布：  
```math
J(w)=\sum_{s\in S} d_{\pi}(s) (v_{\pi}(S)-\hat{v}_{\pi}(S,w))^2
```
但是后面到迭代公式的时候，这个分布没有给出：  
```math
w_{t+1} = w_t + \alpha_t  (r_{t+1}+\gamma \hat{v}(s_{t+1},w_t) - \hat{v}(s_t,w_t))\nabla_w\hat{v}(s_t,w_t)
```
直接用采样值代替了期望。  
实际上，稳定分布已经包含在里面了。因为智能体是根据策略来行动的，根据行动结果来采样的，而行动本身就收敛到稳定分布，采样也就是按照稳定分布进行的。所以，用采样数据迭代，就是遵循了稳定分布。  

#### 为什么二维的状态向量不行，要加个偏置？
小弟通俗理解是这样的。  
样例里用归一化的坐标代表状态。坐标(0,0)的点，经过$`w_1x+w_2y`$变换后，必等于0，也就意味着(0,0)的状态价值必然是0，无法调节。所以可以加一个偏置，$`w_0 + w_1x+w_2y`$，这样坐标(0,0)能被$`w_0`$调整。  
但我又想，能不能通过截断、归一化之类的，不让(0,0)的输入出现呢？ 我估计这么解也不是不行，但不好。  
这个问题的解决当然有两种思路，一种是调整输入，一种是调整模型。  
如果多项式本身必然经过原点，那就限制了模型的能力，它不能不经过原点，即使有的问题不可能出现经过原点的样本。  
但如果你加一个偏置，那模型的能力就增强了，到底经不经过原点，就靠模型自己去拟合，当$`w_0`$调整到0的时候，它就可以经过原点了，当$`w_0`$不等于0的时候，他就不经过原点了，这由模型根据样本调整，而不是让你在设计模型的时候就直接限制死。  
Deepseek介绍了"问题的自然原点"和"模型的约束原点"两个概念，一下就明白了。不同问题可以有/没有自然原点。但不能约束模型必经过原点，那样模型就无法处理那些没有自然原点的问题了，这就是限制了模型的能力。  

#### 为什么说$`w_{t+1} = w_t + \alpha_t  (r_{t+1}+\gamma \hat{v}(s_{t+1},w_t) - \hat{v}(s_t,w_t))\nabla_w\hat{v}(s_t,w_t)`$没有解$`J(w) = \mathbb{E}[(v_{\pi}(S) - \hat{v}(S,w))^2]`$?
damn，我就说不对劲。  
明明是两个问题，怎么就突然二合一成一个东西了。  
TD法的迭代公式是从RM算法导出的，解决的是状态价值收敛的问题。  
而这里用函数逼近代替表，是从随机梯度下降法导出的，解的是状态价值估计收敛的问题。  
这明明是两个事，虽然公式看着挺像，但怎么稀里糊涂的就合到一个公式里了？  
原来中间确实省略了过程，只能说看着像，缺乏数学上的推导。  
$`w_{t+1} = w_t + \alpha_t  (r_{t+1}+\gamma \hat{v}(s_{t+1},w_t) - \hat{v}(s_t,w_t))\nabla_w\hat{v}(s_t,w_t)`$实际上是新的算法，需要另外的收敛性证明。  

#### $`w_{t+1} = w_t + \alpha_t  (r_{t+1}+\gamma \hat{v}(s_{t+1},w_t) - \hat{v}(s_t,w_t))\nabla_w\hat{v}(s_t,w_t)`$收敛性证明
将$`\hat{v}(s_{t+1},w_t)`$展开后为：  
```math
w_{t+1} = w_t + \alpha_t  (r_{t+1}+\gamma \phi^T(s_{t+1})w_t - \phi^T(s_t)w_t)\phi(s_t)
```
这个公式看着很熟悉，实际上叠加了很多个算法结论。  
首先，迭代式框架来自RM算法。  
用下一状态的估计状态价值代替真实未来折扣奖励，来自TD算法。  
$`(r_{t+1}+\gamma \hat{v}(s_{t+1},w_t) - \hat{v}(s_t,w_t))\nabla_w\hat{v}(s_t,w_t)`$这一大长串的推导，来自针对损失的随机梯度下降法推导。  
最终$`\phi^T(s_t)w_t)`$的代入是对函数逼近的建模。  
这些叠加之后，比较难分析收敛性，所以先退一步，探究确定性算法：  
```math
w_{t+1} = w_t + \alpha_t  \mathbb{E}[(R_{t+1}+\gamma \phi^T(S_{t+1})w_t - \phi^T(S_t)w_t)\phi(S_t)]
```
的收敛性。这个算法实际上去掉了随机性，替换为期望，变成了确定性算法。相当于从随机梯度下降退回到梯度下降。因此，证明了确定性算法的收敛性，再辅以SDG，就可以证明随机算法的收敛性。  
  
定义两个矩阵：  
```math
\Phi = \left[
\begin{array}{c}
\vdots \\
\phi^{T}(s) \\
\vdots \\
\end{array}
\right] \in \mathbb{R}^{n \times m}
```
每个状态对应的向量是$`\phi(s)`$，维度为m,在矩阵中是一行，所以是$`\phi^{T}(s)`$.  
一共n个状态，每个状态一行，所以矩阵是$`n \times m`$。  
所以这个矩阵是集合了所有状态向量。  
```math
D = \left[
\begin{array}{ccc}
\ddots & & \\
& d_{\pi}(s) & \\
& & \ddots \\
\end{array}
\right] \in \mathbb{R}^{n \times n}
```
这个矩阵把状态分布向量转成矩阵。状态分布向量如上所说，有策略和环境决定。  
为什么把向量换成矩阵呢？方便计算。比如$`\Phi^TD`$，$`\Phi`$每行代表一个状态，转置后每列代表一个状态。和$`D`$乘之后，每列代表一个状态乘自己的分布。其实相当于把之前的向量乘拓展成矩阵乘了。  
  
$`\mathbb{E}[(R_{t+1}+\gamma \phi^T(S_{t+1})w_t - \phi^T(S_t)w_t)\phi(S_t)]`$推导。  
这个其实是在迭代过程中，某一步状态的期望计算。其中的$`S_t`$和$`S_{t+1}`$是随机变量，可能是任何一个状态。而状态的概率分布，遵循稳定分布$`d_{\pi}(s)`$  
```math
\begin{align}
&\mathbb{E}[(R_{t+1}+\gamma \phi^T(S_{t+1})w_t - \phi^T(S_t)w_t)\phi(S_t)]\\
&=\sum_{s\in \mathcal{S}}d_{\pi}(s)\mathbb{E}[(R_{t+1}+\gamma \phi^T(S_{t+1})w_t - \phi^T(S_t)w_t)\phi(S_t)|S_t=s]  \\
&=\sum_{s\in \mathcal{S}}d_{\pi}(s)\mathbb{E}[R_{t+1}\phi(S_t)+(\gamma \phi^T(S_{t+1})w_t - \phi^T(S_t)w_t)\phi(S_t)|S_t=s]\\
&=\sum_{s\in \mathcal{S}}d_{\pi}(s)\mathbb{E}[R_{t+1}\phi(S_t)|S_t=s] + \sum_{s\in \mathcal{S}}d_{\pi}(s)\mathbb{E}[(\gamma \phi^T(S_{t+1})w_t - \phi^T(S_t)w_t)\phi(S_t)|S_t=s]
\end{align}
```
拆成两部分继续推导。第一部分可以理解为即时奖励梯度，第二部分可以理解为未来折扣奖励梯度。  
```math
\begin{align}
&\sum_{s\in \mathcal{S}}d_{\pi}(s)\mathbb{E}[R_{t+1}\phi(S_t)|S_t=s]\\
&= \sum_{s\in \mathcal{S}}d_{\pi}(s)\mathbb{E}[R_{t+1}\phi(s)|S_t=s]\\
&= \sum_{s\in \mathcal{S}}d_{\pi}(s)[\phi(s)\sum_{a \in \mathcal{A}}\pi(a|s)\sum_{r \in \mathcal{R}}rp(r|s,a)]\\
&= \sum_{s\in \mathcal{S}}d_{\pi}(s) \phi(s) r_{\pi}(s)\\
&= \Phi^TDr_{\pi}(s)
\end{align}
```
也就是状态乘分布乘奖励。  
```math
\begin{align}
&\mathbb{E}[(\gamma \phi^T(S_{t+1})w_t - \phi^T(S_t)w_t)\phi(S_t)|S_t=s]\\
&=\mathbb{E}[(\gamma \phi^T(S_{t+1})w_t - \phi^T(s)w_t)\phi(s)|S_t=s]\\
&=\mathbb{E}[(\gamma \phi^T(S_{t+1})w_t\phi(s) - \phi^T(s)w_t\phi(s))|S_t=s]\\
&=\mathbb{E}[(\gamma \phi^T(S_{t+1})w_t\phi(s)|S_t=s]-\Phi^Tw_t\Phi\\
&=\sum_{s'\in\mathcal{S}}p(s'|s)\gamma \phi^T(s')w_t\Phi(s) - \Phi^Tw_t\Phi\\
&=P_{\pi}\gamma\Phi^T w_t\Phi- \Phi^Tw_t\Phi\\
&=(\gamma P_{\pi}-1)\Phi^T w_t\Phi
\end{align}
```
再加上稳定分布：  
```math
\begin{align}
&\sum_{s\in \mathcal{S}}d_{\pi}(s)[(\gamma P_{\pi}-1)\Phi^T w_t\Phi]\\
&=D[(\gamma P_{\pi}-1)\Phi^T w_t\Phi]\\
&=(\gamma P_{\pi}-1)w_t\Phi^TD\Phi\\
&=-(1-\gamma P_{\pi})w_t\Phi^TD\Phi\\
&=-\Phi^TD(1-\gamma P_{\pi})\Phi w
\end{align}
```
先对下shape。  
假如状态n个，m维，$`\Phi`$是$`n\times m`$，则
第一部分的shape是:  
```math
\Phi^TDr_{\pi}(s)\\
(m \times n)(n \times n)(n\times 1)=(m\times 1)
```
第二部分的shape是:  
```math
-\Phi^TD(1-\gamma P_{\pi})\Phi w\\
-(m \times n)(n \times n)(n\times n)(n\times m)(m\times1)=-(m\times 1)
```

合并一起：  
```math
\begin{align}
\Phi^TDr_{\pi}(s) -\Phi^TD(1-\gamma P_{\pi})\Phi w\\
= b-Aw
\end{align}
```
推导完毕。我居然也可以自己推导完整证明了。  

继续。  
把结果带入迭代公式:  
```math
w_{k+1} = w_k - \alpha_k (b-Aw_k)
```
假如迭代会收敛，且当$`k\to\infty`$时最终收敛到$`w^*`$，则:
```math
w^* = w^* - \alpha_{\infty} (b - Aw^*)
```
由于$`\alpha`$不会衰减到0，因此  
$`b-Aw=0,b=Aw,A^{-1}b=w^*`$  
  
所以，假如收敛，最后会收敛到$`w^*=A^{-1}b`$  
就说，假如，还是tabular的表示状态价值，看看$`\Phi`$和$`w`$是什么样的。  
w代表状态价值，所以，有几个状态，w维度就是多少。
$`\Phi`$是个矩阵，每行代表一个状态。函数逼近时，用它将状态转为向量。现在是tabular了，不需要转向量。因此相当于是个单位矩阵。单位矩阵乘任何矩阵/向量都是它自己。  
所以：  
```math
\begin{align}
A^{-1}&=[\Phi^TD(1-\gamma P_{\pi})\Phi]^{-1}\\
&=D(1-\gamma P_{\pi})^{-1}\\
&=(1-\gamma P_{\pi}(s))^{-1}D^{-1}

\end{align}
```
```math
b=\Phi^TDr_{\pi}(s)=Dr_{\pi}(s)
```
因此：  
```math
w^*=A^{-1}b=(1-\gamma P_{\pi}(s))^{-1}D^{-1}Dr_{\pi}(s)=(1-\gamma P_{\pi}(s))r_{\pi}(s)
```
理论上没有$`r_{\pi}(s),P_{\pi}(s)`$直接是$`r_{\pi},P_{\pi}`$懒得改了。  
这个就是最开始线代法解贝尔曼方程时候的解，所以，如果是tabular的状态价值，最终会收敛到贝尔曼方程的解。函数逼近法拓展了tabular方法。也可以说tabular方法是函数逼近法的特例。  
  
两种证明法，一种是类似最开始证明贝尔曼方程收敛的方法，只是这里换成了矩阵。  
一种是RM算法。  
```math
w_{k+1} = w_k - \alpha_k (b-Aw_k)
```
可以认为，是求$`g(w)=b-Aw`$的根，这样，以上迭代公式就是RM算法的迭代公式。最终会收敛到根$`g(w)=b-Aw=0`$，也就是$`w^*=A^{-1}b`$。  

#### weighted norm
```math
||x||_D^2=x^TDx=||D^{1/2}x||_2^2
```
范数一般就是衡量矩阵向量长度/大小的方法。  
L2范数其实就是对应标量里的绝对值平方。$`||A||_2^2=A^TA`$  
weighted norm，就是在距离上乘个权重。$`||A||_D^2=A^TDA`$。这个权重作用在平方之后。  
所以式子最后，相当于$`D^{1/2}`$作用在范数之前的$`x`$。  

#### 公式8.13证明思路梳理  
8.13:  
```math
w_{t+1}=w_t + \alpha_t [r_{t+1}+\gamma \hat{v}(s_{t+1},w_t) - \hat{v}(s_t,w_t)]\nabla_w\hat{v}_t(s_t,w_t)
```
是随机梯度下降形式。转为期望形式，这样可以用矩阵表示公式，方便分析。  
$`\hat{v}(s_t,w_t)=\phi(s) w_t`$因此：
```math
w_{t+1}=w_t+\alpha_t\mathbb{E}[(r_{t+1} + \gamma\phi^T(s_{t+1})w_t - \phi^T(s_t)w_t)\phi(s_t)]
```
主要分析这个迭代公式，8.13可以通过上式加随机梯度下降得到。  
上式看作RM算法，就等于求期望部分的根。因此对期望部分用矩阵表示，并化简，得出：  
```math
w_{t+1}=w_t+\alpha_t [b-Aw_t]
```
并得出收敛后根为：  
```math
w^*=A^{-1}b
```
然后证明，公式会收敛。  
依次引出$`J_E(w),J_{BE}(w),J_{PBE}(w)`$的概念，最终证明，$`w^*=A^{-1}b`$就是在解$`\min J_{PBE}(w)`$  

#### $`J_E(w),J_{BE}(w),J_{PBE}(w)`$概念理解
```math
J_E(w)=\mathbb{E}[(\hat{v}(S,w)-v_{\pi}(S))^2]=||\hat{v}(w)-v_{\pi}||_D^2
```
其中$`\hat{v}`$是函数逼近，$`v_{\pi}`$是“理想中”真实的状态价值。损失函数就是最小化两者的方差。其中期望意味着一个状态分布，也就是$`d_{\pi}(s)`$，用矩阵$`D`$表示。  
由于$`v_{\pi}`$是个理想值，真实实现中拿不到，所以用一个估计值代替。估计值就是用贝尔曼方程根据现有值计算出来的值。
贝尔曼方程：  
```math
v_{\pi} = r+\gamma P_{\pi}v_{\pi}
```
也就是：  
```math
J_{BE}(w)=||\hat{v}(w)-(r+\gamma P_{\pi}\hat{v}(w))||_D^2=||\hat{v}(w)-T_{\pi}(\hat{v}(w))||_D^2
```
把贝尔曼方程的转换写为$`T_{\pi}`$算子。  
这个叫贝尔曼error。有啥区别呢？因为用估计值$`(r+\gamma P_{\pi}\hat{v}(w))`$代替了理想的$`v_{\pi}`$，因此，收敛的方向就发生了变化。函数是有偏的了，因为$`(r+\gamma P_{\pi}\hat{v}(w))`$仅是估计值。这个损失很难降到0，因为函数逼近$`\hat{v}`$的能力有限，无法完美拟合。  
因此，拟合的目标需要改变一下。不再拟合理想的$`v_{\pi}`$，而是拟合理想值在函数逼近能触及范围的投影。因此，要加一个投影矩阵$`M`$,就是$`J_{PBE}(w)`$：  
```math
J_{PBE}(w)=||\hat{v}(w)-MT_{\pi}(\hat{v}(w))||_D^2
```  
$`M`$的值，一种思路是根据推导得出。  
书中是直接给出，然后再证明。逻辑略微有点跳跃。  
$`M=\Phi(\Phi^TD\Phi)^{-1}\Phi^TD \in R^{n \times n}`$  
求$`J_{PBE}(w)`$最小时$`w`$的取值，也就是$`J_{PBE}(w)=||\hat{v}(w)-MT_{\pi}(\hat{v}(w))||_D^2=0`$，  
即$`\hat{v}(w)-MT_{\pi}(\hat{v}(w))=0,\hat{v}(w)=MT_{\pi}(\hat{v}(w))`$。  
假设$`\hat{v}(w)=\Phi w`$代入：  
```math
\begin{align}
\Phi w&=MT_{\pi}(\Phi w)\\
\Phi w&=M(r_{\pi}+\gamma P_{\pi}\Phi w)\\
\Phi w&=\Phi(\Phi^TD\Phi)^{-1}\Phi^TD(r_{\pi}+\gamma P_{\pi}\Phi w)\\
w&=(\Phi)^{-1}\Phi(\Phi^TD\Phi)^{-1}\Phi^TD(r_{\pi}+\gamma P_{\pi}\Phi w)\\
w&= (\Phi^TD\Phi)^{-1}\Phi^TD(r_{\pi}+\gamma P_{\pi}\Phi w)\\
&后面的思路是把w系数合一起，好求w\\
(\Phi^TD\Phi)w&=\Phi^TD(r_{\pi}+\gamma P_{\pi}\Phi w)\\
(\Phi^TD\Phi)w&=\Phi^TDr_{\pi}+ \Phi^TD\gamma P_{\pi}\Phi w\\
(\Phi^TD\Phi)w-\Phi^TD\gamma P_{\pi}\Phi w &= \Phi^TDr_{\pi}\\
(\Phi^TD\Phi-\Phi^TD\gamma P_{\pi}\Phi)w&=\Phi^TDr_{\pi}\\
(1-\gamma P_{\pi})\Phi^TD\Phi w&=\Phi^TDr_{\pi}\\
w&= [(1-\gamma P_{\pi})\Phi^TD\Phi]^{-1}\Phi^TDr_{\pi}\\
w&= A^{-1}b
\end{align}
```
因此，$`J_{PBE}(w)`$的解为$`w=A^{-1}b`$。和开始假设的结论一致。  
其实好像也没证明啥。只是通过两条路到达了同一个终点。  
最开始，用线代和贝尔曼方程来推导迭代公式，得出解是$`w^*=A^{-1}b`$的结论。  
这里，是从调整损失函数的角度，来解$`J_{PBE}(w)`$，得出$`w^*=A^{-1}b`$的结论。  
从这个角度，它解释了8.13的本质，它的迭代目标，是真实状态价值在函数逼近空间的投影。通过这种方式，得到了函数逼近能力内的最优解。  

#### 公式8.13收敛后和真实的状态价值差多少  
$`T_{\pi}()`$是贝尔曼算子，所以真实的状态价值$`v_{\pi}`$满足：  
```math
v_{\pi} = r+\gamma P_{\pi}v_{\pi} = T_{\pi}(v_{\pi})
```
估计的状态价值是$`\hat{v}_{\pi}(s)`$,期望（矩阵）形式是：$`\Phi w`$，收敛后为$`\Phi w^*`$,其中$`w^*=A^{-1}b`$上面已经证明了。收敛后的估计状态价值满足：  
```math
\hat{v}_{\pi} = MT_{\pi}(\hat{v}_{\pi})
```
估计的状态价值和真实的状态价值之间有偏差。原因是逼近函数能力有限，所以只能估计真实解的投影。M就是投影矩阵。  
现在就是看看$`v_{\pi}`$和$`\hat{v}_{\pi}`$的差距有多大。  
做差,并展开到线代方程形式。我理解这个思路是，他们分别是在两个方程里收敛的，直接比不太好比。所以取一个中间值来比。  
```math
\begin{align}
&||\hat{v}_{\pi}-v_{\pi}||_D \\
= &||\hat{v}_{\pi}-Mv_{\pi} + Mv_{\pi}-v_{\pi}||_D\\
\leq &||\hat{v}_{\pi}-Mv_{\pi}||_D + ||Mv_{\pi}-v_{\pi}||_D\\
& 上边两个等式代入\\
= &||MT_{\pi}(\hat{v}_{\pi})-MT_{\pi}(v_{\pi})||_D+||Mv_{\pi}-v_{\pi}||_D\\
& 转矩阵形式\\
= &||MT_{\pi}(\Phi w^*)-MT_{\pi}(v_{\pi})||_D+||Mv_{\pi}-v_{\pi}||_D\\
& T_{\pi}再展开\\
= &||M (r_{\pi}+\gamma P_{\pi}\Phi w^*)-M(r_{\pi}+\gamma P_{\pi}v_{\pi})||_D+||Mv_{\pi}-v_{\pi}||_D\\
= &|| \gamma P_{\pi}(\Phi w^*-v_{\pi})||_D + ||Mv_{\pi}-v_{\pi}||_D
\end{align}
```
$`Mv_{\pi}`$的含义我理解是真实状态价值的投影。是个用来证明的人为构造的公式。  
  
后面推导依赖几个结论。  
- $`||ABx||_D \leq ||A||_D||B||_D||x||_D`$  
这块没太懂。什么诱导范数什么的。我来瞎ji…兴理解下  
在向量运算中，这个范数符号$`||a||`$衡量向量的长度。如果是$`||a-b||`$就是衡量两个向量的距离。类似标量里的绝对值。这个衡量的方法在向量界有多种方法，也就是各种范数。什么L2范数、max范数。  
对于矩阵，一种理解是认为矩阵是一个对向量的变换。比如上面的M矩阵，就是对状态价值的投影变换。这个变换理解为对一个向量的"拉伸"，而$`||M||`$就衡量了拉伸的倍数。所以$`||A||=\max_{x \ne 0}\frac{||Ax||}{||x||}`$，也就是说，给你一个向量$`x`$，你最大拉伸多少。如果向量等于0，这个衡量就没意义了，所以要排除掉。  
省略吧先，这个推导需要高阶线代知识。  

#### 整理下思路
本章之前都是tabular形式的，状态价值就是个矩阵，迭代的过程就是不断更新这个矩阵。  
本章引入了函数逼近，矩阵中的值通过函数来得出。这个函数如果是线性的，可以用$`\Phi w`$表示。$`\Phi`$表示状态特征，$`w`$表示参数，合起来可以计算出状态价值。  
迭代公式里的真实折扣奖励，用来引导收敛方向，有两个选择，一个是蒙特卡洛法的采样样本值，一个是TD法的即时奖励+函数逼近估计值。  
后者融合了多种算法，需要进行严格的数学分析。  
分析首先去掉了随机，把采样的迭代公式转成期望，这样可以用矩阵运算，来证明其收敛性。  
函数逼近用线性函数来分析。  
经过对矩阵运算进行分析，发现，这个算法是对状态价值进行了投影，是在优化$`J_{BPE}`$。为了引出$`J_{BPE}`$，分别介绍了$`J_E`$，就是之前的真实状态价值和估计状态价值差平方，然后是$`J_{BE}`$，是把估计状态价值换成贝尔曼方程，也就是之前用函数逼近预估当前状态的未来折扣奖励，改为预估下一状态的状态价值，再加上即时奖励。其实就是TD法的思路。最后是$`J_{BPE}`$，加上了投影矩阵$`M`$。  

#### 发现一个点
在加入函数逼近之前，各个状态的迭代公式是分离的，各迭代各的，每个状态的奖励只往自己的状态价值迭代公式里带。而加入函数逼近之后，发现迭代公式里不区分状态了，不管你是哪个状态的都往一个迭代公式迭代。也就是所有状态价值的收敛都合在一个迭代公式里了，所以它其实包含了两层收敛，一个是状态价值的收敛，一个是函数逼近的收敛。  

#### 8.13是以MSE构建的，谁都可以当目标
意识到，8.13的基本是以MSE加随机梯度下降构建的，就是迭代法逼近一个目标。至于这个目标是谁，是可以换的。  
听着好像是废话，但是一瞬间有一点悟了的感觉。这个公式杂糅的东西太多了，从哪个方向理解都有新感觉。  
  
#### 为什么在Linear-TD里，状态价值里包含了$`w`$，却没有求导。而Deep-Q-learning里，行动价值里带有$`w`$却要单独处理？  
来自deepseek的解释的理解。  
Linear-TD里没有$`\max`$算子，目标是稳定的。Deep-Q里求的是最优贝尔曼方程，引入了$`\max`$算子，目标会随着$`w`$迭代跳变，从而变的不稳定。所以这块的梯度需要特殊处理。  
其实按照TD的理解，公式里一个是估计的目标，其中部分值也是估计的；一个是当前行动价值的估计值。目标是可能跳变的。所以这两个的估计分成两个模型。目标那个模型降低更新频率。这样就类似：先定住一个目标走一阵，然后更新到更优的目标，再继续迭代。直到收敛。
  
#### 稳定分布
前面提到了多次稳定分布$`d_{\pi}`$，但在实际解决问题时又没有了$`d_{\pi}`$。  
平稳分布d_{\pi}由策略和状态转移概率确定。在公式上可以运算、分析。但实际任务中无法获得状态转移概率，也就无法通过d_{\pi}来计算状态价值。实际上是用的蒙特卡洛法/TD法，对采样状态价值求平均得来的。由于样本是智能体行动获取到的，所以分布就是稳定分布。  

#### $`\bar{v}_{\pi}`$推导
策略梯度法里，对策略建模，目标是最大化状态价值。  
这里$`\bar{v}_{\pi}`$是建模的目标。所有状态的状态价值平均值。  
两种平均权重，一种是所有状态同权平均，一种是按照稳定分布$`d_{\pi}`$加权平均。  
也就是：  
$`\mathbb{E}[v_{\pi}]=\sum_{s\in\mathcal{S}}d_{\pi}(s)v_{\pi}(s)`$  
这个$`\mathbb{E}`$的对象是状态$`s`$，所以要按照$`s`$展开。  
书里是先给了个结论，然后反推到上式，有点迷惑。特别是那个公式猛的一看就容易懵逼。这里正着推导一下  
$`v_{\pi}(s)`$等于啥？按照本书一开始的定义，等于从状态$`s`$起即时奖励和未来折扣奖励和的期望  
```math
v_{\pi}(s) = \mathbb{E}[R_t(s)+\gamma G_{t+1}] = \mathbb{E}[R_t(s)+\gamma R_{t+1}(s')+ \gamma^2 R_{t+2}(s'') + \gamma^3 R_{t+3}(s''')....]
```
注意，这个公式是一种“回合”的视角，后面的R都是回合中后面经过的状态产生的奖励，经过折扣后，累加到当前状态$`s`$上。  
代入后：  
```math
\begin{align}
\mathbb{E}[v_{\pi}]&=\sum_{s\in\mathcal{S}}d_{\pi}(s)v_{\pi}(s)\\
&= \sum_{s\in\mathcal{S}}d_{\pi}(s)\mathbb{E}[R_t(s)+\gamma R_{t+1}(s')+ \gamma^2 R_{t+2}(s'') +...|S_0=s]\\
& 注意，这个\mathbb{E}是选中某个状态后，对应状态的期望\\
& 把所有从状态s开始的时间步的奖励通过\sum统一起来\\
&= \sum_{s\in\mathcal{S}}d_{\pi}(s)\mathbb{E}[\sum_{t=0}^\infty[\gamma^tR_{t+1}]|S_0=s]
\end{align}
```
这个公式理解起来，着实有点费劲哦。特别是$`\mathbb{E}[\sum_{t=0}^\infty[\gamma^tR_{t+1}]|S_0=s]`$。这个$`\mathbb{E}`$是奖励$`R`$的期望。公式说的是，从状态$`s`$起后续所有折扣奖励和。这其实就是状态价值的定义，不知道为啥换了个$`\sum`$的形式一下就懵逼了。  

#### 平均reward $`\bar{r}_{\pi}`$
```math
\bar{r}_{\pi}=\sum_{s\in\mathcal{S}}d_{\pi}(s)r_{\pi}(s)=\mathbb{E}_{S - d_{\pi}}[r_{\pi}(S)]
```
是个针对状态的期望。所以展开是状态的分布乘该状态在策略$`\pi`$得到的奖励。  
而奖励：
```math
r_{\pi}(s)=\sum_{a\in\mathcal{A}}\pi(a|s,\theta)r(s,a)=\mathbb{E}_{A-\pi(a|s,\theta)}[r(s,A)|S=s]
```
在状态$`s`$下，逼近函数是$`\pi(s,\theta)`$，其中$`\theta`$就是逼近函数的可调参数。输入状态$`s`$进去就会输出行动的概率分布，根据概率随机选择一个行动。当然，也可能直接输出行动$`a`$，但总之是有个概率分布的。这里公式的意思就是，奖励也是个期望，需要承上概率分布。

目标函数：  
```math
J(\theta) = \lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}]
```
$`\sum_{t=0}^{n-1}R_{t+1}`$就是智能体从时刻$`t=0`$开始行动，每步在不同状态获取的即时奖励，加和。外层的$`\mathbb{E}`$，可以有不同展开。一方面这个过程经过了不同的状态，所以可以按照状态的概率分布展开，值就是每个状态获得的奖励。一方面可以按照(s,a)展开。总之它是个期望。外层$`\lim_{n\to\infty}\frac{1}{n}`$代表总步数的奖励平均。  
按书上说法，$`J(\theta) = \lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}]=\sum_{s\in\mathcal{S}}d_{\pi}(s)r_{\pi}(s)=\bar{r}_{\pi}`$。  

#### 定义策略梯度法损失函数，为什么整出两个奇葩公式，还要证明？  
状态价值平均的公式：  
```math
J(\theta)=\lim_{n\to\infty}\mathbb{E}[\sum_{t=0}^{n}\gamma^tR_{t+1}]=\sum_{s\in\mathcal{S}}d_{\pi}(s)v_{\pi}(s)
```
奖励平均的公式：  
```math
J(\theta)=\lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}]=\sum_{s\in\mathcal{S}}d_{\pi}(s)r_{\pi}(s)
```
就中间这个东西，给我搞"抑郁"了。有点突然，脱离了之前的连续推导。  
书里两个公式的推导也不一样。对于前者，是从后往前推，对于后者，是从前往后推。确实，对于状态价值，由于前面已经讲过稳定分布，所以$`\sum_{s\in\mathcal{S}}d_{\pi}(s)v_{\pi}(s)`$比较熟悉，所以从它开始往前推。对于奖励平均的公式，"求所有奖励和的平均"这个概念更好理解一些，所以$`\lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}]`$比较容易理解。但这种极限形式，无法求导。所以要转成$`\sum_{s\in\mathcal{S}}d_{\pi}(s)r_{\pi}(s)`$的形式。这个转换不太直观，所以多了一层推导。  
  
这个公式还是让我迷惑，再展开下看看。  
```math
\begin{align}
J(\theta)&=\lim_{n\to\infty}\mathbb{E}[\sum_{t=0}^{n}\gamma^tR_{t+1}]\\
&=\mathbb{E}[\sum_{t=0}^{\infty}\gamma^tR_{t+1}]\\
&=\mathbb{E}[R_{1}+\gamma R_{2}+\gamma^2 R_{3} + \gamma^3 R_{4}...\gamma^t R_{t+1}]
\end{align}
```
这猛一看很像是第一个状态$`s_0`$的状态价值。但仔细一看，确实就是第一个状态的状态价值。  
不过，据说，这个期望有两层随机，一个是遵循策略$`\pi`$随机选择动作。一个是初始状态$`s_0`$的选择也是随机的。所以它的含义是随机选择一个状态起始，按照策略$`\pi`$行动，得到的状态价值期望。优化这个目标，就是让在任意状态起步得到的状态价值最高。这不就是最优贝尔曼方程吗？！  

再看平均奖励的公式：  
```math
J(\theta)=\lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}]=\sum_{s\in\mathcal{S}}d_{\pi}(s)r_{\pi}(s)
```
发现一点，不管是上面平均状态价值，还是这里平均奖励，中间都是个极限，但最后转成了固定值。这就是为什么都需要证明。证明其实就是说，最终会趋于一个稳定分布，这种情况下目标也会收敛到一个固定值。所以公式里的极限符号最后被稳定分布$`d_{\pi}`$给取代了。  
所谓证明，就是在证明为什么一个无限长的序列最终可以转为一个固定的矩阵。  

#### 平均奖励证明  
证明：  
```math
\lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}]=\sum_{s\in\mathcal{S}}d_{\pi}(s)r_{\pi}(s)
```
核心点就在于前边公式的极限是怎么转换成后边稳定分布的？  
首先，这个期望包含两层随机，所以先去掉一层起始点的随机，也就是选定一个固定起始点$`s_0`$，先证明：  
```math
\lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}|S_0=s_0]=\sum_{s\in\mathcal{S}}d_{\pi}(s)r_{\pi}(s)
```
推导：  
```math
\begin{align}
&\lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}|S_0=s_0]\\
&=\lim_{n\to\infty}\frac{1}{n}\sum_{t=0}^{n-1}\mathbb{E}[R_{t+1}|S_0=s_0]\\
&=\lim_{n\to\infty}\frac{1}{n}\{\mathbb{E}[R_{1}|S_0=s_0]+\mathbb{E}[R_{2}|S_0=s_0]+\mathbb{E}[R_{3}|S_0=s_0]+....\mathbb{E}[R_{n}|S_0=s_0]\}\\
\end{align}
```
可以看出来，其实这是个序列。  
这用到了一个什么切萨洛平均：
如果序列$`\{a_k\}_1^\infty`$是收敛的，且$`\lim_{k\to\infty}a_k`$存在。  
则$`\{\frac{1}{n}\sum_{k=1}^{n}a_k\}_{n=1}^{\infty}`$也是收敛的，  
且$`\lim_{n\to\infty}\frac{1}{n}\sum_{k=1}^{n}a_k=\lim_{k\to\infty}a_k`$。  
用大直白话讲一遍。就是说一个序列如果是收敛的，最后会收敛到一个值。这时候，这个序列的均值序列也是收敛的，收敛值和原序列一致。  
套用到上面的公式里，当然还少了个序列收敛性证明：  
```math
\begin{align}
&\lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}|S_0=s_0]\\
&=\lim_{n\to\infty}\frac{1}{n}\{\mathbb{E}[R_{1}|S_0=s_0]+\mathbb{E}[R_{2}|S_0=s_0]+\mathbb{E}[R_{3}|S_0=s_0]+....\mathbb{E}[R_{n}|S_0=s_0]\}\\
&= \lim_{n\to\infty}\mathbb{E}[R_{n}|S_0=s_0]\\
&=\lim_{t\to\infty}\mathbb{E}[R_{t+1}|S_0=s_0]
\end{align}
```
也就是说收益期望最后会收敛到一个稳定值。  
继续看$`\mathbb{E}[R_{t+1}|S_0=s_0]`$，只说是个期望，期望的概率有很多种分解方式。这个公式里，$`R_{t+1}`$是第$`t+1`$步得到的，条件$`S_0=s_0`$却是第1步，需要构建起他们之间的联系。  
```math
\begin{align}
&\mathbb{E}[R_{t+1}|S_0=s_0] \\
& 全概率公式展开\\
&= \sum_{s\in\mathcal{S}}\mathbb{E}[R_{t+1}|S_0=s_0,S_t=s_t]p^{(t)}(s_t|s_0)\\
& 马尔科夫性，状态转移无关,也就是跳到s_t和s_0没什么关系\\
&= \sum_{s\in\mathcal{S}}\mathbb{E}[R_{t+1}|S_t=s_t]p^{(t)}(s_t|s_0)\\
& 前面的期望，不就是在状态s_t时获取奖励的期望吗，就是r_{\pi}(s_t)\\
&= \sum_{s\in\mathcal{S}}r_{\pi}(s_t)p^{(t)}(s_t|s_0)\\
& 后边的概率，就是状态转移概率，会趋于稳定分布d_{\pi}\\
&\lim_{t\to\infty}p^{(t)}(s_t|s_0)=d_{\pi}(s_t)\\
&因此\\
&\mathbb{E}[R_{t+1}|S_0=s_0]=\sum_{s\in\mathcal{S}}r_{\pi}(s_t)d_{\pi}(s_t)=\bar{r}_{\pi}
\end{align}
```
综上：  
```math
\lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}|S_0=s_0]=\sum_{s\in\mathcal{S}}d_{\pi}(s)r_{\pi}(s)=\bar{r}_{\pi}
```
然后是处理初始状态。按照全概率公式，用初始状态做条件：  
```math
\begin{align}
&\lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}]\\
&=\lim_{n\to\infty}\frac{1}{n}\sum_{s\in\mathcal{S}}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}|S_0=s]\\
&= \sum_{s\in\mathcal{S}}\lim_{n\to\infty}\frac{1}{n}\mathbb{E}[\sum_{t=0}^{n-1}R_{t+1}|S_0=s]\\
&= \sum_{s\in\mathcal{S}}\sum_{s\in\mathcal{S}}d_{\pi}(s)r_{\pi}(s)\\
&= \sum_{s\in\mathcal{S}}d_{\pi}(s)r_{\pi}(s)\\
&= \bar{r}_{\pi}
\end{align}
```
得证。  
说了这么多，其实就一个，长期会趋于稳定分布。  

#### $`\bar{v}_{\pi}`$和$`\bar{v}_{\pi}^0`$有什么区别？  
这涉及，任务的起始状态该怎么选。  
公式推导中，都是用的稳定分布$`d_{\pi}`$，但$`d_{\pi}`$不是一个真实可获取的值，是一个经过长期迭代后逐渐稳定的值。所以起始状态，在实际上很难用稳定分布来选。  
稳定分布是说，选中某个状态的概率分布。  
当起始状态的选择没有按照稳定分布来选的时候，就是和稳定分布独立了。这个起始的状态分布用$`d_0`$表示，此时$`d_0 \ne d_{\pi}`$。在这种起始分布下长期迭代，计算出来的平均状态价值就是$`\bar{v}_{\pi}^0`$。  
如果$`d_0 = d_{\pi}`$，计算出来的平均状态价值就是$`\bar{v}_{\pi}`$。  
我开始还有个疑问，真实情况下，不可能一开始就得到$`d_{\pi}`$啊，它是个长期迭代稳定后的分布，所以没有一个任务不是从$`d_0\ne d_{\pi}`$开始的啊。这就是实际和理论的差异了。理论分析的是$`\bar{v}_{\pi}`$，但实际任务运行时，得到的都是$`\bar{v}_{\pi}^0`$，所以才要区分这两个公式。需要论证，即使初始状态分布和稳定分布不一致，也能找到最优答案，以及和理想状态的差距是多少。  

#### 策略梯度法公式期望表示
$`J(\theta)`$的梯度为：  
```math
\begin{align}
\nabla_\theta J(\theta) &= \sum_{s\in\mathcal{S}}\mu(s)\sum_{a\in\mathcal{A}}\nabla_{\theta}\pi(a|s,\theta)q_{\pi}(s,a)\\
&=\mathbb{E}_{\mathcal{S}-\mu}[\sum_{a\in\mathcal{A}}\nabla_{\theta}\pi(a|S,\theta)q_{\pi}(S,a)]
\end{align}
```
把状态分布$`\mu(s)`$转为期望。  
下一步的思路是想把这个$`\sum_{a\in\mathcal{A}}`$去掉，换成期望。可是里边的$`\nabla_{\theta}\pi(a|s,\theta)`$是个梯度形式，不是概率分布形式。所以需要转换一下：  
```math
\begin{align}
\nabla_{\theta} \ln \pi(a|s,\theta)&=\frac{\nabla_{\theta}\pi(a|s,\theta)}{\pi(a|s,\theta)}\\
\pi(a|s,\theta) \nabla_{\theta} \ln \pi(a|s,\theta) &= \nabla_{\theta}\pi(a|s,\theta)
\end{align}
```
因此代入前式：  
```math
\begin{align}
\nabla_\theta J(\theta) &= \sum_{s\in\mathcal{S}}\mu(s)\sum_{a\in\mathcal{A}}\nabla_{\theta}\pi(a|s,\theta)q_{\pi}(s,a)\\
&=\mathbb{E}_{\mathcal{S}-\mu}[\sum_{a\in\mathcal{A}}\nabla_{\theta}\pi(a|S,\theta)q_{\pi}(S,a)]\\
&=\mathbb{E}_{\mathcal{S}-\mu}[\sum_{a\in\mathcal{A}}\pi(a|S,\theta) \nabla_{\theta} \ln \pi(a|S,\theta)q_{\pi}(S,a)]\\
&=\mathbb{E}_{\mathcal{S}-\mu,\mathcal{A}-\pi(s,\theta)}\nabla_{\theta} \ln \pi(a|S,\theta)q_{\pi}(S,A)]
\end{align}
```
这样就变换为了期望形式。期望形式有一个好处，就是方便利用蒙特卡洛法。

#### $`\bar{v}_{\pi}`$和$`\bar{r}_{\pi}`$的等价性  
$`v_{\pi}`$和$`r_{\pi}`$的定义：  
```math
\begin{align}
\bar{v}_{\pi} = d_{\pi}^T v_{\pi}\\
\bar{r}_{\pi} = d_{\pi}^T r_{\pi}
\end{align}
```
而$`v_{\pi}`$和$`r_{\pi}`$满足贝尔曼方程(注意，是$`v_{\pi}`$满足贝尔曼方程，而不是$`\bar{v}_{\pi}`$)：
```math
\begin{align}
v_{\pi} &= r_{\pi} + \gamma P_{\pi}v_{\pi}\\
d_{\pi}^T v_{\pi}&= d_{\pi}^T(r_{\pi} + \gamma P_{\pi}v_{\pi})\\
\bar{v}_{\pi} &= \bar{r}_{\pi} + \gamma d_{\pi}^TP_{\pi}v_{\pi}\\
d_{\pi}^T&稳定分布定义： d_{\pi}^T = d_{\pi}^T P_{\pi}\\
\bar{v}_{\pi} &= \bar{r}_{\pi} + \gamma d_{\pi}^Tv_{\pi}\\
\bar{v}_{\pi} &= \bar{r}_{\pi} + \gamma \bar{v}_{\pi}\\
(1-\gamma)\bar{v}_{\pi} &= \bar{r}_{\pi}
\end{align}
```
没太搞明白这个等式的含义。  

#### $`v_{\pi}(s)`$的梯度  
根据定义：  
```math
v_{\pi}(s) = \sum_{a\in\mathcal{A}} \pi(a|s,\theta)q_{\pi}(s,a)
```
因此：  
```math
\nabla_{\theta} v_{\pi}(s) = \nabla_{\theta} [\sum_{a\in\mathcal{A}} \pi(a|s,\theta)q_{\pi}(s,a)]
```
$`q_{\pi}(s,a)`$里其实还包含了下一状态的状态价值，所以也是$`\theta`$的函数：  
```math
\begin{align}
\nabla_{\theta} v_{\pi}(s) &= \nabla_{\theta} [\sum_{a\in\mathcal{A}} \pi(a|s,\theta)q_{\pi}(s,a)]\\
&= \sum_{a\in\mathcal{A}}[\nabla_{\theta} (\pi(a|s,\theta)q_{\pi}(s,a))]\\
&= \sum_{a\in\mathcal{A}}[q_{\pi}(s,a)\nabla_{\theta}\pi(a|s,\theta) + \pi(a|s,\theta) \nabla_{\theta}q_{\pi}(s,a)]\\
&= \sum_{a\in\mathcal{A}}q_{\pi}(s,a)\nabla_{\theta}\pi(a|s,\theta) + \sum_{a\in\mathcal{A}}\pi(a|s,\theta) \nabla_{\theta}q_{\pi}(s,a)
\end{align}
```
继续展开$`q_{\pi}(s,a)`$:  
```math
q_{\pi}(s,a) = r_{\pi}(s,a) + \gamma \sum_{s'\in\mathcal{S}}p(s'|s,a)v_{\pi}(s')
```
其中$`r_{\pi}(s,a)=\sum_{r\in\mathcal{R}}p(r|s,a)r`$，和$`\theta`$无关。所以：  
```math
\begin{align}
\nabla_{\theta}q_{\pi}(s,a) &= \nabla_{\theta} r_{\pi}(s,a) + \gamma \nabla_{\theta} \sum_{s'\in\mathcal{S}}p(s'|s,a)v_{\pi}(s')\\
&= 0 + \gamma \sum_{s'\in\mathcal{S}}p(s'|s,a)\nabla_{\theta}v_{\pi}(s')\\
&= \gamma \sum_{s'\in\mathcal{S}}p(s'|s,a)\nabla_{\theta}v_{\pi}(s')
\end{align}
```
代入上式：  
```math
\begin{align}
\nabla_{\theta} v_{\pi}(s) &= \sum_{a\in\mathcal{A}}q_{\pi}(s,a)\nabla_{\theta}\pi(a|s,\theta) + \sum_{a\in\mathcal{A}}\pi(a|s,\theta) \nabla_{\theta}q_{\pi}(s,a)\\
&= \sum_{a\in\mathcal{A}}q_{\pi}(s,a)\nabla_{\theta}\pi(a|s,\theta) + \gamma \sum_{a\in\mathcal{A}}\pi(a|s,\theta)\sum_{s'\in\mathcal{S}}p(s'|s,a)\nabla_{\theta}v_{\pi}(s')
\end{align}
```
简化一下公式：  
```math
u(s)=\sum_{a\in\mathcal{A}}q_{\pi}(s,a)\nabla_{\theta}\pi(a|s,\theta)
```
```math
\sum_{a\in\mathcal{A}}\pi(a|s,\theta)\sum_{s'\in\mathcal{S}}p(s'|s,a)\nabla_{\theta}v_{\pi}(s') = \sum_{s'\in\mathcal{S}}p(s'|s)\nabla_{\theta}v_{\pi}(s') = \sum_{s'\in\mathcal{S}}[P_{\pi}]_{ss'}\nabla_{\theta}v_{\pi}(s')
```
其中$`P_{\pi}`$是个矩阵，如果状态有n个，矩阵就是$`n \times n`$的。而$`[P_{\pi}]_{ss'}`$是矩阵中位于$`(s,s')`$的那个元素，是个标量。$`v_{\pi}`$是个n维的向量，其中的每个元素代表一个状态的状态价值，所以$`v_{\pi}(s')`$是向量中的一个元素，标量。假设$`\theta`$是m维的，那$`\nabla_{\theta} v_{\pi}`$是$`m \times n`$维的，每个状态$`s`$对$`\theta`$中每一维都有一个梯度分量。而$`\nabla_{\theta} v_{\pi}(s')`$就是矩阵中的一个向量，是$`m`$维列向量。因此，$`\sum_{s'\in\mathcal{S}}[P_{\pi}]_{ss'}\nabla_{\theta}v_{\pi}(s')`$整个式子最后得出一个m维向量。  
再看$`u(s)`$。假设动作有$`k`$个，则$`\pi(a|s)`$是一个$`n \times k`$的矩阵。每个元素在求梯度时都会产生一个$`\theta`$上的分量，则$`\nabla_{\theta}\pi(a|s,\theta)`$是$`n\times k\times m`$维的矩阵。选定某个动作后，切出$`n \times m`$的矩阵。$`q_{\pi}`$是$`n \times k`$的，选中某个动作后切出$`n`$维行向量。因此，选定某个动作后$`q_{\pi}(s,a)\nabla_{\theta}\pi(a|s,\theta)`$为$`1 \times n * n times m= 1 \times m`$的向量。  
把两式代入，得出：  
```math
\nabla_{\theta} v_{\pi}(s) = u(s) + \sum_{s'\in\mathcal{S}}[P_{\pi}]_{ss'}\nabla_{\theta}v_{\pi}(s')
```
最终得到的也是一个$`m`$维向量，shape对得上。  
```math
\underbrace{
\left[\begin{array}{c}
\vdots \\
\nabla_{\theta} v_{\pi}(s) \\
\vdots \\
\end{array}\right]
}_{\substack{\text{$\nabla_{\theta} v_{\pi} \in \mathbb{R}^{mn}$}}}
=
\underbrace{
\left[\begin{array}{c}
\vdots \\
u(s) \\
\vdots \\
\vdots
\end{array}\right]
}_{\substack{u \in \mathbb{R}^{mn}}}
+ \gamma (P_{\pi} \otimes I_{m})
\underbrace{
\left[\begin{array}{c}
\vdots \\
\nabla_{\theta} v_{\pi}(s') \\
\vdots \\
\vdots
\end{array}\right]
}_{\substack{\nabla_{\theta} v_{\pi} \in \mathbb{R}^{mn}}}
```
再看下转成矩阵形式。  
$`P_{\pi}`$是$`n \times n`$的，$`I_m`$是$`m \times m`$的单位矩阵。中间的克罗内克积会用$`P_{\pi}`$中每个元素乘单位矩阵$`I_m`$。也就是原来矩阵的一个元素变成了一个$`m \times m`$矩阵。因此$`P_{\pi} \otimes I_{m}`$后shape为$`nm \times nm`$的。  
按照上面的分析$`\nabla_{\theta} v_{\pi}`$是$`n \times m`$的，但是公式中是$`nm`$的，因为被做了向量化，摊平了。也就是向量中每m个元素对应一个状态。所以上面公式中$`\nabla_{\theta} v_{\pi}`$是$`nm \times 1`$的。和$`P_{\pi} \otimes I_m`$乘，结果为$`nm \times nm * nm \times 1=nm \times 1`$。  
这理解起来其实有点晦涩，主要是克罗内克积和向量化。其实没有这两个，shapey一样对得上。假如$`\nabla_{\theta} v_{\pi}`$是个$`n\times m`$的二维矩阵，而$`P_{\pi}`$是个$`n \times n`$的矩阵，相乘得$`n \times m`$的矩阵，而且含义也挺清晰。且那边的$`u`$也是一个$`n \times m`$的矩阵，维度都对得上。  
但是如果$`\nabla_{\theta} v_{\pi}`$要向量化，那就必须加一个克罗内克积，让维度对齐了，其实含义没变。  
  
总之，可以简写为：  
```math
\nabla_{\theta} v_{\pi} = u + \gamma (P_{\pi} \otimes I_m)\nabla_{\theta} v_{\pi}
```
可以解出$`\nabla_{\theta}v_{\pi}`$:  
```math
\begin{align}
\nabla_{\theta} v_{\pi} &= u + \gamma (P_{\pi} \otimes I_m)\nabla_{\theta} v_{\pi} \\
\nabla_{\theta} v_{\pi} - \gamma (P_{\pi} \otimes I_m)\nabla_{\theta} v_{\pi} &= u\\
(I_{nm} - \gamma (P_{\pi} \otimes I_m))\nabla_{\theta}v_{\pi} &= u\\
\nabla_{\theta}v_{\pi} &= [I_{nm} - \gamma (P_{\pi} \otimes I_m)]^{-1}u\\
\nabla_{\theta}v_{\pi} &= [I_n \otimes I_m - \gamma (P_{\pi} \otimes I_m)]^{-1}u \\
\nabla_{\theta}v_{\pi} &= [(I_n - \gamma P_{\pi}) \otimes I_m]^{-1}u\\
\nabla_{\theta}v_{\pi} &= [(I_n - \gamma P_{\pi})^{-1} \otimes I_m]u
\end{align}
```
针对某个状态$`s`$再展开：  
```math
\begin{align}
\nabla_{\theta}v_{\pi}(s) &= \sum_{s'\in\mathcal{S}}[I_n - \gamma P_{\pi}]^{-1}_{ss'} u(s')\\
&= \sum_{s'\in\mathcal{S}}[I_n - \gamma P_{\pi}]^{-1}_{ss'}\sum_{a\in\mathcal{A}}q_{\pi}(s',a)\nabla_{\theta}\pi(a|s',\theta)
\end{align}
```
根据诺伊曼级数定理，对于一个方阵A，如果其谱半径（所有特征值的最大绝对值）小于1，那么矩阵$`I-A`$是可逆的，并且其逆矩阵可以表示为无穷级数：$`(I-A)^{-1}=I+A+A^2+A^3+...`$。因此：  
```math
\begin{align}
[I_n - \gamma P_{\pi}]^{-1}_{ss'} &= I_n + \gamma P_{\pi} + \gamma^2P_{\pi}^2 +...\\
&= \sum_{k=0}^{\infty} [\gamma ^k P_{\pi}^k]_{ss'} \\
&= \mathrm{Pr}_{\pi}(s'|s)
\end{align}
```
因此，公式也可以写为：  
```math
\begin{align}
\nabla_{\theta}v_{\pi}(s) &= \sum_{s'\in\mathcal{S}}\sum_{k=0}^{\infty} [\gamma ^k P_{\pi}^k]_{ss'}\sum_{a\in\mathcal{A}}q_{\pi}(s',a)\nabla_{\theta}\pi(a|s',\theta)\\
&= \sum_{s'\in\mathcal{S}}\mathrm{Pr}_{\pi}(s'|s)\sum_{a\in\mathcal{A}}q_{\pi}(s',a)\nabla_{\theta}\pi(a|s',\theta)
\end{align}
```
至此，第一步，对$`v_{\pi}(s)`$求梯度，完成了。  

#### $`\bar{v}_{\pi}^0(s)`$的梯度  
$`\bar{v}_{\pi}^0(s)`$的意思是，回合开始收个状态的选择的分布是$`d_0`$，而不是$`d_{\pi}`$。选择好初始状态后，后面的状态分布，由于是策略$`\pi`$和环境概率分布决定的，因此是$`d_{\pi}`$。因此：  
```math
\begin{align}
\bar{v}_{\pi}^0(s) &= \sum_{s\in\mathcal{S}} d_0(s)v_{\pi}(s)\\
\nabla_{\theta}\bar{v}_{\pi}^0(s)&=\nabla_{\theta}\sum_{s\in\mathcal{S}} d_0(s)v_{\pi}(s)\\
& d_0(s)和\theta无关，所以\\
&= \sum_{s\in\mathcal{S}} d_0(s)\nabla_{\theta}v_{\pi}(s)
\end{align}
```
后者在上面第一步已经证明过了，可以直接代入：  
```math
\begin{align}
\nabla_{\theta}\bar{v}_{\pi}^0(s) &= \sum_{s\in\mathcal{S}} d_0(s)\nabla_{\theta}v_{\pi}(s)\\
&= \sum_{s\in\mathcal{S}}d_0(s) \sum_{s'\in\mathcal{S}}\mathrm{Pr}_{\pi}(s'|s)\sum_{a\in\mathcal{A}}q_{\pi}(s',a)\nabla_{\theta}\pi(a|s',\theta)\\
&= \sum_{s'\in\mathcal{S}} [\sum_{s\in\mathcal{S}}d_0(s) \mathrm{Pr}_{\pi}(s'|s)] \sum_{a\in\mathcal{A}}q_{\pi}(s',a)\nabla_{\theta}\pi(a|s',\theta)\\
&= \sum_{s'\in\mathcal{S}} \rho_{\pi}(s')\sum_{a\in\mathcal{A}}q_{\pi}(s',a)\nabla_{\theta}\pi(a|s',\theta)\\
& s'替换成s，反正都是遍历所有的状态\\
&= \sum_{s\in\mathcal{S}} \rho_{\pi}(s)\sum_{a\in\mathcal{A}}q_{\pi}(s,a)\nabla_{\theta}\pi(a|s,\theta)\\
& 由于\nabla_{\theta}\ln \pi(a|s,\theta) = \frac{\nabla_{\theta}\pi(a|s,\theta)}{\pi(a|s,\theta)}\\
&= \sum_{s\in\mathcal{S}} \rho_{\pi}(s)\sum_{a\in\mathcal{A}}q_{\pi}(s,a)\pi(a|s,\theta)\nabla_{\theta}\ln \pi(a|s,\theta)\\
&= \sum_{s\in\mathcal{S}} \rho_{\pi}(s)\sum_{a\in\mathcal{A}}\pi(a|s,\theta)q_{\pi}(s,a)\nabla_{\theta}\ln \pi(a|s,\theta)\\
& 去掉概率分布，改成期望的形式\\
&= \mathbb{E}[q_{\pi}(S,A)\nabla_{\theta}\ln \pi(A|S,\theta)]
\end{align}
```
状态$`S`$遵循$`\rho_{\pi}`$，行动$`A`$遵循$`\pi(s,\theta)`$。  

#### $`\bar{v}_{\pi}(s)`$的梯度
```math
\begin{align}
\nabla_{\theta}\bar{v}_{\pi} &= \nabla_{\theta}\sum_{s\in\mathcal{S}} d_{\pi}(s) v_{\pi}(s)\\
&= \sum_{s\in\mathcal{S}} \nabla_{\theta}d_{\pi}(s)v_{\pi}(s) + \sum_{s\in\mathcal{S}} d_{\pi}(s)\nabla_{\theta}v_{\pi}(s)
\end{align}
```
后半部分$`\sum_{s\in\mathcal{S}} d_{\pi}(s)\nabla_{\theta}v_{\pi}(s)`$转为矩阵形式。$`d_{\pi}`$是$`n \times 1`$的，$`\nabla_{\theta}v_{\pi}(s)`$是$` nm \times 1`$的，所以还得克什么什么积转一下：  
```math
\begin{align}
\sum_{s\in\mathcal{S}} d_{\pi}(s)\nabla_{\theta}v_{\pi}(s) &= (d_{\pi}^T \otimes I_m) \nabla_{\theta}v_{\pi}\\
& 代入\nabla_{\theta}v_{\pi}\\
&= (d_{\pi}^T \otimes I_m) [(I_n - \gamma P_{\pi})^{-1} \otimes I_m]u\\
&= [d_{\pi}^T(I_n - \gamma P_{\pi})^{-1}]\otimes I_m u
\end{align}
```
```math
\begin{align}
d_{\pi}^T(I_n - \gamma P_{\pi})^{-1}&=\frac{1}{1-\gamma}d_{\pi}^T\\
d_{\pi}^T &= \frac{1}{1-\gamma}d_{\pi}^T(I_n - \gamma P_{\pi})\\
(1-\gamma)d_{\pi}^T &= d_{\pi}^T(I_n - \gamma P_{\pi})\\
(1-\gamma)d_{\pi}^T &= d_{\pi}^T - \gamma d_{\pi}^TP_{\pi}\\
& 由于d_{\pi}^T=d_{\pi}^TP_{\pi}，所以\\
(1-\gamma)d_{\pi}^T &= d_{\pi}^T - \gamma d_{\pi}^T
\end{align}
```
得证，所以代入上式：  
```math
\begin{align}
\sum_{s\in\mathcal{S}} d_{\pi}(s)\nabla_{\theta}v_{\pi}(s)
&= [d_{\pi}^T(I_n - \gamma P_{\pi})^{-1}]\otimes I_m u\\
&= \frac{1}{1-\gamma}d_{\pi}^T\otimes I_m u\\
&= \frac{1}{1-\gamma}\sum_{s\in\mathcal{S}}d_{\pi}(s)\sum_{a\in\mathcal{A}}q_{\pi}(s,a)\nabla_{\theta}\pi(a|s,\theta)
\end{align}
```
当$`\gamma \to 1`$时，$`\frac{1}{1-\gamma}\to\infty`$，所以第二项权重大，第一项可以省略（好吧，你说能省就能省），所以：  
```math
\begin{align}
\nabla_{\theta}\bar{v}_{\pi} &\approx \frac{1}{1-\gamma}\sum_{s\in\mathcal{S}}d_{\pi}(s)\sum_{a\in\mathcal{A}}q_{\pi}(s,a)\nabla_{\theta}\pi(a|s,\theta)\\
& 老套路，为了转成期望，需要把\pi从\nabla里提出来\\
&= \frac{1}{1-\gamma}\sum_{s\in\mathcal{S}}d_{\pi}(s)\sum_{a\in\mathcal{A}}q_{\pi}(s,a)\pi(a|s,\theta)\nabla_{\theta}\ln \pi(a|s,\theta)\\
&转成期望 \\
&= \frac{1}{1-\gamma}\mathbb{E}[q_{\pi}(S,A)\nabla_{\theta}\ln\pi(A|S,\theta)]
\end{align}
```
由于$`\bar{r}_{\pi} = (1-\gamma)\bar{v}_{\pi}`$，所以：  
```math
\begin{align}
\nabla_{\theta}\bar{r}_{\pi} &= (1-\gamma)\nabla_{\theta}\bar{v}_{\pi}\\
&\approx (1-\gamma) \frac{1}{1-\gamma}\mathbb{E}[q_{\pi}(S,A)\nabla_{\theta}\ln\pi(A|S,\theta)]\\
&= \mathbb{E}[q_{\pi}(S,A)\nabla_{\theta}\ln\pi(A|S,\theta)]
\end{align}
```

#### Monte Carlo policy gradient(REINFORCE)
收集下，梯度上升的目标函数为：  
```math
J(\theta) = \bar{r}_{\pi}
```
梯度为：  
```math

\nabla_{\theta} J(\theta) = \nabla_{\theta} \bar{r}_{\pi} = \mathbb{E}[q_{\pi}(S,A)\nabla_{\theta}\ln\pi(A|S,\theta)]
```
期望形式，为了应用蒙特卡洛法。  
因此，梯度上升迭代公式为：  
```math
\begin{align}
\theta_{t+1} &= \theta_{t} + \alpha \nabla_{\theta}J(\theta)\\
&= \theta_{t} + \alpha \mathbb{E}\nabla_{\theta}\ln\pi(A|S,\theta) q_{\pi}(S,A)
\end{align}
```
随机梯度下降是$`-`$,这里是随机上升，所以是+。  
得不到期望，所以用随机采样的样本代替：  
```math
\theta_{t+1} = \theta_{t} + \alpha q_t(s_t,a_t) \nabla_{\theta} \ln\pi(a_t|s_t,\theta)
```
这里有一个事实让我给忽略了，期望形式中，行动价值是$`q_{\pi}(S,A)`$，但是随机梯度形式中，行动价值是$`q_t(s,a)`$。$`q_{\pi}`$是个理想值，也是个期望。但$`q_t`$只是单个样本。所以，这里还有一个估计，是用单条样本估计来代替了理想值$`q_{\pi}`$。这是蒙特卡洛法的做法，这个算法称为REINFORE。而这个估计也可以通过其他形式，类似之前估计状态价值，是用method approximation的方式，把s,a输入进某个神经网络，得到一个估计的行动价值，估摸这就是后面的ac法。  
  
变个形：  
```math
\begin{align}
\theta_{t+1} &= \theta_{t} + \alpha q_t(s_t,a_t) \nabla_{\theta} \ln\pi(a_t|s_t,\theta) \\
&= \theta_{t} + \alpha q_t(s_t,a_t) \frac{\nabla_{\theta} \pi(a_t|s_t,\theta)}{\pi(a_t|s_t,\theta)}\\
&= \theta_{t} + \alpha \frac{q_t(s_t,a_t)}{\pi(a_t|s_t,\theta)}\nabla_{\theta} \pi(a_t|s_t,\theta)
\end{align}
```
设$`\beta_t = \frac{q_t(s_t,a_t)}{\pi(a_t|s_t,\theta)}`$则：  
```math
\theta_{t+1} =\theta_{t} + \alpha \beta_t \nabla_{\theta} \pi(a_t|s_t,\theta)
```
这样公式就更简洁清晰了。可以理解，自变量是$`\theta`$，这个迭代公式就是调整$`\theta`$找$`\pi(a_t|s_t,\theta)`$的最大值，也就是选择动作$`a_t`$的概率。而$`\beta_t`$决定了调整的方向。  
根据泰勒公式：  
```math
\begin{align}
\pi(a_t|s_t,\theta_{t+1}) &\approx \pi(a_t|s_t,\theta_t) + \nabla_{\theta}\pi(a_t|s_t,\theta_t)(\theta_{t+1}-\theta_{t})\\
&= \pi(a_t|s_t,\theta_t) + \nabla_{\theta}\pi(a_t|s_t,\theta_t)\alpha \beta_t \nabla_{\theta} \pi(a_t|s_t,\theta)\\
&= \pi(a_t|s_t,\theta_t) + \alpha \beta_t ||\nabla_{\theta}\pi(a_t|s_t,\theta_t)||^2_2
\end{align}
```
所以，如果$`\beta_t \gt 0`$，则$`\pi(a_t|s_t,\theta_{t+1}) \gt \pi(a_t|s_t,\theta_t)`$，也就是选择$`a_t`$的概率会加大。反之，则概率减小。而且，$`beta_t`$的大小还影响了概率调整的幅度。  
  
然后看$`\beta_t = \frac{q_t(s_t,a_t)}{\pi(a_t|s_t,\theta)}`$，挺有意思的。  
$`\beta_t`$和$`q_t(s_t, a_t)`$成正比，也就是行动价值越大的动作，调整它的概率越大，让它有更多的可能被选中。而$`\beta_t`$和$`\pi(a_t|s_t,\theta)`$也就是动作选中的概率成反比，如果一个动作它被选中的概率比较小，那么它调整的幅度就更大。  
说白了，这个公式，让行动价值更大的动作被选中概率更大，以更好的利用样本，让概率小的动作也更容易被选中，以更好探索。所以书上说，达到了探索与利用的平衡。  
  
最后，关于样本采样，说算法9.1提升了样本利用率，不太懂。  
不过仔细看算法，其中的行动价值，也是需要未来的奖励计算得来的。这又回到之前的问题。一种是把数据都记下来，等回合结束从后往前计算行动价值。多回合的同一s,a行动价值组成期望来估计真实行动价值。一种是类似TD法，用下一个状态的行动价值估计值代替后面的计算。  

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

