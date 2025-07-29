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
\\
% "say" 的词向量
\mathbf{v}_{\text{say}} = 
\begin{pmatrix}
1 & 0 & 1 & 1 & 1 & 1 
\end{pmatrix}
\\
% "goodbye" 的词向量
\mathbf{v}_{\text{goodbye}} = 
\begin{pmatrix}
0 & 1 & 0 & 1 & 0 & 0 
\end{pmatrix}
\\
% "and" 的词向量
\mathbf{v}_{\text{and}} = 
\begin{pmatrix}
0 & 1 & 1 & 0 & 1 & 0 
\end{pmatrix}
\\
% "i" 的词向量
\mathbf{v}_{\text{i}} = 
\begin{pmatrix}
0 & 1 & 0 & 1 & 0 & 0 
\end{pmatrix}
\\
% "hello" 的词向量
\mathbf{v}_{\text{hello}} = 
\begin{pmatrix}
0 & 1 & 0 & 0 & 0 & 0 
\end{pmatrix}
```

#### 如何计算词相似度
可以用余弦相似度：
```math
similarityß(\boldsymbol{x},\boldsymbol{y}) = 
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
\operatorname{similarity} = \frac{1}{\sqrt{2}} \approx 0.7071
\end{align}
```


>SVD可以用来降维，但不是用来降维的，鱼书在这一点上有误导


鱼书中对SVD的介绍比较简单，这里稍微详细的展开说下。但只介绍流程，不介绍数学原理。  
SVD是说，一个矩阵可以分解为三个矩阵的乘积：
```math
X = USV^T
```
假设词表长度为m，则共现矩阵就是一个$`(m, m)`$大小的矩阵$`X_{(m,m)}`$。可以分解为：
```math
X_{(m,m)} = U_{(m,m)}S_{(m,m)}V_{(m,m)}^T
```
注意，分解出的$`U_{(m,m)},S_{(m,m)},V_{(m,m)}`$维度均为$`(m,m)`$，其中$`S_{(m,m)}`$是一个只有对角有值的矩阵，称之为奇异值矩阵。  
降维操作就是取$`U_{(m,m)}`$矩阵的前$`k`$列$`U_{(m,k)}`$代表$`X_{(m,m)}`$矩阵。  
于是，某词one_hot编码为$`i`$，则SVD分解前的词向量为$`X_{(m,m)}`$第$`i`$
行，分解后为$`U_{(m,k)}`$第$`i`$行，维度从$`m`$降为$`k, (k<m)`$。

 