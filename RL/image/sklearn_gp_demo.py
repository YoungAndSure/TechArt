#!/usr/bin/env python3
"""
sklearn GaussianProcessRegressor 最小可用示例
==============================================

对应文章里的贝叶斯建模部分:
  k(θi, θj) = RBF
  先验: f(θ) ~ N(0, K)
  观测: y = f(θ) + ε
  后验: f(θ*) | y ~ N(μ*, σ*²)

输入 5 个样本点 → 输出后验分布(均值 + 不确定度)。

依赖: pip install scikit-learn matplotlib numpy
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (
    RBF,                  # 平方指数核 k(x, x') = exp(-||x-x'||²/2l²)
    ConstantKernel,       # 信号方差 σ_f² (Kernel 整体缩放)
    WhiteKernel,          # 观测噪声 σ_n²
)


# ============================================================
# 1. 数据准备
# ============================================================
def true_f(theta):
    """真实函数(待拟合的目标): 一个钟形。"""
    return 0.8 * np.exp(-((theta - 2.0) ** 2) / 2.0)


np.random.seed(42)
X_train = np.array([-2.5, -1.0, 0.5, 1.5, 3.5]).reshape(-1, 1)
y_train = true_f(X_train.ravel()) + np.random.normal(0, 0.08, size=5)

# 测试网格(用于画后验曲线)
X_test = np.linspace(-5, 5, 200).reshape(-1, 1)
y_true = true_f(X_test.ravel())


# ============================================================
# 2. 定义核 + 模型
# ============================================================
# 核组合:  σ_f² · RBF(length_scale=l)  +  白噪声 σ_n²
# 这是文章 line 109-115 那个高斯过程先验的标准形式
kernel = ConstantKernel(1.0, constant_value_bounds=(0.1, 10.0)) * \
         RBF(length_scale=1.0, length_scale_bounds=(0.1, 10.0)) + \
         WhiteKernel(noise_level=0.1, noise_level_bounds=(1e-5, 1.0))

gp = GaussianProcessRegressor(
    kernel=kernel,
    alpha=1e-6,            # 岭正则项(防止 K 接近奇异),默认 1e-10
    normalize_y=True,      # 归一化 y(均值0方差1),小样本时推荐 True
    n_restarts_optimizer=10,  # 超参优化重启次数(0 = 不优化)
    random_state=42,
)


# ============================================================
# 3. 拟合 + 预测后验
# ============================================================
gp.fit(X_train, y_train)
mu_post, std_post = gp.predict(X_test, return_std=True)

# 拟合后学到的超参
print("=" * 50)
print("拟合后的超参(被 sklearn 自动优化过):")
print(f"  σ_f (信号方差)  = {gp.kernel_.k1.k1.constant_value:.4f}")
print(f"  l  (长度尺度)    = {gp.kernel_.k1.k2.length_scale:.4f}")
print(f"  σ_n (观测噪声)   = {gp.kernel_.k2.noise_level:.4f}")
print(f"  log marginal likelihood = {gp.log_marginal_likelihood_value_:.3f}")


# ============================================================
# 4. 绘图
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))

# 真实函数(灰虚线)
ax.plot(X_test, y_true, "k--", alpha=0.5, linewidth=1.5, label=r"真实 $f(\theta)$")

# 后验均值(蓝实线)
ax.plot(X_test, mu_post, color="#3a7bd9", linewidth=2.5, label=r"GP 后验均值 $\mu(\theta)$")

# 不确定度 ±2σ(浅蓝填充)
ax.fill_between(
    X_test.ravel(),
    mu_post - 2 * std_post,
    mu_post + 2 * std_post,
    color="#3a7bd9", alpha=0.2,
    label=r"$\pm 2\sigma$ 后验不确定度",
)

# 观测样本(红点)
ax.scatter(X_train, y_train, s=120, color="#d9534f", zorder=5,
           edgecolors="white", linewidths=1.5, label="观测样本 (5 个)")

# 轴
ax.set_xlabel(r"$\theta$", fontsize=13)
ax.set_ylabel(r"$f(\theta)$", fontsize=13)
ax.set_xlim(-5, 5)
ax.set_ylim(-0.3, 1.1)
ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=11)

fig.suptitle(
    r"sklearn GaussianProcessRegressor — 5 个样本 → 后验 $p(f \mid D) = \mathcal{N}(\mu, \sigma^2)$",
    fontsize=13, fontweight="bold",
)

# 注释
ax.annotate("样本稀疏区\n不确定度大", xy=(4.5, mu_post[-5]), xytext=(3.7, 0.95),
            fontsize=10, color="#888",
            arrowprops=dict(arrowstyle="->", color="#888", alpha=0.6))
ax.annotate("样本密集区\n拟合准", xy=(0, mu_post[100]), xytext=(-3.5, 0.95),
            fontsize=10, color="#3a7bd9", fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="#3a7bd9", alpha=0.6))

plt.tight_layout()
out = "/home/youngsure/Code/TechArt/RL/image/sklearn_gp_demo.png"
plt.savefig(out, dpi=90, bbox_inches="tight", facecolor="white")
print(f"\n[OK] 保存: {out}")