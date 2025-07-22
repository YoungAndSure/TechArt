一、萌芽期：协同过滤奠基（1992-2005）​​  
​​《Using collaborative filtering to weave an information tapestry》​​ (Goldberg et al., 1992)  
​贡献​：提出首个协同过滤系统Tapestry，引入“人群智慧”概念。  
​​《Item-Based Collaborative Filtering Recommendation Algorithms》​​ (Sarwar et al., 2001)  
​贡献​：奠定ItemCF基础，通过物品相似度矩阵解决用户行为稀疏性问题，引用超9000次。  
​​《Amazon.com Recommendations: Item-to-Item Collaborative Filtering》​​ (Linden et al., 2003)  
​贡献​：亚马逊工业级ItemCF实现，推动电商推荐系统落地。  
  
  
🧩 ​二、发展期：矩阵分解时代（2006-2009）​​
​​《Netflix Update: Try This at Home》​​ (Simon Funk, 2006)  
​贡献​：开源SVD矩阵分解实现，推动Netflix Prize竞赛热潮。  
​​《Matrix Factorization Techniques for Recommender Systems》​​ (Koren et al., 2009)  
​贡献​：系统总结MF在推荐中的应用，成为领域最常引用论文之一。  
​​《Restricted Boltzmann Machines for Collaborative Filtering》​​ (Salakhutdinov et al., 2007)  
​贡献​：首次将RBM用于评分预测，Netflix核心算法之一。  
  
  
⚙️ ​三、融合期：特征工程与FM（2010-2015）​​  
​​《Factorization Machines》​​ (Rendle, 2010)  
​贡献​：统一SVM与矩阵分解，支持高维稀疏特征交互，成为CTR预测基准模型。  
​​《Practical Lessons from Predicting Clicks on Ads at Facebook》​​ (He et al., 2014)  
​贡献​：提出GBDT+LR特征组合方案，工业界特征工程范本。  
​​《Ad Click Prediction: a View from the Trenches》​​ (McMahan et al., 2013)  
​贡献​：FTRL在线学习算法实现，解决大规模稀疏数据实时更新问题。  
  
  
🧠 ​四、深度化：神经网络革命（2016-2019）​​  
​​《Wide & Deep Learning for Recommender Systems》​​ (Cheng et al., 2016)  
​贡献​：Google Play提出宽度（记忆）与深度（泛化）联合训练框架，影响工业界架构设计。  
​​《Deep Neural Networks for YouTube Recommendations》​​ (Covington et al., 2016)  
​贡献​：YouTube两阶段（召回+排序）深度学习架构范本，引入用户观看序列建模。  
​​《Deep Interest Network for Click-Through Rate Prediction》​​ (Zhou et al., 2018)  
​贡献​：阿里提出动态兴趣激活单元（DIN），解决用户行为多样性问题。  
​​《Multi-Interest Network with Dynamic Routing for Recommendation》​​ (Li et al., 2019)  
​贡献​：天猫胶囊网络动态路由多兴趣向量，解决用户兴趣分散问题。  
  
  
🔮 ​五、前沿拓展：多目标、因果与可解释性（2018-2020）​​  
​​《The Use of MMR, Diversity-Based Reranking》​​ (Carbonell & Goldstein, 1998)  
​贡献​：最大边界相关（MMR）解决结果多样性，被工业界广泛用于重排阶段。  
​​《Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches》​​ (Dacrema et al., 2019)  
​贡献​：质疑深度学习在推荐中的实际增益，引发可复现性与评估标准反思。  
​​《RippleNet: Propagating User Preferences on the Knowledge Graph》​​ (Wang et al., 2018)  
​贡献​：知识图谱与推荐结合，提升可解释性与冷启动效果。  