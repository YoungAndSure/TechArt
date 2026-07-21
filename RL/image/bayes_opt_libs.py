#!/usr/bin/env python3
"""
贝叶斯优化 / GP 回归库 API 对比 — 展示 sklearn / skopt / GPy / BoTorch / PyMC
各自要设的关键参数,以及最小可用代码。
"""
import numpy as np


# ============ 0. 准备数据 (5 个样本点) ============
np.random.seed(42)


def true_f(theta):
    return 0.8 * np.exp(-((theta - 2.0) ** 2) / 2.0)


X_train = np.array([-2.5, -1.0, 0.5, 1.5, 3.5]).reshape(-1, 1)
y_train = true_fun_safe(X_train.ravel()) if False else true_f(X_train.ravel()) + np.random.normal(0, 0.08, 5)
X_test = np.linspace(-5, 5, 200).reshape(-1, 1)
y_test = true_f(X_test.ravel())


# ============ 1. sklearn: GaussianProcessRegressor ============
print("=" * 60)
print("1. sklearn.gaussian_process.GaussianProcessRegressor")
print("=" * 60)
print("""
最常用的 GP 库,sklearn 自带。

最小调用:
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel

    kernel = ConstantKernel(1.0) * RBF(length_scale=1.0) + WhiteKernel(noise_level=0.1)
    gp = GaussianProcessRegressor(kernel=kernel, alpha=1e-6, normalize_y=True)
    gp.fit(X_train, y_train)
    mu, std = gp.predict(X_test, return_std=True)

要设的关键参数:
  kernel        — 核函数组合
                 RBF(length_scale=l)               平方指数核
                 ConstantKernel(c)                  信号方差 σ_f²
                 WhiteKernel(noise_level=σ_n)       观测噪声
                 Matern(length_scale=l, nu=2.5)     更平滑的替代
                 *  +  组合
                 ExpSineSquared                    周期核

  alpha         — 岭正则项,防止 K 接近奇异,默认 1e-10
  normalize_y   — 是否归一化 y(均值0方差1),小样本时推荐 True
  n_restarts_optimizer — 超参优化重启次数,默认 0(不优化)
                                  建议 ≥ 10,避免局部最优
  random_state  — 随机种子

返回: gp.predict(X, return_std=True)
       → mu (均值), std (标准差, 即 √后验方差)
""")

# ============ 2. skopt (scikit-optimize) ============
print("=" * 60)
print("2. skopt (scikit-optimize): gp_minimize")
print("=" * 60)
print("""
高层 Bayesian 优化库,内部用 sklearn GP。要给目标函数,自动选点。

最小调用:
    from skopt import gp_minimize
    from skopt.space import Real

    def objective(theta):
        # theta 是 Real 空间里的标量(或数组)
        return -true_f(theta[0])   # 最小化,所以加负号

    result = gp_minimize(
        objective,
        dimensions=[Real(-5, 5, name='theta')],
        n_calls=20,                # 总共评估几次
        n_initial_points=5,        # 随机初始化次数,剩余用 GP
        acq_func='gp_hedge',       # 采集函数
        random_state=42,
    )
    print(result.x, -result.fun)

要设的关键参数:
  func            — 目标函数,接收参数数组,返回标量(最小化)
  dimensions      — 搜索空间,Real(low, high) 或 Integer
  n_calls         — 总评估次数(包括 n_initial_points)
  n_initial_points— 初始随机评估次数(后续用 GP)
  acq_func        — 采集函数:
                   'gp_hedge'  — 混合策略(推荐默认)
                   'EI'        — Expected Improvement
                   'PI'        — Probability of Improvement
                   'LCB'       — Lower Confidence Bound
  noise           — 观测噪声水平,>0 时会混合 GP+likelihood
  random_state    — 随机种子

返回: result.x (最优 θ), result.fun (最优值)
""")

# ============ 3. GPy ============
print("=" * 60)
print("3. GPy (Sheffield ML)")
print("=" * 60)
print("""
专门的 GP 库,学术派。比 sklearn 更灵活,支持多输出/分层/复杂核。

最小调用:
    import GPy
    kernel = GPy.kern.RBF(input_dim=1, variance=1.0, lengthscale=1.0)
    gp = GPy.models.GPRegression(X_train, y_train.reshape(-1, 1), kernel)
    gp.optimize(messages=False)      # 超参优化,关键!

    mu, var = gp.predict(X_test)
    std = np.sqrt(var)

要设的关键参数:
  kernel           — 核
                    GPy.kern.RBF(input_dim, variance, lengthscale)
                    GPy.kern.Matern32 / Matern52
                    GPy.kern.PeriodicExponential
                    +  / *  组合
  noise_var        — 噪声方差,默认会被优化
  GPRegression(    — 拟合 GP
    X, Y,
    kernel,
    noise_var=0.01,
    normalizer=True           # 是否归一化 y
  )
  gp.optimize(      — 优化超参(重要!)
    optimizer='bfgs',         # 'bfgs', 'scg', 'lbfgsb'
    max_iters=100,
    messages=False            # 不打印
  )

返回: gp.predict(X) → (mu, var)
""")

# ============ 4. BoTorch (PyTorch-based) ============
print("=" * 60)
print("4. BoTorch (PyTorch-based, Meta/学术派)")
print("=" * 60)
print("""
PyTorch 实现的 GP + BO,灵活度最高,适合深度学习集成。

最小调用:
    import torch
    from botorch.models import SingleTaskGP
    from botorch.fit import fit_gpytorch_mll
    from botorch.optim import optimize_acqf
    from botorch.acquisition import ExpectedImprovement
    from gpytorch.mlls import ExactMarginalLogLikelihood

    # GP 拟合
    gp = SingleTaskGP(train_X, train_Y)
    mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
    fit_gpytorch_mll(mll)        # 超参优化

    # 采集函数 + 选下一个点
    EI = ExpectedImprovement(model=gp, best_f=train_Y.max())
    candidate, acq_value = optimize_acqf(
        acq_function=EI,
        bounds=torch.tensor([[-5.0], [5.0]]),
        q=1, num_restarts=5, raw_samples=20,
    )

要设的关键参数:
  SingleTaskGP(        — 标准 GP 回归
    train_X, train_Y,
    covar_module=ScaleKernel(MaternKernel(...))  # 核
  )
  fit_gpytorch_mll(     — 优化超参(必须调用)
    mll,
  )
  ExpectedImprovement(  — EI 采集函数
    model, best_f=...,       # 当前最优观测值
  )
  optimize_acqf(        — 优化采集函数找下一个点
    acq_function,
    bounds,                  # Tensor, (2, d)
    q=1,                     # 每次选几个点(并行)
    num_restarts=5,          # 多次重启避免局部最优
    raw_samples=512,         # 初始采样数
  )

返回: candidate (下一个评估点)
""")

# ============ 5. PyMC (贝叶斯建模框架) ============
print("=" * 60)
print("5. PyMC (贝叶斯推断框架)")
print("=" * 60)
print("""
通用贝叶斯建模,不只是 BO。可做完整的贝叶斯推断(后验采样)。

最小调用:
    import pymc as pm

    with pm.Model() as model:
        # 先验
        length_scale = pm.Gamma("l", alpha=2, beta=1)
        sigma_f = pm.HalfNormal("sigma_f", sigma=1)
        sigma_n = pm.HalfNormal("sigma_n", sigma=0.5)

        # GP
        cov = sigma_f**2 * pm.math.exp(-0.5 * (X_train[:, None] - X_train[None, :])**2 / length_scale**2)
        f = pm.MvNormal("f", mu=np.zeros(5), cov=cov + sigma_n**2 * np.eye(5))
        y_obs = pm.Normal("y_obs", mu=f, sigma=sigma_n, observed=y_train)

        # MCMC 采样后验
        trace = pm.sample(2000, tune=1000, return_inferencedata=True)

    # 后验预测
    posterior_f = trace.posterior["f"]
    # ...

要设的关键参数:
  pm.Gamma / pm.HalfNormal    — 超参先验
  pm.MvNormal                 — 多元高斯(对 f 的先验)
  pm.Normal                   — 观测 likelihood
  pm.sample(                  — MCMC/NUTS 采样
    draws=2000,                # 后验采样数
    tune=1000,                 # 预烧(tuning)数
    target_accept=0.9,         # 接受率
    chains=4,                  # 链数
  )
""")

# ============ 汇总对比 ============
print("=" * 60)
print("选用建议")
print("=" * 60)
print("""
入门 / 经典场景 → sklearn (简单,文档好)
想直接做 Bayesian Optimization → skopt (高层 API)
学术 GP 研究 / 复杂核结构 → GPy
深度学习集成 / 自定义采集函数 → BoTorch
完整贝叶斯推断 / 非高斯似然 → PyMC
""")