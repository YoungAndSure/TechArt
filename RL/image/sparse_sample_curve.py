#!/usr/bin/env python3
"""
在 J(θ) = E_z[f(θ, z)] 的 1D 曲线上:
  - 真值曲线 (灰虚线)
  - 8 个采样点 (4 个密集在 θ≈-3, 4 个稀疏分散在其他地方)
  - 多项式拟合曲线 (蓝色实线, 在密集区准、稀疏区偏)
"""

import numpy as np


# ============ 同一个 f 和 J(θ) ============
def f(x, y):
    return (
        + 2.0 * np.exp(-((x + 2) ** 2 + (y + 2) ** 2) / 2.5)
        - 1.5 * np.exp(-((x - 1) ** 2 + (y - 1) ** 2) / 2.0)
        + 1.5 * np.exp(-((x - 2) ** 2 + (y + 1) ** 2) / 2.5)
        - 1.0 * np.exp(-((x + 1) ** 2 + (y - 2) ** 2) / 2.0)
        + 1.0 * np.exp(-((x - 3) ** 2 + (y - 2) ** 2) / 2.5)
    )


np.random.seed(42)
Z_SAMPLES = np.random.uniform(-5, 5, 1000)


def J_of(t):
    return np.mean([f(t, z) for z in Z_SAMPLES])


THETA = np.linspace(-5, 5, 200)
J = np.array([J_of(t) for t in THETA])


# ============ 采样点: 4 个密集 + 4 个稀疏 ============
np.random.seed(123)
sample_thetas = np.array([-3.8, -3.4, -3.0, -2.6,  # 密集簇 θ≈-3
                          -1.0, 0.6, 2.5, 4.2])   # 稀疏点

# 加点噪声模拟真实采样误差
sample_J = np.array([J_of(t) + np.random.normal(0, 0.015) for t in sample_thetas])


# ============ 多项式拟合 (degree 5) ============
DEGREE = 5
COEFFS = np.polyfit(sample_thetas, sample_J, deg=DEGREE)
fitted_theta = np.linspace(-5, 5, 200)
fitted_J = np.polyval(COEFFS, fitted_theta)


# ============ 像素映射 ============
VB_W, VB_H = 720, 400
ML, MR, MT, MB = 70, 40, 55, 55
PW = VB_W - ML - MR
PH = VB_H - MT - MB

all_J_min = min(J.min(), fitted_J.min(), sample_J.min()) - 0.15
all_J_max = max(J.max(), fitted_J.max(), sample_J.max()) + 0.15
J_MIN, J_MAX = all_J_min, all_J_max


def to_px(theta_val, j_val):
    x = ML + (theta_val + 5) / 10 * PW
    y = MT + PH - (j_val - J_MIN) / (J_MAX - J_MIN) * PH
    return x, y


# ============ SVG ============
SVG_HEADER = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}" font-family="'Noto Sans CJK JP','PingFang SC','Microsoft YaHei',sans-serif">
  <defs>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#3a7bd9"/>
    </marker>
  </defs>
  <rect width="{VB_W}" height="{VB_H}" fill="#ffffff"/>
'''


def grid_and_axes():
    """网格 + 坐标轴 + 轴标题。"""
    parts = []
    # 网格
    for i in range(-5, 6):
        x, _ = to_px(i, 0)
        if ML <= x <= ML + PW:
            parts.append(f'  <line x1="{x:.1f}" y1="{MT}" x2="{x:.1f}" y2="{MT+PH}" stroke="#eeeeee" stroke-width="1"/>\n')
    parts.append(f'  <line x1="{ML}" y1="{MT+PH}" x2="{ML+PW}" y2="{MT+PH}" stroke="#666" stroke-width="1.5"/>\n')
    parts.append(f'  <line x1="{ML}" y1="{MT}" x2="{ML}" y2="{MT+PH}" stroke="#666" stroke-width="1.5"/>\n')
    for i in range(-5, 6):
        x, _ = to_px(i, 0)
        parts.append(f'  <line x1="{x:.1f}" y1="{MT+PH}" x2="{x:.1f}" y2="{MT+PH+4}" stroke="#666"/>\n')
        parts.append(f'  <text x="{x:.1f}" y="{MT+PH+18}" text-anchor="middle" font-size="10" fill="#666">{i}</text>\n')
    j_lo = int(np.floor(J_MIN))
    j_hi = int(np.ceil(J_MAX))
    for j in range(j_lo, j_hi + 1):
        _, y = to_px(0, j)
        if MT <= y <= MT + PH:
            parts.append(f'  <line x1="{ML-4}" y1="{y:.1f}" x2="{ML}" y2="{y:.1f}" stroke="#666"/>\n')
            parts.append(f'  <text x="{ML-8}" y="{y+3:.1f}" text-anchor="end" font-size="10" fill="#666">{j}</text>\n')
    parts.append(f'  <text x="{ML+PW/2:.1f}" y="{MT+PH+40}" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">θ (待调参数)</text>\n')
    parts.append(f'  <text x="15" y="{MT+PH/2:.1f}" text-anchor="middle" font-size="13" fill="#333" font-weight="bold" transform="rotate(-90,15,{MT+PH/2:.1f})">E_z[f(θ, z)]</text>\n')
    return "".join(parts)


# 真值曲线 (灰虚线)
true_path = "M " + " L ".join(
    f"{to_px(t, j)[0]:.1f},{to_px(t, j)[1]:.1f}" for t, j in zip(THETA, J)
)

# 拟合曲线 (蓝色实线)
fitted_path = "M " + " L ".join(
    f"{to_px(t, j)[0]:.1f},{to_px(t, j)[1]:.1f}" for t, j in zip(fitted_theta, fitted_J)
)


out = [SVG_HEADER]
out.append(f'  <text x="{VB_W/2}" y="28" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">E_z[f(θ, z)] — 稀疏采样下的代理模型拟合</text>\n')
out.append(grid_and_axes())

# 真值曲线 (灰虚线)
out.append(f'  <path d="{true_path}" fill="none" stroke="#999" stroke-width="1.5" stroke-dasharray="5,3"/>\n')

# 拟合曲线 (蓝色实线)
out.append(f'  <path d="{fitted_path}" fill="none" stroke="#3a7bd9" stroke-width="2.5" stroke-linejoin="round"/>\n')

# 标注 "密集采样区" 和 "稀疏采样区"
# 密集区: θ ≈ -3
dense_x_center, _ = to_px(-3.0, 0)
out.append(f'  <text x="{dense_x_center:.1f}" y="{MT + PH - 5:.1f}" text-anchor="middle" font-size="10" fill="#5d4d1a" font-weight="bold">密集采样区</text>\n')

# 拟合曲线与真值差距最大的位置 (找一个明显的偏差位置)
# 大约 θ≈2 附近拟合曲线偏低
gap_x, gap_y = to_px(2.0, fitted_J[np.argmin(np.abs(fitted_theta - 2.0))])
out.append(f'  <text x="{gap_x - 10:.1f}" y="{gap_y + 35:.1f}" text-anchor="middle" font-size="10" fill="#b85450" font-weight="bold">稀疏区 — 拟合偏差大</text>\n')

# 采样点
for t_s, j_s in zip(sample_thetas, sample_J):
    x, y = to_px(t_s, j_s)
    out.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#222" stroke="white" stroke-width="1.5"/>\n')

# 图例 (横向排列, 放在 x 轴标签下方, 不挡曲线)
legend_y = VB_H - 10   # 在 viewBox 底部, x 轴标签下方
legend_items = [
    ("真实 E_z[f(θ, z)]", "#999", "dash"),
    ("拟合 g(W*, θ)", "#3a7bd9", "solid"),
    ("采样点 (8 个)", None, "dot"),
]
lx_start = 100
for i, (label, color, kind) in enumerate(legend_items):
    base_x = lx_start + i * 180
    if kind == "dash":
        out.append(f'  <line x1="{base_x}" y1="{legend_y}" x2="{base_x+30}" y2="{legend_y}" stroke="{color}" stroke-width="1.5" stroke-dasharray="5,3"/>\n')
    elif kind == "solid":
        out.append(f'  <line x1="{base_x}" y1="{legend_y}" x2="{base_x+30}" y2="{legend_y}" stroke="{color}" stroke-width="2.5"/>\n')
    elif kind == "dot":
        out.append(f'  <circle cx="{base_x+15}" cy="{legend_y}" r="5" fill="#222" stroke="white" stroke-width="1.5"/>\n')
    out.append(f'  <text x="{base_x+38}" y="{legend_y+4}" font-size="11" fill="#333">{label}</text>\n')

out.append('</svg>\n')

out_path = "/home/youngsure/Code/TechArt/RL/image/sparse_sample_curve.svg"
with open(out_path, "w") as fh:
    fh.write("".join(out))
print(f"[OK] 写出: {out_path}")
print(f"[INFO] 拟合度: max |拟合 - 真实| = {np.max(np.abs(fitted_J - J)):.3f}")
print(f"[INFO] 密集区(θ≈-3)偏差: {np.max(np.abs(fitted_J[np.abs(fitted_theta + 3) < 0.5] - J[np.abs(fitted_theta + 3) < 0.5])):.3f}")
print(f"[INFO] 稀疏区(θ≈2)偏差: {np.max(np.abs(fitted_J[np.abs(fitted_theta - 2) < 0.5] - J[np.abs(fitted_theta - 2) < 0.5])):.3f}")