#!/usr/bin/env python3
"""
用纯 numpy 实现高斯过程 (GP) 回归 — 对应文章里贝叶斯建模那部分:
  k(θi, θj) = RBF
  先验: f(θ) ~ N(0, K)
  观测: y = f(θ) + ε, ε ~ N(0, σ_n²)
  后验: f(θ*) | y ~ N(μ*, Σ*)

输入 5 个样本点 → 输出后验分布(均值 + 不确定度)。
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False


# ============ RBF kernel (与文章公式一致) ============
def rbf_kernel(X1, X2, length_scale=1.0, sigma_f=1.0):
    """
    k(x, x') = σ_f² · exp(-||x - x'||² / (2 l²))
    X1: (n, d), X2: (m, d)  →  K: (n, m)
    """
    # 展平成 2D, 算 pairwise 距离平方
    X1 = np.atleast_2d(X1)
    X2 = np.atleast_2d(X2)
    sq = np.sum(X1**2, axis=1)[:, None] + np.sum(X2**2, axis=1)[None, :] - 2 * X1 @ X2.T
    return sigma_f**2 * np.exp(-sq / (2 * length_scale**2))


# ============ GP 后验(标准公式) ============
def gp_posterior(X_train, y_train, X_test, length_scale=1.0, sigma_f=1.0, sigma_n=0.1):
    """
    给定训练样本 (X_train, y_train), 计算测试点 X_test 上的后验均值和方差。
    后验:  f* | y ~ N(μ*, Σ*)
    """
    K = rbf_kernel(X_train, X_train, length_scale, sigma_f)            # (n, n)
    K_s = rbf_kernel(X_train, X_test, length_scale, sigma_f)            # (n, m)
    K_ss = rbf_kernel(X_test, X_test, length_scale, sigma_f)             # (m, m)

    # 加观测噪声
    K_noise = K + sigma_n**2 * np.eye(len(X_train))

    # 后验均值和方差(标准公式)
    K_inv_y = np.linalg.solve(K_noise, y_train)
    mu = K_s.T @ K_inv_y                                          # (m,)
    cov = K_ss - K_s.T @ np.linalg.solve(K_noise, K_s)              # (m, m)
    return mu, np.sqrt(np.diag(cov))


# ============ 数据: 真实函数 + 5 个样本 ============
def true_f(theta):
    """真实函数: 一个钟形(类似文章里的 J(θ))。"""
    return 0.8 * np.exp(-((theta - 2.0) ** 2) / 2.0)


np.random.seed(42)
X_train = np.array([-2.5, -1.0, 0.5, 1.5, 3.5]).reshape(-1, 1)
y_train = true_f(X_train.ravel()) + np.random.normal(0, 0.08, size=5)

# 测试网格
X_test = np.linspace(-5, 5, 200).reshape(-1, 1)
y_true = true_f(X_test.ravel())

# 计算 GP 后验(用样本自身的 y 估计超参, 简化版)
length_scale = 1.0
sigma_f = 1.0
sigma_n = 0.15
mu_post, std_post = gp_posterior(X_train, y_train, X_test, length_scale, sigma_f, sigma_n)


# ============ 绘图 ============
fig, ax = plt.subplots(figsize=(12, 6))

# 真实函数(浅灰虚线)
ax.plot(X_test, y_true, "k--", alpha=0.5, linewidth=1.5, label=r"真实 $f(\theta)$")

# 后验均值(蓝色实线)
ax.plot(X_test, mu_post, color="#3a7bd9", linewidth=2.5, label=r"GP 后验均值 $\mu(\theta)$")

# 不确定度(浅蓝填充, ±2σ)
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

# 标题
fig.suptitle(
    r"高斯过程 (GP) 回归 — 5 个样本 → 后验 $p(f \mid D) = \mathcal{N}(\mu, \sigma^2)$",
    fontsize=14, fontweight="bold",
)

# 注释: 样本密集处不确定度低, 远离样本处不确定度高
ax.annotate(
    "样本稀疏区\n不确定度大",
    xy=(4.5, mu_post[np.argmin(np.abs(X_test.ravel() - 4.5))]),
    xytext=(3.8, 0.95),
    fontsize=10, color="#888",
    arrowprops=dict(arrowstyle="->", color="#888", alpha=0.6),
)
ax.annotate(
    "样本密集区\n拟合准",
    xy=(0.5, mu_post[np.argmin(np.abs(X_test.ravel() - 0.5))]),
    xytext=(-3.0, 0.95),
    fontsize=10, color="#3a7bd9", fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="#3a7bd9", alpha=0.6),
)

plt.tight_layout()
out = "/home/youngsure/Code/TechArt/RL/image/gp_regression.png"
plt.savefig(out, dpi=140, bbox_inches="tight", facecolor="white")
print(f"[OK] 保存: {out}")
print(f"[INFO] σ_n (观测噪声)   = {sigma_n}")
print(f"[INFO] l   (长度尺度)   = {length_scale}")
print(f"[INFO] σ_f (信号标准差) = {sigma_f}")
print(f"[INFO] 后验均值范围: [{mu_post.min():.3f}, {mu_post.max():.3f}]")
print(f"[INFO] 后验 σ 范围:    [{std_post.min():.3f}, {std_post.max():.3f}]")