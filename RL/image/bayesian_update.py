#!/usr/bin/env python3
"""
贝叶斯优化示意: 先验 p(θ) → 观测样本 D → 后验 p(θ|D)
用 matplotlib 画 3 个上下排列的子图(标准坐标系),自带清晰坐标轴。
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False


def gaussian_pdf(mu, sigma, x):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


# ============ 数据 ============
THETA_RANGE = (-4, 4)
THETA = np.linspace(*THETA_RANGE, 200)

# 先验: 宽高斯
MU_PRIOR, SIGMA_PRIOR = 0.0, 1.5
P_PRIOR = gaussian_pdf(MU_PRIOR, SIGMA_PRIOR, THETA)

# 观测样本: 10 个点集中在 θ≈2
np.random.seed(42)
SAMPLE_THETAS = np.clip(np.random.normal(2.0, 0.7, 10), *THETA_RANGE)

# 后验: 窄高斯, 中心被样本拉过去
MU_POST, SIGMA_POST = 1.9, 0.5
P_POST = gaussian_pdf(MU_POST, SIGMA_POST, THETA)


# ============ 绘图: 3 个上下子图 ============
fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

# ---------- Panel 1: 先验 ----------
axes[0].plot(THETA, P_PRIOR, color="#3a7bd9", linewidth=2.8)
axes[0].fill_between(THETA, P_PRIOR, alpha=0.15, color="#3a7bd9")
axes[0].axvline(x=0, color="gray", linestyle="--", alpha=0.6, linewidth=1)
axes[0].text(0, P_PRIOR.max() * 0.92, "μ=0", ha="center", color="gray", fontsize=10, style="italic")
axes[0].set_title("先验  p(θ)  —  N(μ=0, σ=1.5)",
                  fontsize=14, color="#3a7bd9", fontweight="bold", loc="left")
axes[0].set_ylabel("密度", fontsize=11)
axes[0].grid(alpha=0.3)
axes[0].set_xlim(*THETA_RANGE)
axes[0].text(0.02, 0.92, "宽分布:对 θ 一无所知",
             transform=axes[0].transAxes, fontsize=10, color="#666", style="italic")

# ---------- Panel 2: 观测样本 ----------
# 用 stripplot 风格: 一行散点 + jitter
np.random.seed(99)
y_jitter = np.random.uniform(-0.08, 0.08, size=len(SAMPLE_THETAS))
axes[1].scatter(SAMPLE_THETAS, y_jitter, s=120, color="#222",
                edgecolors="white", linewidths=1.5, zorder=3)
axes[1].axhline(y=0, color="#999", linewidth=1, zorder=1)
axes[1].set_title(f"观测样本  D  —  {len(SAMPLE_THETAS)} 个 (θᵢ, aᵢ) 点,集中在 θ≈2",
                  fontsize=14, color="#222", fontweight="bold", loc="left")
axes[1].set_ylabel("样本", fontsize=11)
axes[1].set_ylim(-0.4, 0.4)
axes[1].set_yticks([])
axes[1].grid(alpha=0.3, axis="x")
axes[1].text(0.02, 0.85, "看到这些样本",
             transform=axes[1].transAxes, fontsize=10, color="#666", style="italic")

# ---------- Panel 3: 后验 ----------
axes[2].plot(THETA, P_POST, color="#d9534f", linewidth=2.8)
axes[2].fill_between(THETA, P_POST, alpha=0.15, color="#d9534f")
axes[2].axvline(x=2.0, color="#5cb85c", linestyle="--", alpha=0.7, linewidth=1.5,
                label="真实最优点 θ* ≈ 2.0")
axes[2].set_title("后验  p(θ | D)  —  N(μ=1.9, σ=0.5)",
                  fontsize=14, color="#d9534f", fontweight="bold", loc="left")
axes[2].set_xlabel("θ", fontsize=12)
axes[2].set_ylabel("密度", fontsize=11)
axes[2].legend(loc="upper left", fontsize=10)
axes[2].grid(alpha=0.3)
axes[2].text(0.02, 0.92, "窄分布:高概率在 θ≈2 附近",
             transform=axes[2].transAxes, fontsize=10, color="#666", style="italic")

# ---------- 总标题 ----------
fig.suptitle("贝叶斯优化: 先验  →  观测  →  后验",
             fontsize=17, fontweight="bold", y=0.995)

# ---------- 面板之间的箭头 + 公式 ----------
import matplotlib.patches as mpatches

# 箭头 1: 先验 → 观测
arrow1 = mpatches.FancyArrowPatch(
    (0.5, 0.665), (0.5, 0.625),
    transform=fig.transFigure,
    arrowstyle="->", mutation_scale=20, color="#888", linewidth=1.8,
)
fig.add_artist(arrow1)
fig.text(0.52, 0.643, "贝叶斯更新  p(θ|D) ∝ p(D|θ)·p(θ)",
         fontsize=11, color="#666", style="italic")

# 箭头 2: 观测 → 后验
arrow2 = mpatches.FancyArrowPatch(
    (0.5, 0.335), (0.5, 0.300),
    transform=fig.transFigure,
    arrowstyle="->", mutation_scale=20, color="#888", linewidth=1.8,
)
fig.add_artist(arrow2)
fig.text(0.52, 0.318, "得到分布后可算 P(θ ≈ θ*)",
         fontsize=11, color="#666", style="italic")

plt.tight_layout()
plt.subplots_adjust(top=0.94, hspace=0.35)

out = "/home/youngsure/Code/TechArt/RL/image/bayesian_update.png"
plt.savefig(out, dpi=140, bbox_inches="tight", facecolor="white")
print(f"[OK] 保存: {out}")
plt.close()