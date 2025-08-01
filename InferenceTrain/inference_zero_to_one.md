# 推理021

大模型之前，信息是以点状分布的。当你对一个问题好奇时，你必须从海量的互联网文章、浩瀚的技术书片段中，去寻找只言片语，凑成答案。现在有了大模型，自动帮你从海量的文本中找到相关的片段，加以融合，反馈。  
这是一个对好奇心友好的时代，允许你用好奇心驱动，不断扩大已知，到达未知的彼岸。

## 如果让我设计一个推理服务，我该考虑哪些问题？

预估就是用训练好的参数，再执行一遍前向传播的过程。训练和预估往往是两个服务，训练产出参数和计算图后，需要把参数和计算图同步到预估服务，加载后，在接收到新的样本时，按照计算图重算一遍前向传播，返回结果。  
因此，分成两方面考虑实现一个预估服务：  
- 参数
- 计算图

### 参数

又分为两部分，一个是参数本身（也就是tensor）如何保存；一个是包含所有参数的模型如何保存（涉及网络的结构）。

#### 参数本身如何保存
参数在pytorch中通过tensor抽象。保存参数也就是保存一个Tensor。  
大胆猜测tensor应该是类似这样的类：  
```
class Tensor {
  public:
    std::tuple shape();

  private:
    shape_;
    dtype_;
    device_;
  private:
    bytes storage;
};
```
包含：  
- 底层数据的存储。
- tensor属性，包括形状、类型、设备等。相同的底层存储，搭配不同的属性，可以表示不同的tensor。
- 公共方法。

都需要保存哪些信息？以上的底层数据和tensor属性都是需要保存的。

怎么实现序列化？  
如果是我，我会在这个类里加个serilize的方法，把需要存储的数据通过这个方法序列化，返回一个字节流。外层逐个调用tensor的serilize方法获取字节流并保存。  
序列化的库有很多，列举几个可行的：  
- protobuf。训练、预估都用相同的proto定义即可，有很好的压缩、序列化/反序列化、兼容性 等性能。
- boost.serilize。支持C++原生数据结构的序列化。兼容性稍差。  

以上的可读性都比较差，如果要保证可读性，可以用json。不过，对于参数来说，应该不需要保证可读性吧，应该没人会直接拉个tensor出来看内容
  
  
实际上，tensorflow确实是用的proto来序列化tensor的：  
https://github.com/tngan/tensornode/blob/master/tensorflow/core/framework/tensor.proto  
而pytorch用的是pickle。pickle是调用了pytorch提供的接口，将底层的内存序列化。  

#### 模型如何保存
nn.Module通过state_dict()方法打包参数。
state_dict是一个字典，可以将参数命名保存。  

#### 参数如何传输加载
在2020年之前见过最原始的传输加载方式。  
模型dump成文件之后，通过rsync将文件拉取到线上服务器中（如精排服务），起一个进程解析文件，load进共享内存。精排读取共享内存，通过特征查找参数，进行运算。  
那时候只是个刚毕业的菜鸡，看不到系统全貌，实际并不清楚这块在做什么，为什么这么做。  
后来就有了中台团队负责的预估服务，用来加载模型、预估。精排只需要发送抽取好的特征过去，就可以返回分数。自那以后，就没再接触过预估服务了。  

