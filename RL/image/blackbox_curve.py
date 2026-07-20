#!/usr/bin/env python3
"""
对 f(θ, z) 取期望得到 J(θ),然后:
  b.svg  : 仅画 J(θ) 的 1D 曲线
  c.svg  : 在 J(θ) 上做梯度上升,画若干步箭头收敛到 θ*
"""

import numpy as np


# ============ 黑盒函数 (与 blackbox_function.py 一致) ============
def f(x, y):
    return (
        + 2.0 * np.exp(-((x + 2) ** 2 + (y + 2) ** 2) / 2.5)
        - 1.5 * np.exp(-((x - 1) ** 2 + (y - 1) ** 2) / 2.0)
        + 1.5 * np.exp(-((x - 2) ** 2 + (y + 1) ** 2) / 2.5)
        - 1.0 * np.exp(-((x + 1) ** 2 + (y - 2) ** 2) / 2.0)
        + 1.0 * np.exp(-((x - 3) ** 2 + (y - 2) ** 2) / 2.5)
    )


# ============ 计算 J(θ) = E_z[f(θ, z)] ============
np.random.seed(42)
Z_SAMPLES = np.random.uniform(-5, 5, 1000)
THETA = np.linspace(-5, 5, 200)


def J_of(theta_val):
    """给定 θ,返回 J(θ) = E_z[f(θ, z)] 的蒙特卡洛估计。"""
    return np.mean([f(theta_val, z) for z in Z_SAMPLES])


J = np.array([J_of(t) for t in THETA])
peak_idx = int(np.argmax(J))
peak_theta = float(THETA[peak_idx])
peak_J = float(J[peak_idx])
print(f"[INFO] J(θ) 范围: [{J.min():.3f}, {J.max():.3f}]")
print(f"[INFO] 峰值: θ* = {peak_theta:.3f}, J(θ*) = {peak_J:.3f}")


# ============ 像素坐标映射 ============
VB_W, VB_H = 720, 360
ML, MR, MT, MB = 70, 40, 55, 55
PW = VB_W - ML - MR
PH = VB_H - MT - MB

THETA_MIN, THETA_MAX = -5, 5
J_PAD = 0.3
J_MIN, J_MAX = J.min() - J_PAD, J.max() + J_PAD


def to_px(theta_val, j_val):
    x = ML + (theta_val - THETA_MIN) / (THETA_MAX - THETA_MIN) * PW
    y = MT + PH - (j_val - J_MIN) / (J_MAX - J_MIN) * PH
    return x, y


# 曲线 path (用折线连接采样点)
curve_path = "M " + " L ".join(
    f"{to_px(t, j)[0]:.1f},{to_px(t, j)[1]:.1f}" for t, j in zip(THETA, J)
)


# ============ SVG 通用部分 ============
SVG_HEADER = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="'Noto Sans CJK JP','PingFang SC','Microsoft YaHei',sans-serif">
  <defs>
    <marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#d9534f"/>
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#3a7bd9"/>
    </marker>
  </defs>
  <rect width="{w}" height="{h}" fill="#ffffff"/>
'''


def axes_and_labels():
    """生成坐标轴 + 网格 + 轴标签 (两图共用)。"""
    parts = []
    # 网格 (浅灰)
    for i in range(-5, 6):
        x, _ = to_px(i, 0)
        if ML <= x <= ML + PW:
            parts.append(f'  <line x1="{x:.1f}" y1="{MT}" x2="{x:.1f}" y2="{MT+PH}" stroke="#eeeeee" stroke-width="1"/>\n')
    # x 轴
    parts.append(f'  <line x1="{ML}" y1="{MT+PH}" x2="{ML+PW}" y2="{MT+PH}" stroke="#666" stroke-width="1.5"/>\n')
    # y 轴
    parts.append(f'  <line x1="{ML}" y1="{MT}" x2="{ML}" y2="{MT+PH}" stroke="#666" stroke-width="1.5"/>\n')
    # x 轴刻度
    for i in range(-5, 6):
        x, _ = to_px(i, 0)
        parts.append(f'  <line x1="{x:.1f}" y1="{MT+PH}" x2="{x:.1f}" y2="{MT+PH+4}" stroke="#666"/>\n')
        parts.append(f'  <text x="{x:.1f}" y="{MT+PH+18}" text-anchor="middle" font-size="10" fill="#666">{i}</text>\n')
    # y 轴刻度 (每隔 1)
    j_lo = int(np.floor(J_MIN))
    j_hi = int(np.ceil(J_MAX))
    for j in range(j_lo, j_hi + 1):
        _, y = to_px(0, j)
        if MT <= y <= MT + PH:
            parts.append(f'  <line x1="{ML-4}" y1="{y:.1f}" x2="{ML}" y2="{y:.1f}" stroke="#666"/>\n')
            parts.append(f'  <text x="{ML-8}" y="{y+3:.1f}" text-anchor="end" font-size="10" fill="#666">{j}</text>\n')
    # 轴标题
    parts.append(f'  <text x="{ML+PW/2:.1f}" y="{MT+PH+40}" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">θ (待调参数)</text>\n')
    parts.append(f'  <text x="15" y="{MT+PH/2:.1f}" text-anchor="middle" font-size="13" fill="#333" font-weight="bold" transform="rotate(-90,15,{MT+PH/2:.1f})">g(W*, θ) ≈ E_z[f(θ, z)]</text>\n')
    return "".join(parts)


# ============ 图 b: 1D 曲线 ============
def make_b_svg():
    out = [SVG_HEADER.format(w=VB_W, h=VB_H)]
    out.append(f'  <text x="{VB_W/2}" y="28" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">J(θ) — 对 z 取期望后的目标曲线</text>\n')
    out.append(axes_and_labels())
    # J(θ) 曲线
    out.append(f'  <path d="{curve_path}" fill="none" stroke="#3a7bd9" stroke-width="2.5" stroke-linejoin="round"/>\n')
    # 峰值
    px, py = to_px(peak_theta, peak_J)
    out.append(f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#3a7bd9" stroke="white" stroke-width="2"/>\n')
    out.append(f'  <text x="{px+12:.1f}" y="{py-10:.1f}" font-size="11" fill="#3a7bd9" font-weight="bold">θ* ≈ {peak_theta:.2f}</text>\n')
    out.append(f'  <text x="{px+12:.1f}" y="{py+5:.1f}" font-size="10" fill="#666">J(θ*) ≈ {peak_J:.2f}</text>\n')
    out.append('</svg>\n')
    return "".join(out)


# ============ 图 c: 梯度上升 ============
def grad_ascent(theta_0, eta=1.0, n_steps=6, delta=0.05):
    """θ_{t+1} = θ_t + η · ∂J/∂θ。返回 (θ, J) 轨迹。"""
    traj = [(theta_0, J_of(theta_0))]
    th = theta_0
    for _ in range(n_steps):
        g = (J_of(th + delta) - J_of(th - delta)) / (2 * delta)
        th_new = th + eta * g
        # 截断到域内
        th_new = max(-5, min(5, th_new))
        traj.append((th_new, J_of(th_new)))
        th = th_new
        if abs(g) < 0.01:
            break
    return traj


def make_c_svg():
    # 从 θ=1.0 起步,eta=1.0,清晰看到从谷底向全局峰值爬升
    traj = grad_ascent(1.0, eta=1.0, n_steps=6)
    out = [SVG_HEADER.format(w=VB_W, h=VB_H)]
    out.append(f'  <text x="{VB_W/2}" y="28" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">θ ← θ + η · ∂g(W*, θ) / ∂θ</text>\n')
    out.append(axes_and_labels())
    # g(W*, θ) 曲线 (淡蓝背景)
    out.append(f'  <path d="{curve_path}" fill="none" stroke="#3a7bd9" stroke-width="2.5" stroke-linejoin="round" opacity="0.85"/>\n')

    # 梯度上升箭头: 从 (θ_t, J(θ_t)) 到 (θ_{t+1}, J(θ_{t+1}))
    # 箭头从下方靠近曲线,显式指向上坡方向
    for i in range(len(traj) - 1):
        t1, j1 = traj[i]
        t2, j2 = traj[i + 1]
        x1, y1 = to_px(t1, j1)
        x2, y2 = to_px(t2, j2)
        # 箭头从点下方一点出发 (避免被曲线挡住), 终点到曲线点
        offset_y = 14  # 偏移到曲线下方
        out.append(
            f'  <line x1="{x1:.1f}" y1="{y1+offset_y:.1f}" '
            f'x2="{x2:.1f}" y2="{y2+offset_y:.1f}" '
            f'stroke="#d9534f" stroke-width="2.2" marker-end="url(#arrow-red)"/>\n'
        )

    # 轨迹点
    for i, (t, j) in enumerate(traj):
        x, y = to_px(t, j)
        is_peak = (i == len(traj) - 1)
        if is_peak:
            # 峰值: 绿色星
            out.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#5cb85c" stroke="white" stroke-width="2.5"/>\n')
            out.append(f'  <text x="{x-8:.1f}" y="{y-15:.1f}" text-anchor="end" font-size="12" fill="#5cb85c" font-weight="bold">θ*</text>\n')
        elif i == 0:
            # 起点: 灰圆
            out.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#888" stroke="white" stroke-width="2"/>\n')
            out.append(f'  <text x="{x:.1f}" y="{y+30:.1f}" text-anchor="middle" font-size="11" fill="#666" font-weight="bold">θ₀ = {t:.2f}</text>\n')
        else:
            # 中间步
            out.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#d9534f" stroke="white" stroke-width="1.8"/>\n')
            out.append(f'  <text x="{x:.1f}" y="{y+30:.1f}" text-anchor="middle" font-size="10" fill="#d9534f">θ{i} = {t:.2f}</text>\n')

    # 图例 (小框)
    out.append('  <rect x="500" y="45" width="170" height="48" rx="6" fill="#fafafa" stroke="#ccc" stroke-width="1"/>\n')
    out.append('  <line x1="512" y1="60" x2="540" y2="60" stroke="#3a7bd9" stroke-width="2.5"/>\n')
    out.append('  <text x="548" y="64" font-size="10" fill="#333">g(W*, θ) 代理曲线</text>\n')
    out.append('  <line x1="512" y1="82" x2="540" y2="82" stroke="#d9534f" stroke-width="2.2" marker-end="url(#arrow-red)"/>\n')
    out.append('  <text x="548" y="86" font-size="10" fill="#333">梯度上升步</text>\n')

    out.append('</svg>\n')
    return "".join(out)


# ============ 写出 ============
def make_g_surrogate_svg():
    """图 d: 训练好的代理模型 g(W*, θ) 的曲线 (无梯度上升箭头)。"""
    out = [SVG_HEADER.format(w=VB_W, h=VB_H)]
    out.append(f'  <text x="{VB_W/2}" y="28" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">g(W*, θ) — 训练好的代理模型曲线</text>\n')
    out.append(axes_and_labels_g())
    out.append(f'  <path d="{curve_path}" fill="none" stroke="#3a7bd9" stroke-width="2.5" stroke-linejoin="round"/>\n')
    px, py = to_px(peak_theta, peak_J)
    out.append(f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#3a7bd9" stroke="white" stroke-width="2"/>\n')
    out.append(f'  <text x="{px+12:.1f}" y="{py-10:.1f}" font-size="11" fill="#3a7bd9" font-weight="bold">θ* ≈ {peak_theta:.2f}</text>\n')
    out.append(f'  <text x="{px+12:.1f}" y="{py+5:.1f}" font-size="10" fill="#666">g(W*, θ*) ≈ {peak_J:.2f}</text>\n')
    out.append('</svg>\n')
    return "".join(out)


def axes_and_labels_g():
    """与 axes_and_labels 类似,但 Y 轴标题是 g(W*, θ)。"""
    parts = []
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
    parts.append(f'  <text x="15" y="{MT+PH/2:.1f}" text-anchor="middle" font-size="13" fill="#333" font-weight="bold" transform="rotate(-90,15,{MT+PH/2:.1f})">g(W*, θ)</text>\n')
    return "".join(parts)


b_path = "/home/youngsure/Code/TechArt/RL/image/blackbox_curve_1d.svg"
c_path = "/home/youngsure/Code/TechArt/RL/image/blackbox_gradient_ascent.svg"
g_path = "/home/youngsure/Code/TechArt/RL/image/g_surrogate_curve.svg"

with open(b_path, "w") as fh:
    fh.write(make_b_svg())
print(f"[OK] 写出: {b_path}")

with open(c_path, "w") as fh:
    fh.write(make_c_svg())
print(f"[OK] 写出: {c_path}")

with open(g_path, "w") as fh:
    fh.write(make_g_surrogate_svg())
print(f"[OK] 写出: {g_path}")

# 输出梯度上升轨迹供检查
print("\n[INFO] 梯度上升轨迹:")
for i, (t, j) in enumerate(grad_ascent(1.0, eta=1.0, n_steps=6)):
    print(f"  θ{i} = {t:.3f}, J = {j:.3f}")