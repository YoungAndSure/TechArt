#### 什么是funtional/泛函数？  
这会儿简单理解，就是函数的函数  

#### note
supervised learning包含classification problem和regression problem.监督学习是说样本里有输入向量和对应的目标向量。分类问题输出是离散变量，回归输出是连续变量。  
回归一次的来源是研究两代人身高，发现下一代会趋于平均值，这个趋于平均值叫回归regression。没想清楚怎么跟这里的回归对应上的。  

#### note
只有输入向量，没有目标向量的是unsupervised learning。包含clustering和density estimation。聚类是把点分类，回答这个点属于哪个分类的问题。密度估计是得出点的分布。

#### note
很高兴又看到credit assignment problem,之前读mfrl时候只get到了explorition和exploitation问题，没有意识到信用分配的问题。信用分配说的是，如何把reward合理分配到action的问题。一个回合结束后得到轨迹的return，这个回合中那么多action，哪个对这个return贡献多？哪个对这个return贡献少？需要有个分配，credit assignment problem讨论的就是如何分配的问题。

#### note
有意思，为什么多项式里的$x$明明是$M$阶的，这种模型还叫linear model?因为从参数$w$的角度看，是线性的，本来要调整的也是$w$，所以这个叫linear model。  

#### note
Figure1.4: 多项式阶数过高，就是过拟合，泛化能力一定下降。拟合能力和泛化能力就是互斥的一对，有你没我有我没你。  

#### 均方误差(RMS)和平方误差和比，有什么区别？  
平方误差和：  
$E(\mathbf{w}) = \sum_{n=1}^N\{y(x_n, \mathbf{w}) - t_n\}^2$  
均方误差：  
$E_{RMS}(\mathbf{w}) = \sqrt{2E(\mathbf{w})/N}$  
$N$可以消去数据集大小的影响，让不同数据集之间可比。  
$\sqrt{}$让误差落回和目标$t$一样的尺度，可以和$t$来比较看差异。  
有道理啊，三阶多项式是九阶多项式在高阶系数等于=0时的特例，九阶多项式的表达能力应该强于三阶。况且，模拟数据通过$\sin(2\pi x)$生成，无穷阶的二项式可以逼近$\sin(2\pi x)$，所以阶数越多，越能逼近才对。为什么反倒九阶的拟合效果还不如三阶呢？  
写到这我还没看下边的内容，盲猜一下为什么。  
限制九阶泛化能力的是数据而不是九阶本身。如果数据足够多，九阶肯定比三阶好，无穷阶更好。数据给的信息不全，目标没有指向$\sin(2\pi x)$，所以九阶能力强但学的方向错了。  
答对了。不过这也挺好理解，数据越多，噪声的影响就越少，就越能学到真实的分布。  
  
最终是说，数据量必须得是参数量的一个倍数时候，才不会过拟合。  
然后作者装了个逼，说，最小二乘不过是最大似然的一个特例，过拟合是最大似然的普遍问题，而从贝叶斯的视角出发，贝叶斯模型不要求参数量和数据量的关系，会自动选择参数量。  
听着就牛逼。  

#### note
Note that often the coefficient w0 is omitted from the regularizer because its inclusion causes the results to depend on the choice of origin for the target variable, or it may be included but with its own regularization coefficient.  
英语角度，没意识到inclusion是个名词，是its inclusion，包含它，而不是个动词。  
算法角度。  
首先，什么是正则化(regularizer)？
书里说的是，为了防止过拟合，给损失函数加了个惩罚项，限制参数太大，这个是正则化。  
扩大一下，所有解决过拟合问题的技术都属于正则化范畴。  
然后，这里说的是为什么正则化的时候一般不处理$w_0$。  
$w_0$是多项式里的常数项，控制的是拟合函数曲线的平移。对这个项进行惩罚，限制它的大小，等于限制了拟合函数曲线的平移。其他参数，控制的是曲线的形状。而正则化要解决的是，参数过大，导致曲线形状扭曲去适配噪声数据的问题，要解决的是让曲线形状不要那么的适配输入数据，重点调整的应该是影响曲线形状的参数。限制调整$w_0$不能解决曲线形状的问题。  
另外，限制调整$w_0$导致曲线需要平移变更基线时受阻，其他参数为了损失函数最小会在基线错误的情况下拟合，得到更差的拟合效果。  

#### 为什么公式里用$\lambda$，但图例里用$\ln \lambda$?  


#### We see that in effect λ now controls the effective complexity
of the model and hence determines the degree of over-fitting.effective什么意思？  
effective complexity of the model，模型的有效复杂度。$\lambda$通过限制$w$的大小，实际限制了多项式的表达范围，也就是有效复杂度，强迫模型用更简单的曲线来拟合数据。  
in effect，翻译为实际上  
看来，这书里有的句子看不懂有两种原因，一种是单词不会，一种是其中蕴含的概念不明白。每句都不可大意。  

#### Here we simply note that, if we were trying to solve a practical
 application using this approach of minimizing an error function, we would have to find a way to determine a suitable value for the model complexity. The results above suggest a simple way of achieving this, namely by taking the available data and partitioning it into a training set, used to determine the coefficients w, and a separate validation set, also called a hold-out set, used to optimize the model complexity (either M or λ). In many cases, however, this will prove to be too wasteful of valuable training data, and we have to seek more sophisticated approaches.
训练集和验证集都用的一个带了正则化的损失函数。  
训练集只能得出损失函数最小，无法评估泛化能力，验证集独立于训练集，用来评估泛化能力。由于不确定参数M和lambda的取值，需要在训练集上取各种值进行训练，在验证集上看哪个效果最好。

#### Now suppose we randomly pick one of the boxes and from that box we
 randomly select an item of fruit, and having observed which sort of fruit it is we replace it in the box from which it came.  
 replace：放回，不是替换的意思  

#### and that when we remove an item of fruit from a box we are equally likely to select any of the pieces of fruit in the box.  
remove这里是取出的意思，短暂的去除。  
equally likely，等可能  

#### the identity of the box 
反正和the box不同，难准确翻译。  

#### we shall define the probability of an event to be the fraction of times that event occurs out of the total number of trials, in the limit that the total number of trials goes to infinity.  
the fraction of times, 次数的比值，这个要整体看  
out of : 解释前面比值到底是哪个和哪个  
in the limit : 表示一种极限条件， goes to infinity，说明具体是什么极限  

#### We can answer questions such as these, and indeed much more complex questions associated with
problems in pattern recognition, once we have equipped ourselves with the two elementary rules of probability, known as the sum rule and the product rule.  
indeed: 这里的意思是"甚至"  
equipped: 掌握  

#### $p(X|Y)$  
很基础的概念，但看着看着就混淆了。因为公式简化了，很多信息很容易忽略。  
$P(X|Y)$是个随机"变量"，不是具体值。因为$X$可以取各种值$x_i$。  
$p(X)=p(X|Y)p(Y)$，首先，展开成一个具体的取值，更容易理解：  
$p(X=x_i)=p(X=x_i|Y=y_j)p(Y=y_j)$  
翻译：$p(X=x_i|Y=y_j)$是把$Y=y_j$事件的点全都圈出来作为分母，然后挑出$X=x_i$事件的点作为分子，相除。这里分子分母还挺明确的。$p(Y=y_j)$比较狗的一点是，隐含了分母是什么。$p(Y=y_j)$的分母是全体样本，包含所有$X=x_*$和$Y=y_*$的样本，分子是其中$Y=y_j$的事件数量。  
