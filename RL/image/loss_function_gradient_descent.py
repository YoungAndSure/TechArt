#!/usr/bin/env python3
"""
画损失函数 L(W) = (1/n) Σᵢ |g(W,θᵢ) − aᵢ|² 的 3D loss landscape,
含多个局部最小值 + 梯度下降轨迹。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False


# ============ 损失函数 (示意,形式上等价 MSE) ============
def loss(W1, W2):
    """L(W) — 含 1 个全局最小值 + 1 个局部最小值。"""
    return (
        # 全局最小值: 深度 2.5 的负高斯在 (-2, -2)
        - 2.5 * np.exp(-((W1 + 2) ** 2 + (W2 + 2) ** 2) / 1.5)
        # 局部最小值: 较浅的负高斯在 (2, -1)
        - 1.2 * np.exp(-((W1 - 2) ** 2 + (W2 + 1) ** 2) / 1.5)
        # 远离原点的二次抬升 (让边缘高, 看起来像山谷地形)
        + 0.08 * (W1 ** 2 + W2 ** 2)
    )


# ============ 数值梯度 ============
def grad_loss(W1, W2, delta=0.05):
    dW1 = (loss(W1 + delta, W2) - loss(W1 - delta, W2)) / (2 * delta)
    dW2 = (loss(W1, W2 + delta) - loss(W1, W2 - delta)) / (2 * delta)
    return dW1, dW2


# ============ 网格 (画 3D 曲面 + 底部等高线) ============
W1 = np.linspace(-5, 5, 200)
W2 = np.linspace(-5, 5, 200)
W1g, W2g = np.meshgrid(W1, W2)
L = loss(W1g, W2g)

# 找全局最小值位置
i_min = np.unravel_index(np.argmin(L), L.shape)
global_min_W1, global_min_W2 = W1g[i_min], W2g[i_min]
print(f"[INFO] 全局最小: W* = ({global_min_W1:.2f}, {global_min_W2:.2f}), L = {L.min():.3f}")


# ============ 梯度下降轨迹 ============
# 起点选在远离两个最小值的左下角, 沿 bowl 一路下到全局最小
W1_t, W2_t = -4.5, -4.5
eta = 0.35
trajectory = [(W1_t, W2_t, loss(W1_t, W2_t))]
for _ in range(40):
    g1, g2 = grad_loss(W1_t, W2_t)
    W1_t = W1_t - eta * g1
    W2_t = W2_t - eta * g2
    W1_t = np.clip(W1_t, -5, 5)
    W2_t = np.clip(W2_t, -5, 5)
    trajectory.append((W1_t, W2_t, loss(W1_t, W2_t)))
    if abs(g1) + abs(g2) < 0.01:
        break

traj = np.array(trajectory)
print(f"[INFO] 起点: ({traj[0,0]:.2f}, {traj[0,1]:.2f}), L = {traj[0,2]:.3f}")
print(f"[INFO] 终点: ({traj[-1,0]:.2f}, {traj[-1,1]:.2f}), L = {traj[-1,2]:.3f}")
print(f"[INFO] 步数: {len(traj)}")

# 抬高轨迹,避免被曲面遮住
traj_z = traj[:, 2] + 0.2


# ============ 绘图 ============
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection="3d")

# 3D 损失曲面 (蓝色: 浅=低=好, 深=高=差)
surf = ax.plot_surface(
    W1g, W2g, L,
    cmap="Blues_r",
    alpha=0.85,
    edgecolor="none",
    antialiased=True,
)

# 底部等高线 (topographic)
z_bottom = L.min() - 0.5
ax.contour(
    W1g, W2g, L,
    zdir="z", offset=z_bottom,
    cmap="Blues_r", alpha=0.6, levels=15,
)

# 梯度下降轨迹 (3D)
ax.plot(
    traj[:, 0], traj[:, 1], traj_z,
    color="#d9534f", linewidth=2.2,
    marker="o", markersize=5, markerfacecolor="#d9534f",
    markeredgecolor="white", markeredgewidth=0.8,
    label="梯度下降轨迹", zorder=10,
)

# 起点
ax.scatter(
    [traj[0, 0]], [traj[0, 1]], [traj_z[0]],
    color="#ff8c1a", s=160, marker="o",
    edgecolors="black", linewidths=1,
    label="起点 W₀", zorder=11,
)

# 终点 (全局最小)
ax.scatter(
    [traj[-1, 0]], [traj[-1, 1]], [traj_z[-1]],
    color="#5cb85c", s=220, marker="*",
    edgecolors="black", linewidths=1,
    label="全局最优 W*", zorder=11,
)

# 坐标轴
ax.set_xlabel("W1", fontsize=12, labelpad=10)
ax.set_ylabel("W2", fontsize=12, labelpad=10)
ax.set_zlabel("L(W)", fontsize=12, labelpad=8)
ax.set_title("L(W)", fontsize=16, pad=15)

# 视角
ax.view_init(elev=28, azim=-55)
ax.set_zlim(z_bottom, L.max() + 0.5)

# 弱化坐标面板
ax.xaxis.pane.set_alpha(0.15)
ax.yaxis.pane.set_alpha(0.15)
ax.zaxis.pane.set_alpha(0.15)

# 图例
ax.legend(loc="upper left", fontsize=10, framealpha=0.9)

# 标注终点坐标
ax.text(
    traj[-1, 0] - 1.2, traj[-1, 1] + 0.8, traj_z[-1] + 0.3,
    f"W* ≈ ({traj[-1,0]:.1f}, {traj[-1,1]:.1f})\nL* ≈ {traj[-1,2]:.2f}",
    color="#2d5e2d", fontsize=9, fontweight="bold",
)

# 标注起点坐标
ax.text(
    traj[0, 0] + 0.5, traj[0, 1] + 0.5, traj_z[0] + 0.3,
    f"W₀ = ({traj[0,0]:.1f}, {traj[0,1]:.1f})",
    color="#cc6600", fontsize=9, fontweight="bold",
)

plt.tight_layout()

out = "/home/youngsure/Code/TechArt/RL/image/loss_function_gradient_descent.png"
plt.savefig(out, dpi=90, bbox_inches="tight", facecolor="white")
print(f"[OK] 保存: {out}")
plt.close()