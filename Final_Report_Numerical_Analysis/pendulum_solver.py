import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 日本語フォントの設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'Arial', 'Helvetica', 'Yu Gothic', 'Meiryo', 'MS Gothic']


# 数式フォントの設定
mpl.rcParams['mathtext.default'] = 'regular'

# --- グローバル設定 ---
# 物理定数
G = 9.8  # 重力加速度 (m/s^2)
L = 1.0  # 振り子の長さ (m)
M = 1.0  # 質点の質量 (kg)


# 初期条件
THETA_0 = np.pi / 6  # 初期角度 30度 (rad)
OMEGA_0 = 0.0        # 初期角速度 (rad/s)

# シミュレーション時間
T_START = 0.0
T_END = 10.0

# --- 連立1階常微分方程式の定義 ---
# y = [theta, omega]
# dy/dt = f(t, y)
def f(t, y):
    """
    単振り子の運動方程式を記述するベクトル関数。
    Args:
        t (float): 時刻 (未使用だが、一般的なソルバーのインターフェースに合わせる)
        y (np.ndarray): 状態ベクトル [theta, omega]
    Returns:
        np.ndarray: 状態ベクトルの時間微分 [d(theta)/dt, d(omega)/dt]
    """
    theta, omega = y
    return np.array([omega, -(G / L) * np.sin(theta)])

# --- エネルギー計算関数 ---
def calculate_energy(y):
    """
    与えられた状態ベクトルから全力学的エネルギーを計算する。
    Args:
        y (np.ndarray): 状態ベクトル [theta, omega]
    Returns:
        float: 全力学的エネルギー (J)
    """
    theta, omega = y
    kinetic_energy = 0.5 * M * (L * omega)**2
    potential_energy = M * G * L * (1 - np.cos(theta))
    return kinetic_energy + potential_energy

# --- 数値解法ソルバー ---
def euler_step(f_func, t, y, h):
    """オイラー法による1ステップ計算"""
    return y + h * f_func(t, y)

def rk4_step(f_func, t, y, h):
    """4次ルンゲ・クッタ法による1ステップ計算"""
    k1 = h * f_func(t, y)
    k2 = h * f_func(t + h / 2, y + k1 / 2)
    k3 = h * f_func(t + h / 2, y + k2 / 2)
    k4 = h * f_func(t + h, y + k3)
    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6

# --- シミュレーション実行関数 ---
def run_simulation(h, solver_func):
    """
    指定された刻み幅とソルバーでシミュレーションを実行する。
    Args:
        h (float): 時間刻み幅
        solver_func (function): 使用するソルバー関数 (euler_step or rk4_step)
    Returns:
        tuple: (時間配列, 角度配列, エネルギー配列)
    """
    time_points = np.arange(T_START, T_END + h, h)
    num_steps = len(time_points)
    
    y_history = np.zeros((num_steps, 2))
    y_history[0] = np.array([THETA_0, OMEGA_0])  # 初期条件を設定
    
    energy_history = np.zeros(num_steps)
    energy_history[0] = calculate_energy(y_history[0])
    
    for i in range(num_steps - 1):
        y_history[i+1] = solver_func(f, time_points[i], y_history[i], h)
        energy_history[i+1] = calculate_energy(y_history[i+1])
        
    theta_history = y_history[:, 0]
    return time_points, theta_history, energy_history

# --- メイン処理 ---
if __name__ == '__main__':
    H_LIST = [0.1, 0.01, 0.001]
    
    # --- 表1のデータ生成 ---
    initial_energy = calculate_energy(np.array([THETA_0, OMEGA_0]))
    print("表1: 各手法と刻み幅における最終時点（t=10s）の角度とエネルギー")
    print(f"(初期エネルギー E_0 = {initial_energy:.6f} J)")
    print("| 手法 (Method) | 刻み幅 h (s) | 最終角度 θ(10) (rad) | 最終エネルギー E(10) (J) |")
    print("|:---|:---|:---|:---|")
    
    solvers = {'オイラー法': euler_step, 'RK4': rk4_step}
    results_for_table = {}

    for name, solver in solvers.items():
        for h in H_LIST:
            t, theta, energy = run_simulation(h, solver)
            print(f"| {name} | {h:<12} | {theta[-1]:.6f} | {energy[-1]:.6f} |")
            results_for_table[(name, h)] = (t, theta, energy)

    # --- 図1と図2のプロット生成 ---
    fig_angle, axes_angle = plt.subplots(3, 1, figsize=(10, 15), sharex=True)
    fig_energy, axes_energy = plt.subplots(3, 1, figsize=(10, 15), sharex=True)
    
    fig_angle.suptitle('図1: 異なる刻み幅における角度の時間変化', fontsize=16, y=0.92)
    fig_energy.suptitle('図2: 異なる刻み幅における全エネルギーの時間変化', fontsize=16, y=0.92)

    for i, h in enumerate(H_LIST):
        # オイラー法の結果を取得
        t_e, theta_e, energy_e = results_for_table[('オイラー法', h)]
        # RK4の結果を取得
        t_r, theta_r, energy_r = results_for_table[('RK4', h)]
        
        # 図1: 角度のプロット
        axes_angle[i].plot(t_e, theta_e, label='オイラー法', color='blue')
        axes_angle[i].plot(t_r, theta_r, label='RK4', color='orange')
        axes_angle[i].set_title(f'h = {h} s')
        axes_angle[i].set_ylabel('角度 $\\theta$ (rad)')
        axes_angle[i].grid(True)
        axes_angle[i].legend()
        
        # 図2: エネルギーのプロット
        axes_energy[i].plot(t_e, energy_e, label='オイラー法', color='blue')
        axes_energy[i].plot(t_r, energy_r, label='RK4', color='orange')
        axes_energy[i].axhline(y=initial_energy, color='red', linestyle='--', label='初期エネルギー')
        axes_energy[i].set_title(f'h = {h} s')
        axes_energy[i].set_ylabel('エネルギー E (J)')
        axes_energy[i].grid(True)
        axes_energy[i].legend()
        # Y軸の範囲を調整して変動を見やすくする
        energy_max = max(np.max(energy_e), np.max(energy_r))
        energy_min = min(np.min(energy_e), np.min(energy_r))
        padding = (energy_max - energy_min) * 0.1
        axes_energy[i].set_ylim(min(initial_energy, energy_min) - padding, energy_max + padding)

    axes_angle[-1].set_xlabel('時間 t (s)')
    axes_energy[-1].set_xlabel('時間 t (s)')
    
    fig_angle.tight_layout(rect=[0, 0, 1, 0.9])
    fig_energy.tight_layout(rect=[0, 0, 1, 0.9])

    fig_angle.savefig('図1_角度の時間変化.jpg', dpi=300, bbox_inches='tight')
    fig_energy.savefig('図2_エネルギーの時間変化.jpg', dpi=300, bbox_inches='tight')


    plt.show()