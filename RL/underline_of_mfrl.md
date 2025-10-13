> 二次读mfrl，有的语句让我产生新的灵感，但不是笔记，只是有感而发。想到可以把语句记下来，加上评注。也许有一天我能开发一个app出来，把这个下划线的评注和文档联系起来，就能一体呈现了。  

The task becomes nontrivial if the agent does not know any information
about the environment in advance. Then, the agent must interact with the environment to find a good policy by trial and error.   
有点意思，从人的视角看这个问题，看到的是全局视角，只要一眼就获取了迷宫的所有信息，是在全局视角下找一条最好路径。如果把人的解决步骤转化为算法，会开始思考，怎么把这整个迷宫输入到计算机里？怎么从这么多信息里找路呢？但是实际上算法必须转化为从agent的视角一步一步看该往哪走。在agent的视角上，你不知道前后左右是否有障碍，也不知道目标在哪。此时就需要data或model来驱动寻找最优路径了。  


