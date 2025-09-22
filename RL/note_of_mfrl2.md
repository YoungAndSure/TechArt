#### 附录B：测度论概率论
测度论是一个更高维度、更大范围的理论，测度理论概率论是其中一个分支，概率论套用了测度论的一些理论来描述概率论问题。  

##### 概率三元组
-样本空间$`\Omega`$，包含了所有可能发生的结果，其中元素是$`\omega`$。  
-事件域$`\mathcal{F}`$,样本空间中所有元素的组合中，满足$`\sigma`$-algebra条件的子集。其中元素是事件$`A`$。  
-概率测度$`\mathbb{P}`$，从$`\mathcal{F}`$到[0,1]的映射。  
> $`\mathcal{F}`$中有很多事件，他们的概率测度$`\mathbb{P}`$在[0,1]之间。分母是样本空间$`\Omega`$，而不是$`\mathcal{F}`$。比如$`\mathcal{F}`$中有一个事件$`A=\Omega`$,它的概率测度$`\mathbb{P}(A)=1`$。  

> $`\mathcal{F}`$的存在是为了限定要分析的对象。" it is a σ-algebra (or σ-field) of
Ω"。  

##### 随机变量
随机变量就是将$`\Omega`$中的样本映射到实数空间$`\mathbb{R}`$的"方法"。  
但并非所有映射都是随机变量。映射必须满足：  
对于任意实数$`x\in\mathbb{R}`$,小于$`x`$的映射$`X(\omega)`$也属于事件域$`\mathcal{F}`$。  
公式：$`A=\{\omega\in\Omega|X(\omega)<=x\}\in\mathcal{F}`$  
>这里<=和限制$`\mathcal{F}`$都有含义。<=感觉是一种可加性，限制$`\mathcal{F}`$是防止突破三元组中$`\mathcal{F}`$的讨论范畴。具体不太明白。  

##### 随机变量的期望
>这段公式太牛逼了，看得我一愣一愣的  

先给随机变量的定义：  
$`X(\omega) = \sum_{x\in\mathcal{X}}x \mathbb{1}_{A_{x}}(\omega)`$  
随机变量就是样本空间$`\Omega`$到实数空间$`x\in\mathbb{R}`$的映射，记为$`X`$。所以可以看到这个公式里，左边输入是样本空间中某样本$`\omega`$，经过映射$`X`$变换后，右边是一个对实数$`x`$的运算。  
比较奇葩的是这个函数，这个符号叫指示函数：  
$`\mathbb{1}_{A_{x}}(\omega)\doteq\left\{\begin{array}{ll}
1, &\omega\in A_{x},\\
0, &\text{otherwise.}
\end{array}\right.`$  
这个函数输入是样本$`\omega`$和一个集合$`A_x`$，如果$`\omega`$在集合$`A_x`$中，输出值为1，否则为0.说白了，就是判断$`\omega`$在不在集合$`A_x`$中。  
所以$`A_x`$是个啥？这定义也挺绕的：  
$`A_x=\{\omega \in \Omega|X(\omega)=x\}=X^{-1}(\omega)`$  
这个集合，是样本$`\omega`$的集合。其中的样本，通过随机变量$`X`$映射后的值为$`x`$。注意，这里的映射是多对一的，也就是多个$`\omega`$可能映射到一个$`x`$。这些$`\omega`$组成了一个集合叫$`A_x`$。最右边的一项是另一种解释，$`X`$不是把$`\omega`$映射到$`x`$了吗，$`^{-1}`$是逆运算，就是反过来，给$`x`$映射回$`\omega`$。  
给个图说明下：  
![图片描述](./images/random_variables.png)  
所以，$`X(\omega_1)`$是多少？嗯，就是$`x`$，但是根据公式你得绕一圈才能得到这个答案。  
遍历所有样本$`\omega`$，能映射为$`x`$的有三个：$`\omega_1`$, $`\omega_2`$, $`\omega_3`$.所以$`A_x=\{\omega_1,\omega_2,\omega_3\}`$。$`1_{A_x}(\omega_1)=1`$，因为$`\omega_1`$在$`A_x`$里。  
对所有$`x\in\mathcal{X}`$加和，因为只有$`\omega_1`$这一项的$`1_{A_x}(\omega_1)=1`$，所以$`X(\omega)=x`$。  
>听着很脱了裤子放屁，但是这个定义是个更高维的框架，是一种看问题的方式，更本质些。  
  
然后是期望。  
期望是什么？一个值和它出现的概率加权求和。  
现在要计算一个随机变量的概率，那就是这个随机变量的值$`x`$和发生的概率。  
根据前面的定义，某个随机变量取值$`x`$发生的概率是多少呢？$`x`$对应样本空间中映射到$`x`$的样本的集合是$`A_x`$。所以$`x`$发生的概率就是$`A_x/\Omega`$。  
看上图的例子，右侧$`x`$由左侧$`\omega_1,\omega_2,\omega_3`$映射而来，所以概率就是$`\omega_1,\omega_2,\omega_3`$比上样本空间全体$`\Omega`$。  
这只是一个取值$`x`$和它的概率的加权，扩展到所有取值就是：  
$`\mathbb{E}(X)=\sum_{x\in\mathcal{X}}x \mathbb{P}(A_x)`$  
  
另外，这会儿不知道有什么用，书上说，指示函数$`\mathbb{1}_{A}`$也可以看作一个随机变量。确实，它把在$`A`$里的$`\omega`$映射成1，不在的映射成0，满足随机变量的定义。  
且，$`\mathbb{E}(\mathbb{1_{A}})=\mathbb{P}(A)`$  
就这么想。$`\mathbb{1_{A}}`$由两部分组成，一部分是在$`A`$里的，随机变量是1，一部分是不在$`A`$里的，随机变量是0.随机变量是0的，就不用考虑了，所以只考虑在$`A`$里这部分样本$`\omega`$。这部分概率是多少呢？每一个样本$`\omega`$的概率都是$`\frac{1}{\Omega}`$，乘值1之后还是$`\frac{1}{\Omega}`$。$`A`$里所有这样的$`\omega`$加一起，就是$`\frac{A}{\Omega}`$,这不就是$`\mathbb{P}(A)`$吗。  

##### 随机变量条件期望
$`X,Y,Z`$是三个随机变量。提出了三种情况，理解一下：  
Case1: $`\mathbb{E}[X|Y=2]`$是一个数字。按照上面随机变量的定义，这么理解。$`X,Y`$其实都是个映射。所谓条件$`Y=2`$就是说，把样本空间中所有的$`\omega`$都通过$`Y`$映射到$`\mathcal{Y}`$，其中映射结果等于2的那些个$`\omega`$组成的集合。相当于在样本空间$`\Omega`$里画了个小圈。在这个小圈里，对$`\omega`$执行$`X`$映射，会映射到$`\mathcal{X}`$中。然后，计算$`X`$映射后的值及概率，求期望，得到的是一个数。这个求概率的过程跟上文说的一致，只是此时分母不是$`\Omega`$了，而是$`Y=2`$的这些$`\omega`$组成的集合。  
![图片描述](./images/conditional_expectation.png)
>"概率就是面积"，这句话的含金量还在上升  

Case2:$`\mathbb{E}[X|Y=y]`$是一个$`y`$的函数。扩展一下case1，上边$`Y=2`$是划定了一个小圈，如果把2变成一个变量$`y`$呢？这个圈就随着$`y`$的变化而变化。由于$`X`$的作用对象是$`Y`$划定的这个小圈，所以$`X`$的期望自然也随着$`y`$的变化而变化。期望也是如此。最后就变成了一个$`y`$的函数。  
Case3:$`\mathbb{E}[X|Y]`$是一个随机变量。这个有点抽象。凑合这么理解。上边两个case，都通过$`Y=?`$圈定了$`X`$在$`\Omega`$的作用域。但Case3没有圈定，所以，它的作用范围就是整个$`\Omega`$。这么想，整个$`\Omega`$里，有两个映射，分别把所有的$`\omega`$映射到实数域。如果这两个映射，完全没有关系，或者说独立，或者说$`Y`$把一个$`\omega`$映射成2和$`X`$把同一个$`\omega`$映射成5没有依赖关系的话，那其实计算$`X`$的期望就跟$`Y`$没关系，所以就是$`\mathbb{E}(X|Y)=\mathbb{E}(X)`$，结果就是个实数。如果$`Y`$把一个$`\omega`$映射成2时$`X`$把同一个$`\omega`$映射成5，$`Y`$把一个$`\omega`$映射成3时$`X`$把同一个$`\omega`$映射成6，这样，$`X`$把一个$`\omega`$映射成谁跟$`Y`$的映射结果有依赖关系的话，那$`X`$和$`Y`$就不是独立的。这时候，计算$`X`$的期望，就依赖随机变量$`Y`$了，所以它是随机变量$`Y`$的函数，还是个随机变量。  
> 有的事/概念理解不好，其实是底层逻辑没有构建好。当底层逻辑构建好、运用好之后，那些结论是可以自己分析出来的。  

##### 随机变量期望性质  
$`\mathbb{E}[X|Y]`$和$`\mathbb{E}[X|Y=y]`$有什么区别？为什么明明他们不等价，但是证明里却老提后者？  
前者是个随机变量，你不知道$`Y`$会取哪个值。后者已经确定要取$`y`$了，虽然它也是个变量，但总之是不随机了。书里的讨论都是证明对于"every y"满足某性质，也就意味着$`Y`$满足某性质了  
(a)$`\mathbb{E}[a|Y]=a`$  
这是一个有关Y的函数，假设$`Y=y`$  
$` \mathbb{E}[a|Y=y]=\sum_x x*p(a=x|Y=y)= a*p(a|Y=y)=a `$  
这里开始证明我犯了一个错误，误以为$`Y`$是个没有被确定值限定范围的随机变量，所以按照定义应该展开成：$`\mathbb{E} [ a|Y ] =\sum_y yp(a|y)`$。一个显然的反驳点就是，上面说$`\mathbb{E}[X|Y=y]`$是个$`y`$的函数，如果$`y`$展开了，就没有$`y`$了，那就变成常数了，与前论相悖。所以$`\mathbb{E}[X|Y]`$应该理解成，$`Y`$是用来圈定范围的，$`X`$才是要展开求的值。所以无论何时都要用$`X`$展开，$`Y`$只能是个变量。  
(b)$`\mathbb{E}[aX+bY]=a\mathbb{E}[X]+b\mathbb{E}[Y]`$  
期望的线性性质  
(c)$`\mathbb{E}[X|Y]=\mathbb{E}[X],如果\ X,Y 独立`$  
```math
\begin{align}
\mathbb{E}[X=y|Y=y]&=\sum_x x*p(X=x|Y=y)\\
&= \sum_x x*\frac{p(X=x,Y=y)}{p(Y=y)}\\
&= \sum_x x*\frac{p(X=x)p(Y=y)}{p(Y=y)}\\
&= \sum_x x*p(X=x)\\
&= \mathbb{E}[X]
\end{align}
```
(d)$`\mathbb{E}[Xf(Y)|Y]=f(Y)\mathbb{E}[X|Y]`$  
对每一个$`y`$：
```math
\begin{align}
\mathbb{E}[Xf(Y=y)|Y=y]&=\sum_x xf(Y=y)p(X=x|Y=y)\\
& f(y)跟x无关，可以从加和里提出来，但p(x|y)跟x是相关的\\
&= f(Y=y) \sum_x xp(X=x|Y=y)\\
&= f(Y=y)\mathbb{E}[X|Y=y]
\end{align}
```
(e)$`\mathbb{E}[f(Y)|Y]=f(Y)`$  
直接套用(a)  
(f)$`\mathbb{E}[X|Y,f(Y)]=\mathbb{E}[X|Y]`$  
对每一个y  
```math
\begin{align}
\mathbb{E}[X|Y=y,f(Y=y)]&=\sum_x xp(x|y,f(y))\\
& y确定了，f(y)也就确定了，所以p(x|y,f(y))=p(x|y)=p(x|f(y))\\
&= \sum_x xp(x|y)\\
&= \mathbb{E}[X|Y=y]
\end{align}
```
(g) if X > 0,$`\mathbb{E}[X|Y]>0`$  
(h) if X > Z, $`\mathbb{E}[X|Y]>\mathbb{E}[Z|Y]`$  
$`\mathbb{E}[X|Y=y]=\sum_x xp(x|Y=y)`$  
这个证明，同贝尔曼最优方程里最优行动的证明。  

##### 随机变量期望2 
(a) $`\mathbb{E}[\mathbb{E}[X|Y]]=\mathbb{E}[X]`$  
首先，$`\mathbb{E}[X|Y]=f(Y)`$,因为它是随机变量$`Y`$的函数。  
```math
\begin{align}
\mathbb{E}[\mathbb{E}[X|Y]] &= \mathbb{E}[f(Y)]\\
&= \sum_y f(y) p(f(Y=y))\\
& y确定了，f(y)也就确定了，所以p(f(y)) = p(y)\\
&= \sum_y f(y) p(y)\\
&= \sum_y \mathbb{E}[X|Y=y]p(y)\\
&= \sum_y \sum_x xp(x|y)p(y)\\
&= \sum_y \sum_x x p(x,y)\\
&= \sum_x x \sum_y p(x,y)\\
&= \sum_x x p(x) \\
&= \mathbb{E}[X]
\end{align}
```
这么理解，里层Y相当于圈定了一部分样本，求这部分样本X的期望。然后又求整体样本对于Y的期望，其实就是求整体样本X的期望。  

(b) $`\mathbb{E}[\mathbb{E}[X|Y,Z]]=\mathbb{E}[X]`$  
(c) $`\mathbb{E}[\mathbb{E}[X|Y]|Y]=\mathbb{E}[X|Y]`$  
类似(a)可证。  

##### 随机收敛定义
这里的收敛说的不是下意识想的，一个实数序列最终会收敛到一个实数值。  
这里的收敛说的是随机变量也就是从样本$`\omega`$到$`x`$的映射方法收敛。涉及两个维度：  
1. 对哪些样本收敛？  
2. 收敛到什么程度？  

下边逐个总结下

- Sure convergence  
```math
A=\Omega, where A=\{\omega \in \Omega:\lim_{k \to \infty} X_k(\omega) = X(\omega)\}
```
收敛的范围是全体$`\omega`$，收敛的程度，是：收敛到映射$`X`$。这是约束最强的收敛。  

- Almost sure convergence  
```math
\mathbb{P}(A)=1, where A=\{\omega \in \Omega:\lim_{k \to \infty} X_k(\omega) = X(\omega)\}
```
注意，和Sure convergence的区别是收敛范围，不再是全体样本，而是收敛范围内样本概率为1.有些事件，发生的概率趋近于0.这些事件不收敛。  

- Convergence in probability  
```math
\lim_{k\to\infty}\mathbb{P}(A)=0, where A=\{\omega \in \Omega:|X_k(\omega)-X(\omega)|>\epsilon\}
```
这个是说，那些不收敛的样本，发生概率随着k增加趋近于0。约束的不是哪些样本收敛，而是那些不收敛的样本发生的概率。  

- Convergence in mean  
```math
\lim_{k\to\infty}\mathbb{E}[|X_k-X|^r]=0
```
约束了随机变量的期望和方差一致。  

- Convergence in distribution
```math
\lim_{k\to\infty}\mathbb{P}(X_k\leq a) = \mathbb(X\leq a)
```
$`\mathbb{P}(X_k\leq a)`$是$`X_k`$在样本空间上的概率分布累积值。也就是映射的概率分布收敛。  

#### 附录C：确定性序列收敛  
这下不是随机变量序列了，是实数序列。收敛就是实数序列的值会收敛到某个实数。  
##### 单调序列收敛  
两个条件：  
- 非递增，即$`x_{k+1} \leq x_k`$  
- 有下界，即$`x_k\geq\alpha, for\ all\ k`$  

则$`\{x_k\}`$收敛。反之：
- 非递减，即$`x_{k+1} \geq x_k`$
- 有上界，即$`x_k \leq \alpha, for\ all\ k`$  

也收敛。

##### 非单调序列收敛
对于非负序列$`x_k>0`$，如果$`\sum_{k=1}^\infty(x_{k+1}-x_k)^+\lt \infty`$，则$`\{x_k\}`$收敛  
这个看着简单，涉及的概念还挺多。  
这个右上角的$`^+`$是说，大于等于0的保留，小于0的用0替换。$`^-`$同理  
对$`x_k`$分解：  
```math
\begin{align}
x_k &= x_k - x_{k-1}+x_{k-1}-x_{k-2}+x_{k-2}...x_3-x_2+x_2-x_1+x_1\\
&=\sum_{i=1}^{k-1}(x_{i+1}-x_i) + x_1\\
&=S_{k}+x_1
\end{align}
```
说白了，就是求序列中每个元素和上一个元素的差值，全都加到$`x_1`$上，就是$`x_k`$。条件中的$`\sum_{k=1}^\infty(x_{k+1}-x_k)^+\lt \infty`$就是对差值序列中正的部分求和进行约束。  
- 证明一：有界  
差值序列按照正负可以分成两个序列和：  
$`S_k^+=\sum_{k=1}^\infty(x_{k+1}-x_k)^+`$  
$`S_k^-=\sum_{k=1}^\infty(x_{k+1}-x_k)^-`$  
$`S_k=S_k^++S_k^-`$  
所以：  
$`x_k=S_k+x_1=S_k^++S_k^-+x_1 \geq 0`$  
也就是：  
$`S_k^-\geq -S_k^+-x_1`$  
如果$`S_k^+=\sum_{k=1}^{k-1}(x_{k+1}-x_k)^+\lt \infty`$  
$`S_k^- \gt -\infty`$  
也就是$`S_k^-`$是有下界的。  
所以只要约束了$`\sum_{k=1}^\infty(x_{k+1}-x_k)^+\lt \infty`$，也就约束了$`\sum_{k=1}^\infty(x_{k+1}-x_k)^-\gt \infty`$,也就是差值序列里的非负和和非正和都是有界的。  
- 证明二：非递增/非递减  
然后，根据$`S_k`$的定义可以得出，$`S_k`$是非递减的(都是正数或0，肯定是增长或不变)。
- 结论：  
$`x_k`$收敛于$`S_k^+ + S_k^- + x_1`$  

##### 推论：非单调序列收敛  
对非负序列$`x_k \geq 0`$，有$`x_{k+1}\leq x_k+\eta_k`$，如果$`\eta_k \geq 0 , \sum_{k=1}^\infty \eta_k \lt \infty`$,则序列$`\{x_k\}`$收敛。  
由于  
$`x_{k+1} \leq x_k+\eta_k`$  
所以  
$`\sum_{k=1}^\infty(x_{k+1}-x_k) \leq \sum_{k=1}^\infty(x_{k+1}-x_k)^+ \leq \sum_{k=1}^\infty \eta_k \lt \infty`$  
根据前面的推导，非递减且有上界，得出$`x_k`$收敛。  

#### 附录C：随机序列的收敛
依赖鞅定理  

##### 鞅定义
对于随机变量组成的序列，两个条件：
- 序列中的随机变量期望有界: $`\mathbb{E}[|X_k|] \lt \infty`$  
- 序列下一个随机变量的期望等于当前随机变量值：$`\mathbb{E}[X_{k+1}|X_k,X_{k-1},X_{k-2}...X_1]=\mathbb{E}[X_{k+1}|\mathcal{H}_k]=X_k`$  

第二个条件也就意味着随机变量的期望都是相等的，因为之前的推导：
$`\mathbb{E}[\mathbb{E}[X|Y]]=E[X]`$  
所以：  
$`\mathbb{E}[\mathbb{E}[X_{k+1}|\mathcal{H}_k]]=E[X_{k+1}]=E[X_k]`$  
  
错误理解：鞅的条件表明序列中的随机变量是相互独立的。  
因为看到$`E[X_{k+1}]=E[X_k]`$，下意识的认为随机变量之间是相互独立的。其实不然。  
如果$`X,Y`$相互独立，有$`\mathbb{E}[X|Y]=\mathbb{E}[X]`$，但定义中的条件是$`\mathbb{E}[X|Y]=X`$，两者不同。  
另一个理解方式，上文附录B已讨论，$`\mathbb{E}[X|Y]`$是个$`Y`$相关的随机变量，因此$`\mathbb{E}[X_{k+1}|\mathcal{H}_k]`$是个随机变量。或者说，$`\mathcal{H}_k`$圈定了样本范围，计算下一个随机变量$`X_{k+1}`$的期望，所以$`\mathbb{E}[X_{k+1}|\mathcal{H}_k]`$是随着$`\mathcal{H}_k`$的变化而变化的随机变量——另一个维度说明随机变量之间不是独立的，而是相关的。  
>这会儿也get不到这性质有什么用  

##### 下鞅
对于随机变量组成的序列，两个条件：
- 随机变量期望有上下界：$`\mathbb{E}[|X_k|]\lt\infty`$  
- $`\mathbb{E}[X_{k+1}|\mathcal{H_k}]\geq X_k`$  

跟鞅不同的就是$`\mathbb{E}[X_{k+1}|\mathcal{H_k}]\geq X_k`$，通过$`\mathbb{E}[\mathbb{E}[X|Y]]=E[X]`$也可以导出：  
$`\mathbb{E}[X_{k+1}]\geq \mathbb{E}[X_{k}] \geq \mathbb{E}[X_{k-1}]...\geq \mathbb{E}[X_1]`$  
也就是随机变量序列的期望是非递减的。  

##### 上鞅
和上鞅相反，随机变量序列的期望是非递增的。  

>这个定义的名词确实容易懵逼。上鞅super，是递减的，下鞅sub是递增的。  

##### 鞅收敛
上鞅和下鞅会almost surely收敛到一个随机变量$`X`$。  

##### 拟鞅
上面确定性序列通过约束相邻元素差的和，导出收敛。  
鞅的约束得以让随机变量序列的期望有了类似确定性序列的性质。  
因此，拟鞅这里结合了两者，通过对随机变量序列相邻元素的期望差的和进行约束，导出收敛。  
类似上文的$`S_k^+,S_k^-`$，这里也要有对应的正向、负向表示：  
```math
\mathbb{1}_{A_{k}}=\left\{\begin{array}{ll}
1, & \mathbb{E}\left[X_{k+1}-X_{k} \mid \mathcal{H}_{k}\right] \geq 0, \\
0, & \mathbb{E}\left[X_{k+1}-X_{k} \mid \mathcal{H}_{k}\right] < 0.
\end{array}\right.
```
这个就相当于确定性序列界的$`S_k^+`$。注意$`\mathbb{E}[X_{k+1}-X_{k} \mid \mathcal{H}_{k}]`$：  
- 它是个有关$`\mathcal{H}_k`$的随机变量，可取范围内的实数值。  
- 它是对$`X_{k+1}-X_{k}`$求期望。这是相邻随机变量的差值。  

为什么$`\mathbb{1}`$后面要跟个$`A_k`$，且类似$`S_k^-`$的公式用$`\mathbb{1}_{A_k^c}`$表示？  
因为$`\mathbb{E}[X_{k+1}-X_{k} \mid \mathcal{H}_{k}]`$是个随机变量，$`\mathbb{E}[X_{k+1}-X_{k} \mid \mathcal{H}_{k}] \geq 0`$的含义是取随机变量值大于0的部分，实际就是圈定了样本空间$`\Omega`$中的部分样本组成一个集合，也就是$`A_k`$：  
$`A_k=\{\omega\in\Omega, \mathbb{E}[X_{k+1}-X_{k} \mid \mathcal{H}_{k}] \geq 0\}`$
所以，它的另一面是补集。  
  
拟鞅收敛：  
对于非负随机变量序列$`\{X_k\geq0\}`$,满足:  
$`\sum_{k=1}^\infty\mathbb{E}[(X_{k+1}-X_k)\mathbb{1}_{A_k}]\lt\infty`$  
则随机变量序列收敛。  
类似确定性非单调非负序列的收敛，增加上界约束，则下界也受约束，从而导向收敛。  

#### Dvoretzky’s convergence theorem
RM算法：
序列$`w_{k+1}=w_k-a_k(g(w_k)+\eta_k)`$收敛到$`g(w)`$的根$`w^*`$,如果$`g(w),a_k,\eta_k`$满足约束。  
这里Dvoretzky收敛是RM算法更高一层的理论，通过Dvoretzky收敛可以导出RM的收敛。  

>这段条件过多了，理解有限，几乎是照葫芦画瓢重写一遍  
后来，我问了一个问题：为什么是$`\mathbb{E}[\eta_k|\mathcal{H}_k]=0`$而不是$`\mathbb{E}[\eta_k]=0`$?打开了理解的大门。  
所以，问：为什么不是，比问，为什么是，能获取到的信息要更多。  

Dvoretzky迭代公式：  
$`\triangle_{k+1}=(1-\alpha_k)\triangle_k+\beta_k\eta_k`$  
约束：  
- $`\alpha_k`$:$`\sum_{k=1}^\infty \alpha_k = \infty, \sum_{k=1}^\infty \alpha_k^2 \lt \infty`$,同RM算法里说的，不能太慢也不能太快  
- $`\beta_k`$:$`\sum_{k=1}^\infty \beta_k^2 \lt \infty`$  
- $`\eta_k`$:$`\mathbb{E}[\eta_k|\mathcal{H}_k]=0,\mathbb{E}[\eta_k^2|\mathcal{H}_k]\leq C`$，$`\mathcal{H}_k=\{\triangle_k...\alpha_{k-1}...\beta_{k-1}\...\eta_{k-1}\}`$,总之，就是前面所有的随机变量  
- 都是almost surely  

满足约束时，$`\triangle_{k+1}\to 0`$ almost surely

这条件太多，初看平平无奇，细看处处玄机：  
- 发现和RM的差异没。RM是收敛到根，也就是$`w_k`$收敛到$`g(w_k)=0`$时的$`w^*`$，而Dvoretzky这里是收敛到$`\triangle_{k+1}=0`$。所以$`\triangle_{k+1}`$就是$`g(w)`$的更宽泛表示吗？不是，$`\triangle_{k+1}`$表示的是当前点到根的距离,也就是$`\omega_{k+1} - \omega^*`$。当$`\triangle_{k+1}`$收敛到0时，$`\omega`$收敛到$`\omega^*`$。可是迭代公式里没有$`\omega`$啊？初始值$`w_1`$是随机选的，是个随机变量，收敛后的值$`w^*`$也可以认为是一个随机变量，需要构造$`\triangle_k=\omega_1-\omega_k`$并分析其中的随机变量是否满足约束，来证明是否能收敛到根。  

- 为什么是$`\mathbb{E}[\eta_k|\mathcal{H}_k]=0`$而不是$`\mathbb{E}[\eta_k]=0`$?需要细究一下两者的含义区别。先说什么时候两者相等呢？相互独立的时候，$`\mathbb{E}[\eta_k|\mathcal{H}_k]=\mathbb{E}[\eta_k]`$，也就是当前的噪声$`\eta_k`$和过去的随机变量完全无关。所以$`\mathbb{E}[\eta_k|\mathcal{H}_k]=0`$比$`\mathbb{E}[\eta_k]=0`$的条件要宽松。前者没有要求完全独立，但独立也包含其中。独立是很严苛的条件，要$`\eta_k`$和过去的所有随机变量都无关是很难的。这里的条件是，可以相关，但期望是0，方差有界。含义就是：过去的随机变量对当前的噪声可以相关，可以有正的影响，也可以有负的影响，但总体归0，等于没有影响。否则，如果期望是正的或者是负的，就会导致过去对当前的噪声持续有影响，随着叠加，影响越来越大，最终难以收敛。  

- 既然$`\eta_k`$代表噪声，那$`\beta_k`$是干嘛的？类似$`\alpha_k`$对$`\triangle_k`$的调控，$`\beta_k`$是对噪声$`\eta_k`$的调控。它可以是一个确定性序列，也可以是依赖$`\mathcal{H}_k`$的随机变量。它跟$`\alpha_k`$不一样的一点是，不要求它$`\sum_{k=1}^\infty \beta_k=\infty`$。为啥呢？$`\sum_{k=1}^\infty \alpha_k=\infty`$，意味着当$`k\to\infty`$时，$`\alpha_k`$没有衰减到0，还能对$`\triangle_k`$产生作用。如果$`\alpha_k`$在某个点衰减到0，就意味着必须在这个点之前$`\triangle_k`$收敛到0才行，因为再之后$`\alpha_k`$不起作用了（这个在RM算法中也有证明）。但对于噪声$`\eta_k`$来说，肯定希望它越早衰减到0越好，如果不行，那也要限制它的增长范围。所以没有限制$`\sum_{k=1}^\infty \beta_k = \infty`$，只是限制了$`\sum_{k=1}^\infty \beta_k^2 \lt \infty`$。

#### Dvoretzky’s convergence theorem 证明
证明方法类似附录C里的收敛证明思路，通过构造相邻序列差，并约束差合的期望，来证明收敛。  
假设$`h_k=\triangle_k^2`$,则  
```math
\begin{align}
h_{k+1}-h_k&=\triangle_{k+1}^2-\triangle_k^2\\  
&=(\triangle_{k+1}+\triangle_k)(\triangle_{k+1}-\triangle_k)\\
&=[(1-\alpha_k)\triangle_k+\beta_k\eta_k+\triangle_k][(1-\alpha_k)\triangle_k+\beta_k\eta_k-\triangle_k]\\
&=[(2-\alpha_k)\triangle_k+\beta_k\eta_k][-\alpha_k\triangle_k+\beta_k\eta_k]\\
&=-\alpha_k(2-\alpha_k)\triangle_k^2-\alpha_k\beta_k\eta_k\triangle_k+(2-\alpha_k)\beta_k\eta_k\triangle_k+\beta_k^2\eta_k^2\\  
&=-\alpha_k(2-\alpha_k)\triangle_k^2+2(1-\alpha_k)\beta_k\eta_k\triangle_k+\beta_k^2\eta_k^2
\end{align}
```
加上期望：  
```math
\begin{align}
\mathbb{E}[h_{k+1}-h_k|\mathcal{H}_k]&=\mathbb{E}[-\alpha_k(2-\alpha_k)\triangle_k^2|\mathcal{H}_k]+\mathbb{E}[2(1-\alpha_k)\beta_k\eta_k\triangle_k|\mathcal{H}_k]+\mathbb{E}[\beta_k^2\eta_k^2|\mathcal{H}_k]
\end{align}
```
分析：
- $`\triangle_k`$包含在$`\mathcal{H}_k`$里，所以可以移出来  
- $`\alpha_k,\beta_k`$一般是$`\triangle_k`$函数，包含在$`\mathcal{H}_k`$里，或确定性序列，和$`\mathcal{H}_k`$无关，所以也可以移出来。  

所以：  
```math
\begin{align}
\mathbb{E}[h_{k+1}-h_k|\mathcal{H}_k]
&=-\alpha_k(2-\alpha_k)\triangle_k^2
+2(1-\alpha_k)\beta_k\triangle_k\mathbb{E}[\eta_k|\mathcal{H}_k]
+\beta_k^2\mathbb{E}[\eta_k^2|\mathcal{H}_k]
\end{align}
```
这么看，说白了只有$`\eta_k`$这个噪声是不确定因素，其他的其实都可以看作可控的变量，所以可以移出来。  

其中，条件$`\mathbb{E}[\eta_k|\mathcal{H}_k]=0`$是已经假定的，所以可以减掉一项：  
```math
\begin{align}
\mathbb{E}[h_{k+1}-h_k|\mathcal{H}_k]
&=\beta_k^2\mathbb{E}[\eta_k^2|\mathcal{H}_k]-\alpha_k(2-\alpha_k)\triangle_k^2
\end{align}
```
其中，条件$`\mathbb{E}[\eta_k^2|\mathcal{H}_k]\leq C`$是已经假定的，所以：  
```math
\beta_k^2\mathbb{E}[\eta_k^2|\mathcal{H}_k]\leq \beta_k^2C
```
又来一个假定：由于$`\sum_{k=1}^\infty \alpha_k^2 \lt \infty`$,所以$`\alpha_k \to 0`$，所以“不失一般性”，$`\alpha_k\leq 1`$。  
所以：  
```math
\begin{align}
-\alpha_k(2-\alpha_k)\triangle_k^2 &\lt 0\\
\beta_k^2\mathbb{E}[\eta_k^2|\mathcal{H}_k]-\alpha_k(2-\alpha_k)\triangle_k^2 &\leq \beta_k^2C\\
\mathbb{E}[h_{k+1}-h_k|\mathcal{H}_k]&\leq \beta_k^2C\\
\sum_{k=1}^\infty\mathbb{E}[h_{k+1}-h_k|\mathcal{H}_k]&\leq \sum_{k=1}^\infty\beta_k^2C \lt \infty
\end{align}
```

所以对于：
```math
\begin{align}
\sum_{k=1}^\infty\alpha_k(2-\alpha_k)\triangle_k^2
&=\sum_{k=1}^\infty\beta_k^2\mathbb{E}[\eta_k^2|\mathcal{H}_k]-\sum_{k=1}^\infty\mathbb{E}[h_{k+1}-h_k|\mathcal{H}_k]
\end{align}
```
等式右边两项都有界，所以左边也有界：  
```math
\sum_{k=1}^\infty\alpha_k(2-\alpha_k)\triangle_k^2 \lt \infty
```
且：
```math
\sum_{k=1}^\infty\alpha_k(2-\alpha_k)\triangle_k^2 \geq \sum_{k=1}^\infty\alpha_k\triangle_k^2 \geq 0
```
所以$`\sum_{k=1}^\infty\alpha_k\triangle_k^2`$有界。  
又因为$`\sum_{k=1}^\infty\alpha_k = \infty`$,所以必须有$`\triangle_k \to 0`$。
>这证明证的，各种假设。不是专家压根搞不清楚哪些是合理的，只能大概领略一下了。  
看这个证明过程，感觉是先有一个大概假设形式，然后去推导，推导最后必须满足的作为条件约束。  

#### Dvoretzky应用到均值估计  
回顾一下，均值估计是说，有一个随机变量$`X`$，现在得到一个采样序列$`x_1,x_2...x_k`$,现在要求它的期望$`\mathbb{E}[X]`$。一种是全部加和求平均值，一种是迭代式求解，方法是：  
```math
w_{k+1}=w_k + \alpha_k(x_k-w_k)
```
其中$`\alpha_k=\frac{1}{k}`$,满足$`\sum_{k=1}^\infty \alpha_k=\infty, \sum_{k=1}^\infty \alpha_k^2\lt\infty`$。  
现在要证明，以上迭代法可以收敛到$`\mathbb{E}[X]=w^*`$。  
上边也说了，Dvoretzky算法证明的是某点到目标点的收敛性，所以证明要先构造当前点到目标点的差，作为$`\triangle_k`$,于是：  
```math
\begin{align}
w_{k+1}-w^*&=w_k -w^* + \alpha_k(x_k-w^*+w^*-w_k)\\
w_{k+1}-w^*&=(w_k -w^*) + \alpha_k(x_k-w^*-(w_k-w^*))\\
\triangle_{k+1}&=\triangle_k+\alpha_k(x_k-w^*-\triangle_k)\\
\triangle_{k+1}&=(1-\alpha_k)\triangle_k+\alpha_k(x_k-w^*)
\end{align}
```
变形为Dvoretzky的形式，其中$`\alpha_k(x_k-w^*)`$部分的$`\alpha_k`$相当于标准公式中的$`\beta_k`$，$`x_k-w^*`$相当于标准公式中的$`\eta_k`$。  
$`\alpha_k`$无需赘言，完全满足Dvoretzky中的条件。$`\beta_k=\alpha_k`$也满足$`\sum_{k=1}^\infty \beta_k^2 \lt \infty`$的条件。  
然后看$`\eta_k`$是否满足条件：
```math
\begin{align}
\mathbb{E}[\eta_k|\mathcal{H}_k]&=\mathbb{E}[x_k-w^*|\mathcal{H}_k]\\
&=\mathbb{E}[x_k|\mathcal{H}_k]-\mathbb{E}[w^*|\mathcal{H}_k]\\
&=w^* - w^*\\
&=0
\end{align}
```
其中$`x_k`$的期望当然是$`w^*`$，$`w^*`$是个实数所以期望还是$`w^*`$。  
```math
\begin{align}
\mathbb{E}[\eta_k^2|\mathcal{H}_k]&=\mathbb{E}[(x_k-w^*)^2|\mathcal{H}_k]\\
&=\mathbb{E}[(x_k^2+(w^*)^2-2(w^*)x_k)|\mathcal{H}_k]\\
&=\mathbb{E}[x_k^2|\mathcal{H}_k]+\mathbb{E}[(w^*)^2|\mathcal{H}_k]-\mathbb{E}[2(w^*)x_k|\mathcal{H}_k]\\
&=\mathbb{E}[x_k^2|\mathcal{H}_k]+(w^*)^2-2(w^*)\mathbb{E}[x_k|\mathcal{H}_k]\\
&=\mathbb{E}[x_k^2|\mathcal{H}_k]+(w^*)^2-2(w^*)^2\\
&=\mathbb{E}[x_k^2|\mathcal{H}_k]-(w^*)^2
\end{align}
```
如果$`\mathbb{E}[x_k^2|\mathcal{H}_k]`$有界，则$`\mathbb{E}[\eta_k^2|\mathcal{H}_k]`$有界。  
综上，根据Dvoretzky定理，如果$`\mathbb{E}[x_k^2|\mathcal{H}_k]`$有界，通过$`w_{k+1}=w_k + \alpha_k(x_k-w_k)`$可以收敛到$`\mathbb{E}[X]`$。  

#### Dvoretzky定理证明RM算法  
回顾下RM算法。  
RM算法是说，有个未知函数$`g(w)`$，现在只能观察到带噪声的结果序列$`\tilde{g}(w_k)=g(w_k)+\eta_k`$，怎么根据这个$`\tilde{g}(w_k)`$来找到$`g(w)=0`$的解$`w^*`$。RM算法说：  
```math
w_{k+1}=w_k+a_k\tilde{g}(w_k)
```
且满足3个约束（下文证明时给出），通过不断迭代，就能找到$`w^*`$。  
现在通过Dvoretzky定理证明RM算法会收敛。  
同样的，构造从当前点到目标点的距离：  
```math
\begin{align}
w_{k+1}-w^*&=w_k-w^*+a_k\tilde{g}(w_k)\\
w_{k+1}-w^*&=w_k-w^*+a_k(g(w_k)+\eta_k)\\
&由于g(w^*)=0\\
w_{k+1}-w^*&=w_k-w^*+a_k(g(w_k)-g(w^*)+\eta_k)\\
\triangle_{k+1}&=\triangle_k+a_k(g(w_k)-g(w^*)+\eta_k)\\
&由于g(w_k)-g(w^*)=\nabla g(w')(w_k-w^*),w'\in[w_k, w^*]\\
\triangle_{k+1}&=\triangle_k+a_k(\nabla g(w')(w_k-w^*)+\eta_k)\\
\triangle_{k+1}&=\triangle_k+a_k(\nabla g(w')\triangle_k+\eta_k)\\
\triangle_{k+1}&=(1+a_k\nabla g(w'))\triangle_k+a_k\eta_k
\end{align}
```
RM的三个约束：  
(a) $`0<c_1<\nabla_w g(w)<c_2`$  
(b)$`\sum_{k=1}^\infty a_k > \infty`$且$`\sum_{k=1}^\infty a_k^2 < \infty`$  
(c)$`\mathbb{E}(\eta_k|\mathcal{H}_k)=0`$且$`\mathbb{E}(\eta_k^2|\mathcal{H}_k)<\infty`$  
根据约束可以得出：  
- 因为$`0<c_1<\nabla_w g(w)<c_2`$有界，所以$`a_k\nabla g(w')`$性质和$`a_k`$一致，根据RM条件(b),$`a_k\nabla g(w')`$满足Dvoretzky条件。  
- RM中$`a_k`$有界，满足Dvoretzky中$`\beta_k`$的条件  
- RM条件(c)对噪声的约束和Dvoretzky一致  

因此，根据Dvoretzky定理，RM算法收敛。  

#### Dvoretzky定理多变量拓展  
上面Dvoretzky定理，如果把$`\triangle_k,k=1,2...\infty`$当做一个带有随机噪声的序列，那定理证明了，只要其中的随机变量满足某些条件，$`\triangle_k`$可以收敛到0。如果把$`\triangle_k`$当做当前值和解之间的误差，则可以认为只要误差中的噪声满足某些条件，误差可以通过定理中的方法迭代最终降到0。  
~~这些都是针对一个序列，或者说一个问题的，用$`s`$表示。我们用集合$`\mathcal{S}`$代表多个序列或者说多个问题的集合。这些问题之间的随机变量和误差可能会相互干扰。在什么条件下，集合$`\mathcal{S}`$中的问题可以全部收敛呢？Dvoretzky定理的拓展就解答的这个问题。~~  
说不清楚这个多变量到底是什么含义了。我是觉得Dvoretzky定理是解了一个"收敛问题"，现在是有多个相互干扰又同时要收敛的"问题"。但是问deepseek又非说这不能叫问题。$`s`$是什么呢？书上说它是一个数，但是这个数干扰到随机过程收敛了吗？没有，我说它没有参与计算。书上又说，它是一个索引，这个倒是比较准确，它映射了一组随机变量($`\alpha_k(s),\beta_k(s),\eta_k(s),\triangle_k(s)`$)，通过迭代可以让$`\triangle_k(s)`$收敛。但是我能说，之前Dvoretzky是单索引，现在是多索引吗？不能。或者说，原来是单一变量，现在是多变量？那也不对吧，你还是可以说$`s`$是一个变量，不同的$`s`$映射到不同的一组随机参数，但随机参数组成的这个收敛的过程，到底叫什么呢？  
那就叫多随机过程收敛吧。  
在多随机过程中：  
```math
\triangle_{k+1}(s)=(1-\alpha_k(s))\triangle_k(s)+\beta_k(s)\eta_k(s)
```
其实针对单个随机过程$`s`$的迭代方式没变，变的是收敛成立的条件。  
条件是证明出来的，书里省略了，这里就也先省略，只做一个初步理解。  
(a)首先是熟悉的$`\sum_{k=1}^\infty \alpha_k(s)=\infty,\sum_{k=1}^\infty \alpha_k^2(s)\lt\infty,\sum_{k=1}^\infty \beta_k^2(s)\lt\infty`$,前面已经理解过了。新增了一个条件$`\mathbb{E}[\beta_k(s)|\mathcal{H}_k] \leq \mathbb{E}[\alpha_k(s)|\mathcal{H}_k]`$ almost surely。  
(b)针对噪声:$`||\mathbb{E}[\eta_k(s)|\mathcal{H}_k]||_\infty \lt \gamma||\triangle_k(s)||_\infty, \gamma \in (0,1)`$。  
(c)噪声方差约束：$`\mathrm{var}[\eta_k(s)|\mathcal{H}_k]\leq C(1-||\triangle_k(s)||_\infty)^2`$,C是常量。
  
说说几个我问过的问题吧。
- 多随机过程收敛只需要每个随机过程都满足Dvoretzky定理，不就可以都收敛了吗？为什么这里还需要单独的证明？  
如果多随机过程之间完全没有任何联系，那当然只需证明每个随机过程满足Dvoretzky条件就可以了。但这里的多随机过程之间是有联系的。其中的$`\mathcal{H}_k`$没有区分$`s`$，也就是包含了所有随机过程的历史信息。既然s间的历史随机变量可以互相干扰，那是否收敛就不能单独分别看待了。所以条件中多了$`||?||_\infty`$，含义是所s中取最大的。也就是说条件的约束，是整个集合S维度的。
- $`\mathrm{var}[X]`$和$`\mathbb{E}[X^2]`$什么关系？  
$`\mathrm{var}[X]=\mathbb{E}[X^2]-\mathbb{E}[X]^2`$,这俩可不是一个东西。方差才是衡量波动性的指标。  
- $`\alpha_k(s)`$和$`\beta_k(s)`$是人工设置的参数吗？  
是的，他们是留给人工调的参数，只要满足收敛的条件，就可以收敛。  
- 那该怎么设置呢？噪声是随机的，不可能和$`\triangle_k(s)`$分离，又怎么给它加上$`\beta_k(s)`$这样的调控系数呢？  
确实不能分离，这里只是公式化的理论分析。就像RM中让$`\tilde{g}(w_k)`$分解成$`g(w_k)+\eta_k`$一样，实际中是不能分离的，只是在公式上分离可以更好的分析噪声。$`\beta_k(s)`$也不是一个直接作用在$`\eta_k(s)`$上的系数，就像Dvoretzky证明RM算法一样，通过变形之后一些可调参数会转化成$`\beta_k(s)`$的形式，而不是上来对噪声设置一个系数然后调整。  

这个定理后面会用来分析强化学习算法的收敛。一个随机过程收敛对应强化学习中一个状态价值或行动价值。集合$`S`$的收敛对应所有状态价值或行动价值的收敛。  

#### 附录D:梯度下降
>以为要讲梯度下降原理，跃跃欲试，结果研究的方面不一样。这里要研究的是，什么情况下可以用梯度下降，怎么判断能不能用，用了之后找到的是全局极值还是局部的，怎么判断能不能找到，梯度下降的步要设置多长...这些问题。这些问题确实和应用更贴近些。 

首先，什么情况下可以用梯度下降法找极值？引出凸集、凸函数的概念。  
##### 凸集
是一个集合，满足$`\mathcal{D}\in\mathbb{R}^n`$,集合中的任意元素$`x,y`$满足$`z=cx+(1-c)y \in \mathcal{D}, c\in[0,1]`$。  
集合$`\mathcal{D}`$就是个点集合。集合中的任意两点，连成一个直线，直线上的点就是$`cx+(1-c)y,c\in[0,1]`$，直线上的点也在集合$`\mathcal{D}`$里的，是凸集。  
写这么复杂(严谨)，其实意思挺简单，给两个示例：
![图片示例](./images/convex_set.png)  
这个圆及其中的点组成一个凸集$`\mathcal{D}`$。因为圆中任意两点连接的直线上的点都在圆中。
![图片示例](./images/not_convex_set.png)  
这个空心圆中的点组成一个集合。但集合中两点连线穿过了中间的非集合区域，所以不满足$`cx+(1-c)y`$的条件，不是一个凸集。

##### 凸函数  
从定义域$`\mathcal{D}`$到$`\mathbb{R}^n`$的映射，其中定义域$`\mathcal{D}`$是凸集，映射满足定义域中任意$`x,y, f(cx+(1-c)y)\leq cf(x)+(1-c)f(y)`$。  
注意不等式里包含等号，也就是直线也是凸函数。不等式的含义就是函数上任意两点$`(x,y)`$连线，函数上的[x,y]之间的点在连线之下。  
如图，是一个抛物线，就是一个凸函数。c=0.5。
![图片](./images/convex_func.png)

##### 类似抛物线这种明明是凹的，为什么叫凸函数
这个数学定义和日常生活就是反的。  
日常生活是以地面为参照，突出地面的叫凸，陷入地面的凹。  
凸函数的定义是"上帝视角"，从天上往下看。假如你是“上帝”，头朝地面站在云上，你的活动空间是大气层。你会觉得河谷是凸出大气层了，高山是凹进大气层了。  
所以，凸函数的凸是从函数上方往下看的视角。这时候$`y=x^2`$是凸出了。  

##### 为什么梯度下降要先定义凸集
定义凸函数我是理解的，因为没有凸函数，就没有最优点。但我开始没搞明白的是，凸函数为什么一定要定义在凸集上。  
>!!!注意，下边是错误理解  

我假设这么一个图形：  
![图片](./images/not_convex_set_with_parabola.png)  
空心圆蓝色部分是非凸集合$`\mathcal{D}`$，在集合中有一个抛物线，这个抛物线满足凸函数的定义。虽然抛物线在非凸集合内，但抛物线本身是可以找最小值的，这种问题为什么要排除在凸函数定义之外呢？  
仔细思考之后发现我的理解有误。  
注意看凸函数的定义，其中是函数定义域是个凸集，而不是定义域和值域均是凸集$`\mathcal{D}`$。对于图中抛物线来说，定义域$`\mathcal{D}`$是$`x\in [-4,4]`$,是一个连续的取值范围，满足取值范围内任意两点之间的点还在区间内的条件，因此是个凸集。因此，抛物线是个凸函数，没有被排除。  
什么样的函数的定义域是图中蓝色空心圆部分，从而不是凸函数呢？那需要再加一维，比如一个空心圆柱，这种函数由于定义域不是凸集，函数也不是凸函数，是不能找最小值的。  
  
>以下是正确理解  

凸集的定义是$`\mathbb{R}^n`$的子集$`\mathcal{D}`$。  
n=1的时候，$`\mathcal{D}`$是一维的，是个取值范围，或者说一条线段。  
n=2的时候，$`\mathcal{D}`$是二维的，是个平面。  
...  
当$`\mathcal{D}`$是定义域的时候，函数必然多一维。  

为什么要给定义域做凸集的限制呢？  
凸集其实意味着在集合内的任意两点之间是连续的，没有断层的。也就意味着凸函数的定义域一定是连续的。定义域中没有任何两点中的点是落在无意义的定义域之外的。  
因为梯度下降法是一种不断迭代找最小值的方法，如果定义域不连续，意味着在迭代过程中，可能落入定义域之外无意义的点，导致无法继续迭代，也就无法找最小值了。  
所以，为了应用梯度下降法，一定要是凸函数，而凸函数的定义域一定要连续，也就是凸集。  

