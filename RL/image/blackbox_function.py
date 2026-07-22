#!/usr/bin/env python3
"""绘制黑盒函数 f(w1, w2) 的 3D 曲面,作为自动调参文章的示意图。"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (用于 3d projection)
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False


# ============ 黑盒函数:多个波峰(正高斯) + 多个波谷(负高斯) ============
def blackbox(x, y):
    """3 个波峰 + 2 个波谷的合成函数。"""
    return (
        + 2.0 * np.exp(-((x + 2) ** 2 + (y + 2) ** 2) / 2.5)   # 波峰 A (左上)
        - 1.5 * np.exp(-((x - 1) ** 2 + (y - 1) ** 2) / 2.0)   # 波谷 (右下偏中)
        + 1.5 * np.exp(-((x - 2) ** 2 + (y + 1) ** 2) / 2.5)   # 波峰 B (右上)
        - 1.0 * np.exp(-((x + 1) ** 2 + (y - 2) ** 2) / 2.0)   # 波谷 (左下偏中)
        + 1.0 * np.exp(-((x - 3) ** 2 + (y - 2) ** 2) / 2.5)   # 波峰 C (右下)
    )


# ============ 网格采样 ============
x = np.linspace(-5, 5, 200)
y = np.linspace(-5, 5, 200)
X, Y = np.meshgrid(x, y)
Z = blackbox(X, Y)

# 找全局最大 / 最小
i_max = np.unravel_index(np.argmax(Z), Z.shape)
i_min = np.unravel_index(np.argmin(Z), Z.shape)
max_x, max_y, max_z = X[i_max], Y[i_max], Z[i_max]
min_x, min_y, min_z = X[i_min], Y[i_min], Z[i_min]


# ============ 绘图 ============
fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection="3d")

# 曲面 (蓝色)
surf = ax.plot_surface(
    X, Y, Z,
    cmap="Blues",
    alpha=0.9,
    edgecolor="none",
    antialiased=True,
)

# 等高线投影到 z=bottom
z_bottom = Z.min() - 0.5
ax.contour(X, Y, Z, zdir="z", offset=z_bottom, cmap="Blues", alpha=0.5, levels=12)

# 全局最优点
ax.scatter([max_x], [max_y], [max_z],
           color="red", s=140, marker="*",
           edgecolors="black", linewidths=0.8, zorder=10,
           label="全局最优")

# 全局最差点(标注一个局部最高点 vs 全局最高点的对比)
ax.scatter([min_x], [min_y], [min_z],
           color="blue", s=80, marker="v",
           edgecolors="black", linewidths=0.5, zorder=10,
           label="全局最差")

# 标注文字(在最优/最差点旁边)
ax.text(max_x + 0.3, max_y, max_z + 0.3,
        f"全局最高点\nθ = {max_x:.1f}, z = {max_y:.1f}\nf(θ,z) ≈ {max_z:.2f}",
        color="darkred", fontsize=10, fontweight="bold")
ax.text(min_x + 0.3, min_y, min_z - 0.6,
        f"全局最低点\nf(θ,z) ≈ {min_z:.2f}",
        color="darkblue", fontsize=9)

# 坐标轴
ax.set_xlabel("θ (待调参数)", fontsize=12, labelpad=10)
ax.set_ylabel("z (随机变量 / 上下文)", fontsize=12, labelpad=10)
ax.set_zlabel("f(θ, z) + ε", fontsize=12, labelpad=8)
ax.set_title(
    "f(θ, z)",
    fontsize=16, pad=15,
)

# 视角
ax.view_init(elev=35, azim=-60)

# z 轴下限
ax.set_zlim(z_bottom, Z.max() + 0.5)

# 网格线弱化
ax.xaxis.pane.set_alpha(0.15)
ax.yaxis.pane.set_alpha(0.15)
ax.zaxis.pane.set_alpha(0.15)

# 图例
ax.legend(loc="upper right", fontsize=10)

plt.tight_layout()

# 保存
out_png = "/home/youngsure/Code/TechArt/RL/image/blackbox_function.png"
plt.savefig(out_png, dpi=90, bbox_inches="tight", facecolor="white")
print(f"[OK] 保存 PNG: {out_png}")
plt.close()