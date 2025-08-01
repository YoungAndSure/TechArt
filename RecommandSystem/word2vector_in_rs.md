# word2vector in RS

在推荐系统做了几年工程，总觉得知其然而不知其所以然，常常苦恼。近年陆续涉猎了深度学习、自然语言处理、强化学习的基本原理，再回过头来看推荐系统，多了一些理解。但是看推荐系统的最新论文，感觉理解还是不够深入，就是：你知道它用这个数据乘了那个数据，然后做了这个变换，但是为什么可以这样呢？为什么这样就能行呢？说不清楚。只知其表，不知其理，终究还是经不住推敲。  
  
追根溯源，读经典论文DNN，发觉，模型结构和CBOW有共通之处，文中也说借鉴了word2vector。再加上推荐系统的特点：巨大的嵌入表，足以说明，word2vector对推荐系统模型的影响之深。所以，还是要从word2vector理解起。  
  
而word2vector的前身是矩阵分解。  

## 自然语言处理的演化思路
### 矩阵分解
重读鱼书之三中一二章，发现写的不仅简单，还有一点误导。重新梳理总结下推导过程。

#### 如何表示一个词的含义？
分布假设：一个词的含义由上下文决定。  
"you say goodbye and i say hello"，say的含义由you和goodbye决定。上下文窗口是可以调整的，比如上例窗口为1.  
  
| word | contexts(window=1) | contexts(window=2) |
|------|---------------------|---------------------|
|you|say|say,goodbye|  
|say|you,goodbye|you,goodbye,and|
|goodbye|say,and|you,say,and,i|

以此类推

#### 如何在计算机中表示词关系
共现矩阵。  
```math
% 需引入 amsmath 宏包
A = \begin{pmatrix}
& \texttt{you} & \texttt{say} & \texttt{goodbye} & \texttt{and} & \texttt{i} & \texttt{hello} \\
\texttt{you}     & 0 & 1 & 0 & 0 & 0 & 0 \\
\texttt{say}     & 1 & 0 & 1 & 1 & 1 & 1 \\
\texttt{goodbye} & 0 & 1 & 0 & 1 & 0 & 0 \\
\texttt{and}     & 0 & 1 & 1 & 0 & 1 & 0 \\
\texttt{i}       & 0 & 1 & 0 & 1 & 0 & 0 \\
\texttt{hello}   & 0 & 1 & 0 & 0 & 0 & 0
\end{pmatrix}
```
不赘述书中内容了。

#### 如何表示词
词向量,直接从共现矩阵取出：
```math
% "you" 的词向量
\mathbf{v}_{\text{you}} = 
\begin{pmatrix}
0 & 1 & 0 & 0 & 0 & 0 
\end{pmatrix}
```
```math
% "say" 的词向量
\mathbf{v}_{\text{say}} = 
\begin{pmatrix}
1 & 0 & 1 & 1 & 1 & 1 
\end{pmatrix}
```
```math
% "goodbye" 的词向量
\mathbf{v}_{\text{goodbye}} = 
\begin{pmatrix}
0 & 1 & 0 & 1 & 0 & 0 
\end{pmatrix}
```
```math
% "and" 的词向量
\mathbf{v}_{\text{and}} = 
\begin{pmatrix}
0 & 1 & 1 & 0 & 1 & 0 
\end{pmatrix}
```
```math
% "i" 的词向量
\mathbf{v}_{\text{i}} = 
\begin{pmatrix}
0 & 1 & 0 & 1 & 0 & 0 
\end{pmatrix}
```
```math
% "hello" 的词向量
\mathbf{v}_{\text{hello}} = 
\begin{pmatrix}
0 & 1 & 0 & 0 & 0 & 0 
\end{pmatrix}
```

#### 如何计算词相似度
可以用余弦相似度：
```math
\mathrm{similarity}(\boldsymbol{x},\boldsymbol{y}) = 
\frac{ 
    \boldsymbol{x} \cdot \boldsymbol{y} 
}{ 
    \|\boldsymbol{x}\| \|\boldsymbol{y}\| 
} = 
\frac{ 
    x_1 y_1 + \cdots + x_n y_n 
}{ 
    \sqrt{x_1^2 + \cdots + x_n^2} \cdot \sqrt{y_1^2 + \cdots + y_n^2} 
}
```
如hello和goodbye的相似度：
```math
\begin{align}
\mathbf{v}_{\text{goodbye}} \cdot \mathbf{v}_{\text{hello}} = (0\times0) + (1\times1) + (0\times0) + (1\times0) + (0\times0) + (0\times0) = 0 + 1 + 0 + 0 + 0 + 0 = 1 \\
\|\mathbf{v}_{\text{goodbye}}\| = \sqrt{0^2 + 1^2 + 0^2 + 1^2 + 0^2 + 0^2} = \sqrt{2} \\
\|\mathbf{v}_{\text{hello}}\|   = \sqrt{0^2 + 1^2 + 0^2 + 0^2 + 0^2 + 0^2} = \sqrt{1} = 1 \\
\sqrt{2} \times 1 \approx 1.4142\\
\mathrm{similarity} = \frac{1}{\sqrt{2}} \approx 0.7071
\end{align}
```
可以看到，分子中的1主要由向量第二维得来，$`\mathbf{v}_{goodbye}`$和$`\mathbf{v}_{hello}`$的第二维都是1，而第二维表示的是和say的共现次数。也就是说，如果两个词有更多的公共的context，计算出这两个词的相似度就更高。分母由两个词总的共现次数得出，相当于做了归一化。


#### 总结
以上都是书中内容，回答了四个重要问题：  
- 如何表示一个词的含义
- 如何在计算机中表达词关系
- 如何表示词向量
- 如何计算词相似度

每一步的方案都不唯一，但这些问题给出了一个思考的框架。  

思考整个建模的过程，有新的发现：  
首先，如果两个词在对方的context中出现过，即共现矩阵中的值不为0，那可以认为这两个词有比较高的相关性。  
然而，如果两个词没有在对方的context中出现过，也就是共现矩阵中的值为0，这两个词就不相关了吗？该如何计算相似度呢？  
以上建模方法回答了这个问题，即：如果他们有共同的context，那可以认为这两个词之间是有相关性的。  
这是一个：通过已知建立矩阵、对矩阵进行分解、根据分解建立起新的联系，从而可以通过已知获取未知，的过程。  

#### 降低噪声
以上共现矩阵用计数来表示词意。但有的词，比如the，在很多词的前面都会有，却并不表示the和这些词之间有含义上的联系。为了解决这个问题，有了PMI：
```math
\mathrm{PMI}(x, y)=\log _{2}\frac{P(x, y)}{P(x)P(y)}
```
将共现矩阵表示为 C，将单词 x 和 y 的共现次数表示为 C(x, y)，将 单词 x 和 y 的出现次数分别表示为 C(x)、C(y)，将语料库的单词数量记为 N，则式可以重写为:
```math
\mathrm{PMI}(x,y)=\log_{2}\frac{P(x,y)}{P(x)P(y)}=\log_{2}\frac{\dfrac{C(x,y)}{N}}{\dfrac{C(x)}{N}\dfrac{C(y)}{N}}=\log_{2}\frac{C(x,y)\cdot N}{C(x)C(y)}
```
用词本身出现的次数做分母，降低了本身是高频词的影响。  
用PMI重新计算共现矩阵，生成PMI矩阵：
```math
\mathrm{PMI\_Matrix} = 
\begin{pmatrix}
& \texttt{you} & \texttt{say} & \texttt{goodbye} & \texttt{and} & \texttt{i} & \texttt{hello} \\
\texttt{you}     & 0 & 1.807 & 0 & 0 & 0 & 0 \\
\texttt{say}     & 1.807 & 0 & 0.322 & -0.263 & 0.322 & 1.807 \\
\texttt{goodbye} & 0 & 0.322 & 0 & 1.585 & 0 & 0 \\
\texttt{and}     & 0 & -0.263 & 1.585 & 0 & 1.585 & 0 \\
\texttt{i}       & 0 & 0.322 & 0 & 1.585 & 0 & 0 \\
\texttt{hello}   & 0 & 1.807 & 0 & 0 & 0 & 0
\end{pmatrix}
```
矩阵中有负数项，比如and和say，为什么呢，可以公式推导什么时候PMI会小于0：
```math
\begin{align}
C(x,y)*N &< C(x)*C(y)\\
C(x,y) &< \frac{C(x)*C(y)}{N}
\end{align}
```
也就是两个词共同出现的次数远小于本身出现的次数，PMI就是负的。  
特别是如果两个词从来都没有共现过，PMI将为$`-\infty`$。  
因此，定义PPMI，将PMI负值截断为0：
```math
\mathrm{PPMI}(x,y)=\mathrm{max}(0,\mathrm{PMI}(x,y))
```
PPMI矩阵：
```math
\text{PPMI} = 
\begin{pmatrix}
 & \texttt{you} & \texttt{say} & \texttt{goodbye} & \texttt{and} & \texttt{i} & \texttt{hello} \\
\texttt{you}     & 0 & 1.807 & 0 & 0 & 0 & 0 \\
\texttt{say}     & 1.807 & 0 & 0.322 & 0 & 0.322 & 1.807 \\
\texttt{goodbye} & 0 & 0.322 & 0 & 1.585 & 0 & 0 \\
\texttt{and}     & 0 & 0 & 1.585 & 0 & 1.585 & 0 \\
\texttt{i}       & 0 & 0.322 & 0 & 1.585 & 0 & 0 \\
\texttt{hello}   & 0 & 1.807 & 0 & 0 & 0 & 0
\end{pmatrix}
```
以上都是书中有的内容，不作细究。
后面重点看下书中没有细说的内容。

#### 奇异值分解
以上PPMI矩阵中有很多0，比较稀疏，浪费了内存和计算。  
为了解决这个问题，引入了奇异值分解SVD。  

鱼书中对SVD的介绍比较简单，这里稍微详细的展开说下。但只介绍流程，不介绍数学原理。  
SVD是说，一个矩阵可以分解为三个矩阵的乘积：
```math
X = USV^T
```
其中：
- $`U\in{R^{m*m}}`$:左奇异向量矩阵（正交矩阵，$`U^TU=I`$）
- $`V\in{R^{m*m}}`$:左奇异向量矩阵（正交矩阵，$`V^TV=I`$）
- $`S\in{R^{m*m}}`$:对角矩阵

假设词表长度为m，则共现矩阵就是一个$`(m, m)`$大小的矩阵$`X_{(m,m)}`$。可以分解为：
```math
X_{(m,m)} = U_{(m,m)}S_{(m,m)}V_{(m,m)}^T
```
注意，分解出的$`U_{(m,m)},S_{(m,m)},V_{(m,m)}`$维度均为$`(m,m)`$.  
降维操作就是取$`U_{(m,m)}`$矩阵的前$`k`$列$`U_{(m,k)}`$代表$`X_{(m,m)}`$矩阵。  
于是，某词one_hot编码为$`i`$，则SVD分解前的词向量为$`X_{(m,m)}`$第$`i`$
行，分解后为$`U_{(m,k)}`$第$`i`$行，维度从$`m`$降为$`k, (k<m)`$。  

奇异值分解有固定的计算过程，这里不再赘述。  
针对以上PPMI矩阵，计算奇异值分解得：
```math
S = \begin{pmatrix}
2.896 & 0     & 0     & 0     & 0     & 0 \\
0     & 1.916 & 0     & 0     & 0     & 0 \\
0     & 0     & 1.661 & 0     & 0     & 0 \\
0     & 0     & 0     & -1.661& 0     & 0 \\
0     & 0     & 0     & 0     & -1.916& 0 \\
0     & 0     & 0     & 0     & 0     & -2.896
\end{pmatrix}
```
```math
U = V = \begin{pmatrix}
0.347 & -0.139 & -0.436 & 0.436 & -0.139 & 0.347 \\
0.556 & 0.222  & 0.136  & 0.136  & 0.222  & 0.556 \\
-0.285& 0.569  & -0.236 & -0.236 & 0.569  & -0.285 \\
-0.452& -0.452 & 0.452  & 0.452  & -0.452 & -0.452 \\
-0.285& 0.569  & -0.236 & -0.236 & 0.569  & -0.285 \\
0.347 & -0.139 & -0.436 & 0.436 & -0.139 & 0.347
\end{pmatrix}
```
由于共现矩阵是一个对称矩阵，因此U和V相同。组合到一起：
```math
{
    \begin{pmatrix}
    0 & 1.807 & 0 & 0 & 0 & 0 \\
    1.807 & 0 & 0.322 & 0 & 0.322 & 1.807 \\
    0 & 0.322 & 0 & 1.585 & 0 & 0 \\
    0 & 0 & 1.585 & 0 & 1.585 & 0 \\
    0 & 0.322 & 0 & 1.585 & 0 & 0 \\
    0 & 1.807 & 0 & 0 & 0 & 0
    \end{pmatrix}
}
=
{
    \begin{pmatrix}
    0.347 & -0.139 & -0.436 & 0.436 & -0.139 & 0.347 \\
    0.556 & 0.222 & 0.136 & 0.136 & 0.222 & 0.556 \\
    -0.285 & 0.569 & -0.236 & -0.236 & 0.569 & -0.285 \\
    -0.452 & -0.452 & 0.452 & 0.452 & -0.452 & -0.452 \\
    -0.285 & 0.569 & -0.236 & -0.236 & 0.569 & -0.285 \\
    0.347 & -0.139 & -0.436 & 0.436 & -0.139 & 0.347
    \end{pmatrix}
}
{
    \begin{pmatrix}
    2.896 & 0 & 0 & 0 & 0 & 0 \\
    0 & 1.916 & 0 & 0 & 0 & 0 \\
    0 & 0 & 1.661 & 0 & 0 & 0 \\
    0 & 0 & 0 & -1.661 & 0 & 0 \\
    0 & 0 & 0 & 0 & -1.916 & 0 \\
    0 & 0 & 0 & 0 & 0 & -2.896
    \end{pmatrix}
}
{
\begin{pmatrix}
0.347 & 0.556 & -0.285 & -0.452 & -0.285 & 0.347 \\
-0.139 & 0.222 & 0.569 & -0.452 & 0.569 & -0.139 \\
-0.436 & 0.136 & -0.236 & 0.452 & -0.236 & -0.436 \\
0.436 & 0.136 & -0.236 & 0.452 & -0.236 & 0.436 \\
-0.139 & 0.222 & 0.569 & -0.452 & 0.569 & -0.139 \\
0.347 & 0.556 & -0.285 & -0.452 & -0.285 & 0.347
\end{pmatrix}
}

```
至此，PPMI矩阵分解为三个矩阵的乘积。  
其中U矩阵的维度为6，可以通过截取前k维做降维处理。  

#### 为什么用U矩阵降维当做词向量？
这里先不用数学做推理理解，毕竟奇异值分解在《线性代数及其应用》第七章，一时半会还看不到。但是为了不影响这里的继续推理，先做感性认知，后续再另作文深入理解奇异值分解。  
>这种学习法来自强化学习：动态规划法

奇异值分解的作用，是把向量$`X`$映射到另一个坐标空间$`(V^T)`$，按照另一个空间的坐标做放缩$`(S)`$，之后再映射回来$`U`$。  
奇异值表示了在那个空间坐标的重要度。降维就是把不重要的部分也就是噪声舍弃掉。  
按照以上理解的话，降维应该是取U的前k维$`U_k`$，再经过$`S,V_k^T`$变换，还原回原坐标系，生成新的k维的$`A'_k=U_kS_kV_k^T`$，这样才是在现有的坐标系下对地重要度的维度进行了去除。  
但鱼书以及其他书都直接告诉结论：用$`U_k`$做降维后的词向量。这感觉很别扭，不符合数学的对称美。有种用部分代表整体的感觉  
这里确实有省略。  
- $`U_k`$是$`X`$在新坐标系空间下的坐标，可在新坐标系空间代表$`X`$
- 直接用$`U_k`$节省复原的计算
- 两者在计算余弦相似度时等效

因此，用$`U_k`$作为降维后的词向量。

### skip-gram
矩阵分解更像是一个填字游戏，把要解决的问题转化成一个矩阵，矩阵中有已知有未知。矩阵分解试图将已知分解，通过重组分解后的已知来推测未知，也就是填那些矩阵中未知的空。  
其实严格来讲，机器学习做的就是挖掘数据中的已知，预估未知这样的事。只是矩阵分解用的是数学工具挖掘，深度学习用网络结构+反向传播挖掘。  
  
#### 概率 
同样是分布假设，skip-gram通过条件概率建模。  
skip-gram拿中心词为条件，context作为中心词条件下的条件概率。比如上文的"you say goodbye and i say hello",window是1时，中心词是say,context是i和hello的概率为：
```math
P(w_{hello},w_{i}|w_{say})
```
假设中心词生成context是独立的，则整句话出现的概率是：
```math
P(w_{you},w_{say}...w_{hello}) = P(w_{say}|w_{you})P(w_{you},w_{goobye}|w_{say})....P(w_{say}|w_{hello})
```
总结下，对于第t个词，它的m个上下文出现的概率是：
```math
\prod_{\substack{-m \leq j \leq m \\ j \neq 0}} P\left( w_{(t+j)} \mid w_{(t)} \right)
```
注意，不管是第几个context，都只跟中心词有关，且相互独立。  
对于一个长度为T的句子出现的概率为：
```math
P(w_1,w_2...w_t)=\prod_{t=1}^{T}\prod_{\substack{-m \leq j \leq m \\ j \neq 0}} P\left( w_{(t+j)} \mid w_{(t)} \right)
```
skip-gram的目标是提升真实出现的句子的概率。通过取log简化乘法计算为加法，并加负号转为最小化问题：
```math
\begin{align}
-\mathrm{log}P(w_1,w_2...w_t)
&=-\mathrm{log}\prod_{t=1}^{T}\prod_{\substack{-m \leq j \leq m \\ j \neq 0}} P\left( w_{(t+j)} \mid w_{(t)} \right)\\
&=\sum_{t=1}^{T}\sum_{\substack{-m \leq j \leq m \\ j \neq 0}} -\mathrm{log}P\left( w_{(t+j)} \mid w_{(t)} \right)
\end{align}
```

#### 建模
word2vector继承了矩阵分解的结论，直接将word编码为稠密向量。context用$`u_{context}`$表示，中心词用$`v_{center}`$表示,词表用$`\mathcal{V}`$表示。利用softmax分母和为1的性质，将模型输出通过softmax，来生成概率，因此对于某个context词生成的概率模型表示：  
```math
P\left( w_{context} \mid w_{centor} \right) = \frac{\mathrm{exp}(u_{context}^T v_{center})}{\sum_{u_i\in\mathcal{V}}\mathrm{exp}(u_i^Tv_{centor})}
```
对于整句话的生成概率模型表示：
```math
-\sum_{t=1}^{T}\sum_{\substack{-m \leq j \leq m \\ j \neq 0}} \mathrm{log}\frac{\mathrm{exp}(u_{(t+j)}^T v_{t})}{\sum_{u_i\in\mathcal{V}}\mathrm{exp}(u_i^Tv_{t})} = -\sum_{t=1}^{T}\sum_{\substack{-m \leq j \leq m \\ j \neq 0}} [u_{(t+j)}^T v_{t}-\mathrm{log}\sum_{u_i\in\mathcal{V}}\mathrm{exp}(u_i^Tv_{t})]
```
假设window设为2，展开内层累加直观感受下：
```math
-\sum_{t=1}^{T} [(u_{(t-2)}^T v_{t} + u_{(t-1)}^T v_{t} + u_{(t+1)}^T v_{t} + u_{(t+2)}^T v_{t}) - 4\mathrm{log}\sum_{u_i\in\mathcal{V}}\mathrm{exp}(u_i^Tv_{t})]
```
>《动手学深度学习》讨厌的一点：先讲了skip-gram和cbow的公式，但并没有立即开始基于公式建模，而是开始继续讲优化。我没有基于最基本的公式建模，没有对基本公式有深入的把握，怎么能深刻理解到哪里需要优化、为什么优化？这时候继续看优化，懵逼。转去看后面的代码实现，代码是优化后的，我还是懵逼。直接卡这了。不得不先看CBOW的公式，结合鱼书中的源码理解基本公式，再转去看skip-gram的公式，尝试建立起基本的模型。鱼书好的一点就在这，每讲一点，立即尝试编码，然后再引出一点，这样每一步走的都瓷实。


### CBOW
>留个问题，为什么CBOW向量乘完要取$`\frac{1}{2m}`$，而skip-gram不用乘？

#### 概率
CBOW是已知context的条件下，中间词出现的概率为：
```math
    P(w_{center}|w_{context})
```
一句话出现的概率为：
```math
P(w_1,w_2...w_t)=\prod_{t=1}^{T} P\left( w_{(t)} \mid w_{(t-j)}...w_{(t-1)},w_{(t+1)}...w_{(t+j)} \right)
```
取负对数，以降低计算量、转化为最小化问题：
```math
-\mathrm{log}P(w_1,w_2...w_t)=-\sum_{t=1}^{T} \mathrm{log}P\left( w_{(t)} \mid w_{(t-j)}...w_{(t-1)},w_{(t+1)}...w_{(t+j)} \right)
```
对$`P\left( w_{(t)} \mid w_{(t-j)}...w_{(t-1)},w_{(t+1)}...w_{(t+j)} \right)`$建模：
```math
P\left( w_{(t)} \mid w_{(t-j)}...w_{(t-1)},w_{(t+1)}...w_{(t+j)} \right) = \frac{\mathrm{exp}(u_{(centor)})}{}
```