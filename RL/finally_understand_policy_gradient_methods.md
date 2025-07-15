# 终于理解了策略梯度法

读《深度学习入门4：强化学习》到第九章时，引入策略梯度法，短小的篇幅引入了多个概念，搞得我措手不及。经过反复的思考，结合代码，最终才理解。如果你也没看懂，可以按照我的思路走一遍。

## 策略梯度法的神经网络和之前基于价值的方法有什么不同？

一般会先介绍基于价值的方法，再引出基于策略的方法。策略梯度法相较基于价值的方法有很大的不同，很容易到这里卡住。先做个比较：

| **特征**                     | **基于价值的方法（如DQN）** | **策略梯度法（如REINFORCE）** |
|------------------------------|----------------------------|-----------------------------|
| **输入**                     | 状态（State）              | 状态（State）               |
| **输出**                     | 动作的Q值                  | 动作概率分布                |
| **输出意义**                 | 动作的长期价值             | 动作的选择概率或分布特性    |

可以看到，策略梯度法的神经网络，输入是状态`state`，输出是动作的概率分布。我们把这个神经网络中的权重记为 $\theta$ ，某时刻 $t$ 通过 $\theta$ 可以获取到一个状态 $S_t$ 对应的各个动作 $A_t$ 的概率分布，记为 $\pi_\theta(A_t \mid S_t)$。

## 策略梯度法优化的目标是什么？

当然是奖励。对于多个回合的游戏，则是奖励的期望。于是就有了：

假设有一个智能体，在玩游戏。某一个回合，生成序列：
$$\tau = (S_0, A_0, R_0, S_1, A_1, R_1, \cdots, S_{T+1})$$

这个序列过程中的折扣奖励为：
$$G(\tau) = R_0 + \gamma R_1 + \gamma^2 R_2 + \cdots + \gamma^T R_T$$

多次游戏，则生成多个序列，获取到多个折扣奖励。假设每个序列出现的概率为 $\text{Pr}(\tau)$，则对所有序列求期望：
$$E_\tau[G(\tau)] = \sum_{\tau} \text{Pr}(\tau) G(\tau)$$

也就是，某个回合序列出现的概率 $\text{Pr}(\tau)$ 乘以整个序列的收益，所有回合相加，即期望。这就是我们要优化的目标，也是要通过神经网络提升的目标。

## 神经网络和目标是什么关系？

上面已经介绍过神经网络 $\pi_\theta(A_t \mid S_t)$。于是，在目标和神经网络 $\theta$ 之间建立公式：

$\text{Pr}(\tau)$ 是经过神经网络 $\theta$ 得到的概率，可以表示为：$`\text{Pr}(\tau \mid \theta)`$。把 $\text{Pr}(\tau \mid \theta)$ 按照MDP展开（忽略了即时奖励的概率，整本书都没有提，这里也先忽略）：

$$
\begin{align*}
\text{Pr}(\tau \mid \theta) &= p(S_0) \pi_\theta(A_0 \mid S_0) p(S_1 \mid S_0, A_0) \cdots \pi_\theta(A_T \mid S_T) p(S_{T+1} \mid S_T, A_T) \\
&= p(S_0) \prod_{t=0}^T \pi_\theta(A_t \mid S_t) p(S_{t+1} \mid S_t, A_t)
\end{align*}
$$

逐项解释一下：
- $S_0$ 是起始状态，出现的概率是 $p(S_0)$
- 之后，每一个时刻，将 $S_t$ 输入到 $\theta$ 神经网络，获取动作 $A_t$ 的概率为 $\pi_\theta(A_t \mid S_t)$
- 在状态 $S_t$ 执行动作 $A_t$ 之后，跳转到状态 $S_{t+1}$ 的概率为 $p(S_{t+1} \mid S_t, A_t)$

将 $\text{Pr}(\tau \mid \theta)$ 代入 $E_\tau[G(\tau)] = \sum_{\tau} \text{Pr}(\tau \mid \theta) G(\tau)$:

$$
\begin{aligned}
E_\tau[G(\tau)] &= \sum_\tau \text{Pr}(\tau \mid \theta) G(\tau) \\
&= \sum_\tau \left[ p(S_0) \prod_{t=0}^T \pi_\theta(A_t \mid S_t) p(S_{t+1} \mid S_t, A_t) \right] G(\tau) \\
&= \sum_{S_0, A_0, S_1, \ldots, A_T, S_{T+1}} \left[ p(S_0) \prod_{t=0}^T \pi_\theta(A_t \mid S_t) p(S_{t+1} \mid S_t, A_t) \right] \times \sum_{t=0}^T \gamma^t R_t
\end{aligned}
$$

到这里，公式就完全展开了，建立起了神经网络 $\theta$ 和目标 $E_\tau[G(\tau)]$ 的关系。策略梯度法的目标就是通过调整神经网络 $\theta$ 来提升 $E_\tau[G(\tau)]$，因此，这个函数称之为"目标函数"，记为 $J(\theta)$。

## 最优化和梯度下降的区别

有这个疑问，是因为之前已经习惯了监督学习的运行方式：找一个目标，用经过神经网络的预估值和目标求差作为loss，loss反向传播求梯度，权重更新梯度。

按照监督学习的路数，来尝试给以上 $J(\theta)$ 找个label。比如，在一个回合结束后，通过记录奖励 $G(\tau)$，以及多回合的概率分布 $\text{Pr}(\tau)$，计算出一个真实的 $E_\tau[G(\tau)]$，可以用它来当做label吗？

**不可以。** 通过这种方式算出来的 $E_\tau[G(\tau)]$ 并不能称作目标，只能说是真实情况的反映。就像做题，虽然你能用各种方法做出来，但只能是你自己的解，都不是最优答案。监督学习必须要知道最优答案之后，才能调整答案生成过程往最优答案靠。

而强化学习，没有一个label来当做标签的，只是知道目标 $J(\theta)$ 和神经网络 $\theta$ 的关系，希望通过调整神经网络让目标更大。这就是最优化问题。

在监督学习里，对于一个以 $\theta$ 为神经网络权重的函数 $J(\theta)$ 梯度更新是这样的：
$$\theta \leftarrow \theta - \alpha \nabla_\theta J(\theta)$$

可以用一个二维函数 $J(\theta) = 0.1\theta^2 - 2\theta + 10$ 代替神经网络来理解这样更新梯度的含义：

如图，对函数求梯度，在 $`\theta = 20`$ 处，梯度为+2，此时应用以上公式，设 $`\alpha`$ 为1，$`\theta`$ 更新后为18，往左移动，也就更靠近 $`\theta = 10`$ 的最小值点。

反之，如果在 $`\theta = 0`$ 处求梯度，梯度为-2，此时应用以上公式，$`\theta`$ 更新为2，向右移，更靠近 $`\theta = 10`$ 的最小值点。因此，当用以上公式更新权重 $`\theta`$ 时，$`\theta`$ 会逐渐向让 $`J(\theta)`$ 最小的方向移动。

而监督学习里，$`J(\theta)`$ 就是loss，$`\theta`$ 就是神经网络权重，我们利用梯度下降法让loss减小，也就让预估值和目标值更接近了。

但，现在我们面临的，不是找最小值，而是要找让 $`J(\theta)`$ 更大的值。理解了以上梯度下降找最小值，最优化找最大值的方法也就比较简单了，调整 $`\theta`$ 更新的方式为：
$$\theta \leftarrow \theta + \alpha \nabla_\theta J(\theta)$$

即可。还拿以上函数 $`J(\theta) = 0.1\theta^2 - 2\theta + 10`$ 举例，对函数求梯度。
- 在 $`\theta = 20`$ 处，梯度为+2，此时应用以上公式，设 $`\alpha`$ 为1，$`\theta`$ 更新后为22，往右移动，$`J(\theta)`$ 增大。
- 反之，如果在 $`\theta = 0`$ 处求梯度，梯度为-2，此时应用以上公式，$`\theta`$ 更新为-2，向左移，$`J(\theta)`$ 增大。

这就是最优化对 $`\theta`$ 的调整方法。

但大部分训练框架的optimizer都是梯度下降，该如何应用呢？

**两种方法：**
1. 自定义训练框架的optimizer，调整梯度更新的方向
2. 用 $`-J(\theta)`$ 作为目标

比如上文中的 $`J(\theta) = 0.1\theta^2 - 2\theta + 10`$，取负之后：$`-J(\theta) = -(0.1\theta^2 - 2\theta + 10)`$ 的图形：

这时候，通过梯度下降法 $`\theta \leftarrow \theta - \alpha \nabla_\theta [-J(\theta)]`$ 更新参数，会让 $`\theta`$ 朝着让 $`-J(\theta)`$ 减小的方向移动（往两边移动），也就是 $`J(\theta)`$ 增大的方向了。我们采用这种方法。

## 可以直接对 $`-J(\theta)`$ 求梯度更新吗？

回顾一下：
```math
\begin{aligned}
J(\theta) &= E_\tau[G(\tau)] \\
&= \sum_\tau \text{Pr}(\tau) G(\tau) \\
&= \sum_\tau \left[ p(S_0) \prod_{t=0}^T \pi_\theta(A_t \mid S_t) p(S_{t+1} \mid S_t, A_t) \right] G(\tau) \\
&= \sum_{S_0, A_0, S_1, \ldots, A_T, S_{T+1}} \left[ p(S_0) \prod_{t=0}^T \pi_\theta(A_t \mid S_t) p(S_{t+1} \mid S_t, A_t) \right] \times \sum_{t=0}^T \gamma^t R_t
\end{aligned}
```


看起来，只要我们按照以上的公式进行编码，最终得出个 $`J(\theta)`$ 的tensor，加上负号，再调用backward，就可以求梯度了，再调用optimizer更新参数，$`\theta`$ 就可以朝着让 $`J(\theta)`$ 增大的方向调整了。

但问题是，以上公式中的状态转移概率 $`p(S_{t+1} \mid S_t, A_t)`$ 在大多数场景下是无法获知的。举个具体例子，比如一辆车在路上行驶，探测到前面路边有一个人，这是一个状态 $`S_t`$，此时选择动作 $`A_t`$：继续行驶，那状态会转移到哪呢？有可能路边的人没动，这是一个状态，有可能路边的人突然开始跑动，这又是一个状态。但这两种状态转移的概率是多少呢？如果想获取到这个状态转移的概率分布的话，就需要反复做实验收集数据。比如收集所有车遇到这种情况采用不同动作后的状态，建立概率分布。这不但成本高，而且随着时间推移，这个概率分布可能会变化，需要一直更新。甚至有的场景下，是无法获取到状态转移的概率分布的。

因此，以上直接对 $`-J(\theta)`$ 求梯度的方法在实际场景中不可行。

## 如何定义损失函数

既然 $`-J(\theta)`$ 不能直接得到，那是不是可以找到一个不包含 $`p(S_{t+1} \mid S_t, A_t)`$ 的损失函数 $`L(\theta)`$，使得 $`\nabla L(\theta) = -\nabla J(\theta)`$? 这样的话，对 $`L(\theta)`$ 进行反向传播调整 $`\theta`$，就相当于对 $`-J(\theta)`$ 进行反向传播调整 $`\theta`$？

沿着这个思路，先求一下 $`\nabla J(\theta)`$。以下推导虽然书中有写，但比较简单，这里增加过程的解说。

按照上文对 $`J(\theta)`$ 的定义，加上梯度展开：
```math
\begin{align*}
\nabla_\theta J(\theta) & = \nabla_\theta \mathbb{E}_{\tau \sim \pi_\theta}[G(\tau)] \\
& = \nabla_\theta \sum_\tau \text{Pr}(\tau \mid \theta) G(\tau) \\
& = \sum_\tau \nabla_\theta \left( \text{Pr}(\tau \mid \theta) G(\tau) \right) \\
& = \sum_\tau \left\{ G(\tau) \nabla_\theta \text{Pr}(\tau \mid \theta) + \text{Pr}(\tau \mid \theta) \nabla_\theta G(\tau) \right\} \\
& = \sum_\tau G(\tau) \nabla_\theta \text{Pr}(\tau \mid \theta)
\end{align*}
```

由于 $`G(\tau)`$ 是本回合的累加收益，是个常数，所以对 $`\theta`$ 求梯度等于0，所以以上导数第二行加法后的项等于0。

继续：
```math
\begin{align*}
& = \sum_\tau G(\tau) \text{Pr}(\tau \mid \theta) \frac{\nabla_\theta \text{Pr}(\tau \mid \theta)}{\text{Pr}(\tau \mid \theta)} \\
& = \sum_\tau G(\tau) \text{Pr}(\tau \mid \theta) \nabla_\theta \log \text{Pr}(\tau \mid \theta)
\end{align*}
```

这里的变形有点意思，涉及另外一个证明：
$`\nabla_\theta \log \text{Pr}(\tau \mid \theta) = \frac{\nabla_\theta \text{Pr}(\tau \mid \theta)}{\text{Pr}(\tau \mid \theta)}`$

证明：设 $u = \text{Pr}(\tau \mid \theta)$，则：
$`\frac{d}{d\theta} \log u = \frac{1}{u} \cdot \frac{du}{d\theta}`$

带回后：
$`\nabla_\theta \log \text{Pr}(\tau \mid \theta) = \frac{1}{\text{Pr}(\tau \mid \theta)} \cdot \nabla_\theta \text{Pr}(\tau \mid \theta)`$

这个是**log梯度技巧（log-likelihood trick）**，将对数加入到梯度的求导中。为什么要把这个log加入进来呢？简单说就是利用了log可以将乘法转换成加法的性质，下文会用到。

到目前，得到：
```math
\begin{align*}
\nabla_\theta J(\theta) & = \nabla_\theta \mathbb{E}_{\tau \sim \pi_\theta}[G(\tau)] \\
& = \sum_\tau G(\tau) \text{Pr}(\tau \mid \theta) \nabla_\theta \log \text{Pr}(\tau \mid \theta) \\
& = \mathbb{E}_{\tau \sim \pi_\theta} \left[ G(\tau) \nabla_\theta \log \text{Pr}(\tau \mid \theta) \right]
\end{align*}
```

发现没有，这里把期望的梯度，换成了梯度的期望。为什么要这么做呢？因为只有换成梯度的期望，才能应用蒙特卡洛法，用采样近似。也就是说，我们可以在多回合游戏中，通过计算 $`G(\tau) \nabla_\theta \log \text{Pr}(\tau \mid \theta)`$ 取平均值，来近似 $`\mathbb{E}_{\tau \sim \pi_\theta} \left[ G(\tau) \nabla_\theta \log \text{Pr}(\tau \mid \theta) \right]`$，而不用去求 $`\text{Pr}(\tau \mid \theta)`$。上面已经说过了，由于状态转移概率无法获取到，所以 $`\text{Pr}(\tau \mid \theta)`$ 是获取不到的。

继续求 $`\nabla_\theta \log \text{Pr}(\tau \mid \theta)`$：
```math
\begin{align*}
\text{Pr}(\tau \mid \theta) &= p(S_0) \pi_\theta(A_0 \mid S_0) p(S_1 \mid S_0, A_0) \cdots \pi_\theta(A_T \mid S_T) p(S_{T+1} \mid S_T, A_T) \\
&= p(S_0) \prod_{t=0}^T \pi_\theta(A_t \mid S_t) p(S_{t+1} \mid S_t, A_t)
\end{align*}
```

这个上文展开过。
```math
\begin{align*}
\log \text{Pr}(\tau \mid \theta) &= \log p(S_0) + \sum_{t=0}^T \log p(S_{t+1} \mid S_t, A_t) + \sum_{t=0}^T \log \pi_\theta(A_t \mid S_t)
\end{align*}
```

取对数，将乘法转成加法。这大大降低了计算量，不然以上的乘法通过链式法则展开将很复杂。
```math
\begin{align*}
\nabla_\theta \log \text{Pr}(\tau \mid \theta) &= \nabla_\theta \left\{ \log p(S_0) + \sum_{t=0}^T \log p(S_{t+1} \mid S_t, A_t) + \sum_{t=0}^T \log \pi_\theta(A_t \mid S_t) \right\} \\
&= \nabla_\theta \sum_{t=0}^T \log \pi_\theta(A_t \mid S_t)
\end{align*}
```

求梯度，与 $\theta$ 无关的项，求梯度后为0。比如实际场景中无法获取的状态转移概率 $p(S_{t+1} \mid S_t, A_t)$，在这个过程中被消掉。

最终：
```math
\begin{align*}
\nabla_\theta J(\theta) &= \mathbb{E}_{\tau \sim \pi_\theta} \left[ G(\tau) \nabla_\theta \log \text{Pr}(\tau \mid \theta) \right] \\
&= \mathbb{E}_{\tau \sim \pi_\theta} \left[ G(\tau) \sum_{t=0}^T \nabla_\theta \log \pi_\theta(A_t \mid S_t) \right]
\end{align*}
```

通过蒙特卡洛法采样近似，可以得到：
$`\nabla_\theta J(\theta) \simeq \sum_{t=0}^T G(\tau) \nabla_\theta \log \pi_\theta(A_t \mid S_t)`$

推导过程比较长，总结下核心的点：
1. 状态转移概率 $`\text{Pr}(\tau \mid \theta)`$ 实际环境中很难获取，需要规避
2. 期望的梯度需要求出期望，而期望又依赖概率分布 $\text{Pr}(\tau \mid \theta)$，所以把期望的梯度转换成梯度的期望，这样就可以通过蒙特卡洛法，用采样数据做近似了
3. 对数log的加入解决了以上两个问题：
   - 一方面把期望的梯度转换成了梯度的期望
   - 另一方面通过乘法转加法，消掉了 $\text{Pr}(\tau \mid \theta)$ 的梯度项，从而使 $\nabla_\theta J(\theta)$ 与状态转移概率无关

综上，我们得到了 $\nabla_\theta J(\theta)$。再说回最开始的任务，如何找到一个不含 $\text{Pr}(\tau \mid \theta)$ 的损失函数 $L(\theta)$，使得 $\nabla L(\theta) = -\nabla J(\theta)$?

再看看公式：
```math
\begin{align*}
\nabla_\theta J(\theta) &\simeq \sum_{t=0}^T G(\tau) \nabla_\theta \log \pi_\theta(A_t \mid S_t) \\
& = \nabla_\theta \sum_{t=0}^T G(\tau) \log \pi_\theta(A_t \mid S_t)
\end{align*}
```

由于加和是线性的，$`G(\tau)`$ 是常数，梯度符号可以拿出来。去掉两边的梯度符号，加上负号，至此，我们找到了一个代理损失函数 $`L(\theta)`$：
```math
\begin{align*}
L(\theta) & = - \sum_{t=0}^T G(\tau) \log \pi_\theta(A_t \mid S_t)
\end{align*}
```

对这个 $`L(\theta)`$ 反向传播、调整 $`\theta`$，$`\theta`$ 将朝着使 $`J(\theta)`$ 增大的方向调整。

至此，策略梯度法证明完毕。

## 涉及的核心思想

1. **目标奖励和神经网络 $`\theta`$ 的关系推导**：只有找到了关系，才能获取到神经网络 $`\theta`$ 调整的目标
2. **梯度下降找最小值，最优化找最大值**
3. **代理损失函数的构造**：对于一个不可解的函数，通过求梯度等方法消掉不可解部分，再去掉梯度找到一个可解的代理损失函数
4. **log梯度技巧的作用**：乘法转加法简化计算，期望的梯度转成梯度的期望从而可以应用蒙特卡洛法

---

**后记**  
这篇文章一气呵成，开个人公式推导文章之先河。里边的推导很难理解，但思考起来又如痴如醉。在去青岛团建的火车上思考，在信号山顶的咖啡馆思考，在小麦岛的草坪上思考。就当我以为自己已经理解了整个过程，开始提笔写这篇文章的时候，还有些犹豫要不要写，因为编辑公式真的很繁琐。但写的过程中才发现，有太多我以为理解的细节实际上漏洞百出，根本就没有理解。这让我诚惶诚恐，之前囫囫囵囵吞枣看过的书，恐怕也不过只理解了三四成吧。同志仍需努力啊！