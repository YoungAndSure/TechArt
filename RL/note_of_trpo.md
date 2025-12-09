#### 公式3替代了公式2，在实际任务中是怎么做的？  
迭代的流程是这样的，先根据策略$`\pi`$行动，行动过程中对于$`s,a`$访问的概率权重是$`\rho_{\pi}`$,收集样本，计算平均期望，求策略梯度，更新策略到$`\tilde{\pi}`$。  
说的是，在更新到$`\tilde{\pi}`$之前，想评估一下策略提升前后的平均奖励提升幅度。公式就是：  
```math
\eta(\tilde{\pi})=\eta(\pi) + \sum_{s}{\rho}_{\tilde{\pi}}(s)\sum_{a}\tilde{\pi}(s,a)A_{\pi}(s,a)
```
其中访问哪个状态以及选择哪个动作，都跟新策略有关，所以是$`\tilde{\rho}_{\pi}`$和$`\tilde{\pi}(s,a)`$,而行动价值$`q_{\pi}(s,a)`$和状态价值$`v_{\pi}(s,a)`$都是在策略行动$`\pi`$时计算出来的。也就是说在老策略的价值体系下用新策略评估平均奖励提升了多少。（注意，$`q_{\pi}(s,a)`$可是依赖了未来的状态价值，也是经过策略$`\pi`$行动、迭代收敛来的，所以可不能写成$`A_{\tilde{\pi}}(s,a)`$。  
再理解下，为什么是$`A_{\pi}(s,a)`$。如果固定策略$`\pi`$，一直按照策略$`\pi`$行动，收集样本，计算行动价值和状态价值，最终会收敛到策略$`\pi`$下的行动价值和状态价值，也就是贝尔曼方程固定策略时状态价值的解。按照传统动态规划中迭代法的方法，这时候可以按照贪婪策略调整策略$`\pi`$，得到最优策略，然后继续按照新策略行动，再次收敛。。循环往复，最终解出贝尔曼最优方程。而策略梯度法是更新策略，但不是贪婪策略，因为它还要考虑探索性。其实和动态规划是一个原理。而新的策略，在前策略得到的状态价值上，应该得到更优的状态价值。在上面公式中，也就是说加号后面的部分要大于0。  
  
说跑题了。为了评估新策略对旧策略的提升，可以按照上式计算加号后部分。如果智能体真的按照新策略行动一遍，但不更新行动价值和状态价值，就能计算出来，且状态权重概率是$`\rho_{\tilde{\pi}}`$。但现实中比较困难，所以无法得到新策略下的$`\rho_{\tilde{\pi}}`$，而是用旧策略行动中得到$`\rho_{\pi}`$代替。  

#### 实际应用中是怎么计算替代目标的
替代目标就是：  
```math
L_{\pi}(\tilde{\pi}) = \eta_{\pi} + \sum_{s}\rho_{\pi}(s)\sum_a \tilde{\pi}(s,a)A_{\pi}(s,a)
```
因为新的策略必须要让智能体走一遍才能采集到真实的样本，计算出新策略下的累计折扣奖励期望$`\eta_{\tilde{\pi}}`$，难实现。所以可以用旧策略下采集到样本，结合新策略，来计算出一个近似的替代目标$`L_{\pi}(\tilde{\pi})`$。由于用的是旧策略的样本，所以它的状态访问概率密度是旧策略的$`\rho_{\pi}`$，而不是$`\rho_{\tilde{\pi}}`$。  
所以，替代目标计算方法就等于用旧策略下样本，计算新策略下目标，通过重要性采样就可以实现。也就是：  
```math
L_{\pi}(\tilde{\pi}) = \eta_{\pi} + \frac{1}{N}\sum_{i=1}^N \frac{\pi(s_i,a_i)}{\tilde{\pi}(s_i,a_i)} A_{\pi}(s_i,a_i)
```

#### 为什么要限制策略更新幅度？
相对优势有正有负，这都正常，策略更新做的就是提升正优势的概率，降低负优势的概率。  
真正的问题在于：  
- 样本方差大导致的估计偏差。如果样本方差大，会导致估计的期望大幅偏离真实期望，产生估计偏差。  
- method approximation 导致的估计误差。函数逼近法本身的缺陷。  

这些都可能导致优势的估计错误。这时候如果完全按照估计值更新策略，就会放大错误，后续需要很多次正确迭代逐渐修复，如果误差持续累积，就会导致离真实期望越来越远。  

#### Kakade & Langford 证明的下界怎么来的  
几个符号概念：  
$`\pi_{old}`$:老策略  
$`\pi_{new}`$:新策略  
$`L_{\pi_{old}}(\pi_{old})`$:在老策略$`\pi_{old}`$下得到的估计目标，其实就等于真实的目标$`\eta(\pi_{old})`$  
$`L_{\pi_{old}}(\pi_{new})`$:在老策略$`\pi_{old}`$得到的价值体系下，应用新策略$`\pi_{new}`$得到的估计目标，理论上小于在新策略上运行得到的真实目标$`\eta(\pi_{new})`$  
$`\pi'`$:$`\pi'=\argmax L_{\pi_{old}}(\pi_{old})`$，根据老策略计算出的目标，应用贪婪策略得到的策略，更新幅度会很大，注意，它等于$`\pi'=\argmax \eta(\pi_{old})`$,如果按照贪婪策略更新策略，$`\pi_{new}=\pi'`$了，现在是要取其中。由于是贪婪策略，所以必然$`L_{\pi_{old}}(\pi') \ge L_{\pi_{old}}(\pi_{old})`$  
论文是说，如果新策略是老策略和最优策略的折中：  
```math
\pi_{new}(s,a) = (1-\alpha)\pi_{old}(s,a) + \alpha\pi'(s,a)
```
那么：  
```math
\begin{align}
\eta(\pi_{\text{new}}) &\geq L_{\pi_{\text{old}}}(\pi_{\text{new}}) - \frac{2\epsilon\gamma}{(1 - \gamma)^2} \alpha^2\\
\eta(\pi_{\text{new}}) - \eta(\pi_{\text{old}}) &\geq L_{\pi_{\text{old}}}(\pi_{\text{new}}) - \eta(\pi_{\text{old}}) - \frac{2\epsilon\gamma}{(1 - \gamma)^2} \alpha^2\\
\eta(\pi_{\text{new}}) - \eta(\pi_{\text{old}}) &\geq L_{\pi_{\text{old}}}(\pi_{\text{new}}) - L_{\pi_{old}}(\pi_{old}) - \frac{2\epsilon\gamma}{(1 - \gamma)^2} \alpha^2\\
\end{align}
```
因此，结论就是，如果按照以上折中的方式更新策略，目标更新的下界就是：  
```math
L_{\pi_{\text{old}}}(\pi_{\text{new}}) - L_{\pi_{old}}(\pi_{old}) - \frac{2\epsilon\gamma}{(1 - \gamma)^2} \alpha^2
```

#### 什么是total variation divergence  
上边的Kakade & Langford策略，只能应用到类似九宫格这种，行为有限，且非神经网络的策略。在神经网络里，都是梯度下降更新策略，没法像公式里的，用个加权公式更新策略。这就是论文里说的，Kakade & Langford用于mixture policies,而TRPO可以用于general policies.  
所以论文是要拓展这个策略更新公式，用一种可以求梯度的公式来衡量新老策略差异，反向传播更新策略。  
total variation divergence是一种衡量两个策略差异的方法，叫总变差。  
公式看着挺复杂，其实就是两个策略概率分布求差加和乘1/2。  
强化学习里是每个状态一个策略，所以拓展为对所有状态求出的分布差异取max，就是公式7。  
公式8给出了用TV衡量策略得到的目标更新下界。  

#### 怎么理解这个"下界"
$`L_{\theta_{old}}(\theta)`$是对策略$`\theta`$下真实目标$`\eta(\theta)`$的估计。如果直接用$`\eta(\theta)`$做目标，策略更新后新的目标会更新到估计值$`L_{\theta_{old}}(\theta)`$。  
但这样会导致以上说的误差累积问题。所以，需要一个公式来找到一个下界，下界就是说，更新多少，会保证策略是在提升的（比如更新0.00001）。  
通过推演得出$`L_{\theta_{old}}(\theta)-CD_{KL}^{\max}(\theta_{old},\theta)`$是新策略下目标的下界。这个公式后半部分是$`CD_{KL}^{\max}(\theta_{old},\theta)`$,是个新老策略的度量，理论上如果新老策略没变化，这部分就是0，变化幅度越大，这部分值越大。  
既然知道了下界，目标就可以更新为提升下界。因为下界更保守，既保证了会提升，又防止了提升过多。  

#### 演化
本来优化的目标是:  
```math
\eta(\theta)=\mathbb{E}_{s_0,a_0...}[\sum_{t=0}^{\infty}\gamma^tr(s_t)]
```
对于优化后的新策略$`\tilde{\theta}`$,目标可以拆解为：  
```math
\begin{align}
\eta(\tilde{\theta}) &= \eta(\theta) + \mathbb{E}_{s_0,a_0...}[\sum_{t=0}^{\infty}\gamma^t A_{\theta}(s_t, a_t)]\\
&= \eta(\theta) + \sum_s \rho_{\tilde{\theta}}(s)\sum_a \pi(a|s,\tilde{\theta}) A_{\theta}(s,a)
\end{align}
```
也就是用新的策略加旧的价值体系计算相对优势，加上原来的目标，等于新策略目标。  
但没按照新策略运行之前，没法得到新的状态分布，计算新的相对优势，所以用老策略的样本替代：  
```math
\begin{align}
L_{\theta}(\tilde{\theta}) &= \eta(\theta) + \sum_s \rho_{\theta}(s)\sum_a \pi(a|s,\tilde{\theta}) A_{\theta}(s,a)\\
&= L_{\theta}(\theta)+ \sum_s \rho_{\theta}(s)\sum_a \pi(a|s,\tilde{\theta}) A_{\theta}(s,a)
\end{align}
```
得到的$`L_{\theta}(\tilde{\theta})`$是$`\eta(\tilde{\theta})`$的近似。  
实际中以$`L_{\theta}(\tilde{\theta})`$为目标更新策略，会导致误差累积。因此在策略更新时，需要约束新策略的更新幅度。对于过去非神经网络的策略，可以直接对策略加权得到。对于现代的，基于神经网络的策略，需要用KL散度衡量新旧策略差异，通过差异构造目标函数下界，以下界作为目标，驱动参数更新。  
因此，目标变为：  
```math
J(\theta)=\max_{\theta} [L_{\theta}(\tilde{\theta}) - CD_{KL}^{\max}(\tilde{\theta},\theta)]
```
也就是调整$`\theta`$提升下界。  
但，这个公式会导致提升幅度很小，迭代很慢，因此，可以通过约束参数$`\theta`$的更新幅度来实现：  
```math
J(\theta)=\max_{\theta} [L_{\theta}(\tilde{\theta})]\\
\text{subject to}\ D_{KL}^{\max}(\tilde{\theta},\theta) \le \delta
```
其中的$`\max`$算子的对象是所有状态。但对于状态连续、无限的任务来说，需要枚举所有状态，计算量太大，所以替换成期望：  
```math
J(\theta)=\max_{\theta} [L_{\theta}(\tilde{\theta})]\\
\text{subject to}\ \bar{D}_{KL}^{\rho_{\theta_{old}}}(\tilde{\theta},\theta) \le \delta
```

#### 三个替换  
原公式：  
```math
\max_{\theta} \sum_s \rho_{\theta_{old}}(s)\sum_a \pi_{\theta}(a|s)A_{\theta_{old}}(s,a)\\
\text{suject to } \bar{D}_{KL}^{\rho_{\theta}}(\theta_{old}, \theta) \le \delta
```
状态访问换成期望：  
```math
\max_{\theta} \mathbb{E}_{s-\rho_{\theta_{old}}}[\sum_a \pi_{\theta}(a|s)A_{\theta_{old}}(s,a)]\\
\text{suject to } \bar{D}_{KL}^{\rho_{\theta}}(\theta_{old}, \theta) \le \delta
```
相对优势换成行动价值：  
```math
\max_{\theta} \mathbb{E}_{s-\rho_{\theta_{old}}}[\sum_a \pi_{\theta}(a|s)Q_{\theta_{old}}(s,a)]\\
\text{suject to } \bar{D}_{KL}^{\rho_{\theta}}(\theta_{old}, \theta) \le \delta
```
行动换成期望形式，为了在旧数据上跑新策略，需要增加重要度采样：  
```math
\max_{\theta} \mathbb{E}_{s-\rho_{\theta_{old},a-q}}[\frac{\pi_{\theta}(a|s)}{q(a|s)}Q_{\theta_{old}}(s,a)]\\
\text{suject to } \bar{D}_{KL}^{\rho_{\theta}}(\theta_{old}, \theta) \le \delta
```

#### Vine采样  
- 首先选择起始状态$`s_0`$，按照概率分布$`\rho_0`$选择。  
- 从$`s_0`$开始，按照策略$`\pi_{\theta_i}`$行动，得到一组轨迹。  
- 每条轨迹经过了多个状态。如果轨迹是m条，每条行动了n次，一共访问m*n次状态。每条轨迹访问状态的数量可能不同。从这些N条轨迹访问过的状态里选择N个状态，记为$`s_1,s_2...s_N`$,称之为roll out set  
- 对这N个状态，每个状态$`s_n`$按照策略$`q(a_?|s_n)`$选择K个行动。这个策略是可以根据任务调整的，论文说如果是连续型任务，$`q(a_?|s_n)=\pi_{\theta_i}`$效果比较好，也就是还按照策略来选K个行动。而离散型任务用均匀分布效果比较好。  
- 还有一点，是策略$`q(a_?|s_n)`$的支持集必须包含策略$`\pi_{\theta_i}`$的支持集。这点在重要度采样里也有涉及。所谓支持集我理解就是概率大于0的选项的集合。如果某个选项策略$`q(a_?|s_n)=0`$而策略$`\pi_{\theta_i}>0`$，那两者的支持集就不是包含关系。说白了这导致你完全忽略了后者中的某个选项，会导致偏差。  
- N个状态，每个选出K个行动，从这K个行动开始，按照策略$`\pi_{\theta_i}`$继续行动，得到$`N \times K`$条轨迹，计算得到$`N \times K`$个累积折扣奖励。  

