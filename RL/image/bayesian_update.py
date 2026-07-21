#!/usr/bin/env python3
"""
贝叶斯更新 — 概念修正版:
  先验是函数空间上的分布 p(f), 不是 θ 上的分布 p(θ)。
  样本 (θᵢ, aᵢ) 进来后, 得到后验 p(f | D), 也是函数空间上的分布。

可视化: 从先验 GP 里 sample 出几条"可能的函数曲线",
       看到观测后, 后验里的所有曲线都被拉向观测点(附近方差小)。
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False


# ============ 核函数 RBF ============
def rbf_kernel(theta1, theta2, l=1.0, sigma_f=1.0):
    """k(x, x') = σ_f² · exp(-||x-x'||²/2l²)  支持任意形状输入,广播成矩阵"""
    theta1 = np.atleast_1d(theta1)
    theta2 = np.atleast_1d(theta2)
    diff = theta1[:, None] - theta2[None, :]
    return sigma_f**2 * np.exp(-(diff ** 2) / (2 * l**2))


# ============ GP 后验(标准公式) ============
def gp_posterior(theta_train, y_train, theta_test, l=1.0, sigma_f=1.0, sigma_n=0.05):
    K    = rbf_kernel(theta_train, theta_train, l, sigma_f)
    K_s  = rbf_kernel(theta_train, theta_test, l, sigma_f)
    K_ss = rbf_kernel(theta_test, theta_test, l, sigma_f)

    K_noise = K + sigma_n**2 * np.eye(len(theta_train))
    K_inv   = np.linalg.inv(K_noise)
    mu  = K_s.T @ K_inv @ y_train
    cov = K_ss - K_s.T @ K_inv @ K_s
    return mu, cov


# ============ 数据 ============
THETA = np.linspace(-4, 4, 100)               # 函数网格
N_FUNCS = 10                                  # 每个面板画 10 条曲线
np.random.seed(42)

# 真实函数(只用于概念说明, 不参与拟合)
def true_f(t):
    return 0.8 * np.exp(-((t - 1.5) ** 2) / 1.5) + 0.3 * np.exp(-((t + 1.5) ** 2) / 2.0)

# 观测样本
sample_thetas = np.array([-2.5, -1.0, 0.5, 1.5, 3.5])
sample_values = true_f(sample_thetas) + np.random.normal(0, 0.03, 5)

# ============ 从先验 sample 函数: f ~ N(0, K) ============
K_prior = rbf_kernel(THETA, THETA, l=1.0, sigma_f=1.0)
L_prior = np.linalg.cholesky(K_prior + 1e-6 * np.eye(len(THETA)))
prior_funcs = L_prior @ np.random.randn(len(THETA), N_FUNCS)
# 先验均值(理论上 0)
prior_mean = np.zeros(len(THETA))
# 先验不确定度(沿对角线开方)
prior_std = np.sqrt(np.diag(K_prior))

# ============ 后验: f | D ~ N(μ, Σ) ============
mu_post, cov_post = gp_posterior(
    sample_thetas, sample_values, THETA, l=1.0, sigma_f=1.0, sigma_n=0.05,
)
L_post = np.linalg.cholesky(cov_post + 1e-6 * np.eye(len(THETA)))
post_funcs = mu_post[:, None] + L_post @ np.random.randn(len(THETA), N_FUNCS)
post_std = np.sqrt(np.diag(cov_post))


# ============ 绘图 (三联竖排) ============
fig, axes = plt.subplots(3, 1, figsize=(11, 11), sharex=True)

# ---------- Panel 1: 先验 (函数空间) ----------
axes[0].plot(THETA, prior_funcs, color="#3a7bd9", alpha=0.35, linewidth=1)
axes[0].plot(THETA, prior_mean, "k--", linewidth=1.5, alpha=0.7, label="先验均值 (= 0)")
axes[0].fill_between(
    THETA,
    prior_mean - 2 * prior_std,
    prior_mean + 2 * prior_std,
    color="#3a7bd9", alpha=0.15, label=r"$\pm 2\sigma$ 先验不确定度",
)
axes[0].set_title(
    r"先验  $p(f)$  —  函数空间上的分布"
    + "\n(还没看到数据,函数可以千变万化,均值=0,所有平滑曲线都合理)",
    fontsize=12, color="#3a7bd9", loc="left", fontweight="bold",
)
axes[0].set_ylabel("f(θ)", fontsize=12)
axes[0].set_ylim(-2.5, 2.5)
axes[0].grid(alpha=0.3)
axes[0].legend(loc="upper right", fontsize=10)

# ---------- Panel 2: 观测样本 ----------
np.random.seed(99)
y_jitter = np.random.uniform(-0.15, 0.15, size=len(sample_thetas))
axes[1].scatter(sample_thetas, y_jitter, s=120, color="#222",
                edgecolors="white", linewidths=1.5, zorder=3)
axes[1].axhline(y=0, color="#999", linewidth=0.8, zorder=1)
axes[1].set_title(
    f"观测样本  D  —  {len(sample_thetas)} 个 ($\\theta_i$, $a_i$) 对",
    fontsize=12, color="#222", loc="left", fontweight="bold",
)
axes[1].set_ylabel(r"$a_i$", fontsize=12)
axes[1].set_ylim(-0.5, 1.5)
axes[1].set_yticks([])
axes[1].grid(alpha=0.3, axis="x")
axes[1].text(0.02, 0.85, "看到这 5 个点之后 ...",
             transform=axes[1].transAxes, fontsize=10, color="#666", style="italic")

# ---------- Panel 3: 后验 (函数空间) ----------
axes[2].plot(THETA, post_funcs, color="#d9534f", alpha=0.45, linewidth=1.2)
axes[2].plot(THETA, mu_post, "k--", linewidth=1.8, label="后验均值 μ(θ)")
axes[2].fill_between(
    THETA,
    mu_post - 2 * post_std,
    mu_post + 2 * post_std,
    color="#d9534f", alpha=0.18, label=r"$\pm 2\sigma$ 后验不确定度",
)
# 把观测点叠在均值上(给读者锚定)
axes[2].scatter(sample_thetas, sample_values, s=80, color="#222",
                edgecolors="white", linewidths=1.2, zorder=5,
                label="观测样本")
axes[2].set_title(
    r"后验  $p(f \mid D)$  —  看到数据后的函数分布"
    + "\n(所有候选函数都被拉向观测点附近,远处仍可能有较大不确定度)",
    fontsize=12, color="#d9534f", loc="left", fontweight="bold",
)
axes[2].set_xlabel(r"$\theta$", fontsize=13)
axes[2].set_ylabel("f(θ)", fontsize=12)
axes[2].set_ylim(-2.5, 2.5)
axes[2].grid(alpha=0.3)
axes[2].legend(loc="upper right", fontsize=10)

# 总标题
fig.suptitle(
    r"贝叶斯优化: 先验 $p(f)$  →  观测  →  后验 $p(f \mid D)$  (在函数空间上)",
    fontsize=15, fontweight="bold", y=0.995,
)

# 面板间箭头 + 公式
arrow1 = mpatches.FancyArrowPatch(
    (0.5, 0.665), (0.5, 0.625),
    transform=fig.transFigure, arrowstyle="->", mutation_scale=20, color="#888", linewidth=1.8,
)
fig.add_artist(arrow1)
fig.text(0.52, 0.645, "贝叶斯定理: $p(f|D) \\propto p(D|f) \\cdot p(f)$",
         fontsize=11, color="#666", style="italic")

plt.tight_layout()
plt.subplots_adjust(top=0.93, hspace=0.45)

out = "/home/youngsure/Code/TechArt/RL/image/bayesian_update.png"
plt.savefig(out, dpi=140, bbox_inches="tight", facecolor="white")
print(f"[OK] 保存: {out}")
print(f"[INFO] 先验 std 范围: [{prior_std.min():.2f}, {prior_std.max():.2f}] (到处都 ~ {prior_std.mean():.2f})")
print(f"[INFO] 后验 std 范围: [{post_std.min():.2f}, {post_std.max():.2f}] (观测点附近小,远处大)")