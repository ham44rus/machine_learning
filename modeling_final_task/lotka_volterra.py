import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 1. 微分方程式を定義する関数
# z = [x, y] は被食者と捕食者の個体数ベクトル
# t は時間、alpha, beta, delta, gamma はモデルのパラメータ
def lotka_volterra(t, z, alpha, beta, delta, gamma):
    """
    ロトカ・ヴォルテラ方程式を定義する。
    """
    x, y = z
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]

# 2. パラメータと初期条件の設定
# 理論解析との比較のため、以下の値を用いる
params = {
    'alpha': 1.5,  # 被食者の内的増殖率
    'beta': 1.0,   # 捕食率
    'delta': 1.0,  # 捕食者の増殖効率
    'gamma': 3.0,  # 捕食者の内的死亡率
}
# 初期個体数
z0 = [10.0, 5.0] # [被食者の初期値, 捕食者の初期値]

# シミュレーション時間の設定
t_span = (0, 30)  # シミュレーション期間（0～30時間）
t_eval = np.linspace(t_span[0], t_span[1], 1000)  # 評価する時間点

# 3. solve_ivp を用いた数値積分
# args にパラメータをタプルで渡す
sol = solve_ivp(
    lotka_volterra, 
    t_span, 
    z0, 
    args=(params['alpha'], params['beta'], params['delta'], params['gamma']),
    dense_output=True, # 密な出力を有効化
    t_eval=t_eval      # 評価する時間点を指定
)

# 4. 結果のプロット
# フォント設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'Arial', 'Helvetica', 'Yu Gothic', 'Meiryo']

# Figure 1: 時間変化のプロット
plt.figure(figsize=(10, 6))
plt.plot(sol.t, sol.y[0], label='被食者 (x)')
plt.plot(sol.t, sol.y[1], label='捕食者 (y)')
plt.title('ロトカ・ヴォルテラモデル：個体数の時間変化')
plt.xlabel('時間 (t)')
plt.ylabel('個体数')
plt.grid(True)
plt.legend()
plt.savefig('time_series.png', dpi=300)
plt.show()

# Figure 2: 相平面のプロット
# 共存平衡点の計算
x_eq = params['gamma'] / params['delta']
y_eq = params['alpha'] / params['beta']

plt.figure(figsize=(8, 8))
plt.plot(sol.y[0], sol.y[1], label='軌道')
plt.plot(x_eq, y_eq, 'ro', label=f'平衡点 ({x_eq:.1f}, {y_eq:.1f})')
plt.title('ロトカ・ヴォルテラモデル：相平面図')
plt.xlabel('被食者個体数 (x)')
plt.ylabel('捕食者個体数 (y)')
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.savefig('phase_plane.png', dpi=300)
plt.show()

# 以下は追加のコードで、平衡点と初期値を示した相平面図
plt.figure(figsize=(8, 8))
plt.plot(sol.y[0], sol.y[1], label='軌道')
plt.plot(x_eq, y_eq, 'ro', label=f'平衡点 ({x_eq:.1f}, {y_eq:.1f})')
plt.plot(z0[0], z0[1], 'go', label=f'初期値 ({z0[0]:.1f}, {z0[1]:.1f})')
plt.title('ロトカ・ヴォルテラモデル：相平面図（初期値と平衡点）')
plt.xlabel('被食者個体数 (x)')
plt.ylabel('捕食者個体数 (y)')
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.savefig('phase_plane_with_initial.png', dpi=300)
plt.show()