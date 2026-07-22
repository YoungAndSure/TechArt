#!/usr/bin/env python3
"""
RBF kernel 可视化:
  k(θ_i, θ_j) = exp(-||θ_i - θ_j||² / (2 l²))
左:2D 矩阵热图 (imshow)
右:3D 曲面 (plot_surface)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False


def rbf(theta_i, theta_j, l):
    """RBF kernel, 长度尺度 l。"""
    return np.exp(-((theta_i - theta_j) ** 2) / (2 * l ** 2))


# ============ 数据 ============
theta = np.linspace(-5, 5, 100)
THETA_I, THETA_J = np.meshgrid(theta, theta)
K = rbf(THETA_I, THETA_J, l=1.0)


# ============ 绘图 (左右布局: 2D 大, 1D 高) ============
fig, axes = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw={"width_ratios": [1.2, 1]})

# ----- 左: 2D 矩阵热图 -----
ax1 = axes[0]
im = ax1.imshow(
    K,
    extent=[-5, 5, -5, 5],
    origin="lower",
    cmap="viridis",
    aspect="equal",
)
ax1.set_xlabel(r"$\theta_j$", fontsize=12)
ax1.set_ylabel(r"$\theta_i$", fontsize=12)
ax1.set_title(
    r"2D 视图  $k(\theta_i, \theta_j) = \exp\!\left(-\frac{\|\theta_i-\theta_j\|^2}{2l^2}\right)$,  $l=1$"
    + "\n(对角线亮黄 = 1, 离对角线越远越暗 → 越不相关)",
    fontsize=11,
)
ax1.plot([-5, 5], [-5, 5], "w--", alpha=0.4, linewidth=1.2)
ax1.text(3.0, -4.5, r"$\theta_i = \theta_j \Rightarrow k = 1$",
         color="white", fontsize=10, style="italic", fontweight="bold")
ax1.text(-4.7, 4.7, r"距离 $\to$ 大  $\Rightarrow k \to 0$",
         color="white", fontsize=10, style="italic")
cbar = plt.colorbar(im, ax=ax1)
cbar.set_label("k 值", fontsize=10)

# ----- 右: 1D 切片 -----
ax2 = axes[1]
theta_j_fixed = 0.0
k_slice = rbf(theta, theta_j_fixed, l=1.0)
ax2.plot(theta, k_slice, color="#3a7bd9", linewidth=3.0,
         label=r"$k(\theta_i, \theta_j=0)$")
ax2.axvline(x=theta_j_fixed, color="#888", linestyle=":", alpha=0.7, linewidth=1.5,
            label=r"$\theta_j = 0$ 处 $k = 1$")
ax2.fill_between(theta, 0, k_slice, alpha=0.18, color="#3a7bd9")
ax2.set_xlabel(r"$\theta_i$", fontsize=13)
ax2.set_ylabel(r"$k(\theta_i, \theta_j=0)$", fontsize=13)
ax2.set_title(
    "1D 切片 — 固定 $\\theta_j$, 看 $k$ 随距离的衰减\n"
    + "(离 $\\theta_j$ 越近 → $k$ 越大 → 相关性越高)",
    fontsize=11,
)
ax2.set_xlim(-5, 5)
ax2.set_ylim(0, 1.05)
ax2.legend(loc="upper right", fontsize=10)
ax2.grid(alpha=0.3)

# 标注
ax2.annotate(
    "高相关区",
    xy=(0, 1.0), xytext=(-1.5, 0.85),
    fontsize=11, color="#3a7bd9", fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="#3a7bd9", alpha=0.7),
)
ax2.annotate(
    "低相关区",
    xy=(4, rbf(4, 0, 1)), xytext=(2.5, 0.5),
    fontsize=11, color="#888",
    arrowprops=dict(arrowstyle="->", color="#888", alpha=0.5),
)

# 总标题
fig.suptitle(
    r"RBF Kernel: 距离越近 $\Rightarrow$ 相关性越高",
    fontsize=15, fontweight="bold", y=0.99,
)

plt.tight_layout()

out = "/home/youngsure/Code/TechArt/RL/image/rbf_kernel.png"
plt.savefig(out, dpi=90, bbox_inches="tight", facecolor="white")
print(f"[OK] 保存: {out}")
plt.close()