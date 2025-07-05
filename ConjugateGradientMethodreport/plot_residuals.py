import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import matplotlib
import locale




# 日本語フォント設定
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Hiragino Sans GB', 'Arial']
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# マイナス記号を通常のハイフンに置き換え
matplotlib.rcParams['axes.unicode_minus'] = False

# CSV実験結果ファイルのパス
csv_file = '/Users/rintaro/Downloads/Github_private/machine_learning/ConjugateGradientMethodreport/cg_experiment_results_20250705_004836.csv'

def load_experiment_data(csv_file):
    """実験データをロードしてデータフレームとして返す"""
    if not os.path.exists(csv_file):
        print(f"エラー: ファイル {csv_file} が見つかりません。")
        return None
    
    df = pd.read_csv(csv_file)
    print("実験データの概要:")
    print(df.head())
    return df

def plot_convergence_by_precision(df):
    """精度ごとの反復回数と行列サイズの関係をプロット"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 各精度レベルのデータをプロット
    for dps in sorted(df['精度(dps)'].unique()):
        dps_data = df[df['精度(dps)'] == dps]
        ax.plot(dps_data['行列サイズ'], dps_data['反復回数'], 'o-', linewidth=2, 
                label=f'dps={dps}')
    
    ax.set_xlabel('行列サイズ', fontsize=12)
    ax.set_ylabel('反復回数', fontsize=12)
    ax.set_title('多倍長精度CG法: 精度(dps)と反復回数の関係', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('mpmath_iterations_plot.png', dpi=300)
    print("反復回数のグラフを保存しました: mpmath_iterations_plot.png")
    
def plot_time_by_precision(df):
    """精度ごとの計算時間と行列サイズの関係をプロット"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 各精度レベルのデータをプロット
    for dps in sorted(df['精度(dps)'].unique()):
        dps_data = df[df['精度(dps)'] == dps]
        ax.plot(dps_data['行列サイズ'], dps_data['計算時間(秒)'], 'o-', linewidth=2,
                label=f'dps={dps}')
    
    ax.set_xlabel('行列サイズ', fontsize=12)
    ax.set_ylabel('計算時間 (秒)', fontsize=12)
    ax.set_title('多倍長精度CG法: 精度(dps)と計算時間の関係', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('mpmath_time_plot.png', dpi=300)
    print("計算時間のグラフを保存しました: mpmath_time_plot.png")

def plot_time_vs_matrix_size(df):
    """行列サイズと計算時間の関係を対数スケールでプロット"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 各精度レベルのデータをプロット
    for dps in sorted(df['精度(dps)'].unique()):
        dps_data = df[df['精度(dps)'] == dps]
        ax.loglog(dps_data['行列サイズ'], dps_data['計算時間(秒)'], 'o-', linewidth=2,
                 label=f'dps={dps}')
    
    ax.set_xlabel('行列サイズ (対数スケール)', fontsize=12)
    ax.set_ylabel('計算時間 (秒, 対数スケール)', fontsize=12)
    ax.set_title('多倍長精度CG法: 行列サイズと計算時間の関係 (対数スケール)', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('mpmath_time_loglog_plot.png', dpi=300)
    print("対数スケールの計算時間グラフを保存しました: mpmath_time_loglog_plot.png")

def plot_error_by_precision(df):
    """精度ごとの相対誤差と行列サイズの関係をプロット"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 各精度レベルのデータをプロット
    for dps in sorted(df['精度(dps)'].unique()):
        dps_data = df[df['精度(dps)'] == dps]
        ax.semilogy(dps_data['行列サイズ'], dps_data['相対誤差'], 'o-', linewidth=2,
                   label=f'dps={dps}')
    
    ax.set_xlabel('行列サイズ', fontsize=12)
    ax.set_ylabel('相対誤差 (対数スケール)', fontsize=12)
    ax.set_title('多倍長精度CG法: 精度(dps)と相対誤差の関係', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('mpmath_error_plot.png', dpi=300)
    print("相対誤差のグラフを保存しました: mpmath_error_plot.png")

def plot_combined_results(df):
    """精度、反復回数、計算時間の3Dプロット"""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # カラーマップの準備
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(df['精度(dps)'].min(), df['精度(dps)'].max())
    
    # 各行列サイズごとにマーカーを変える
    markers = ['o', 's', '^', 'D', 'v', 'p']
    sizes = sorted(df['行列サイズ'].unique())
    
    for i, size in enumerate(sizes):
        size_data = df[df['行列サイズ'] == size]
        
        # 精度、反復回数、計算時間の関係をプロット
        scatter = ax.scatter(
            size_data['精度(dps)'], 
            size_data['反復回数'], 
            size_data['計算時間(秒)'],
            c=size_data['精度(dps)'],
            cmap=cmap,
            norm=norm,
            marker=markers[i % len(markers)],
            s=80,
            label=f'行列サイズ={size}'
        )
        
        # 各ポイントを線で接続
        ax.plot(
            size_data['精度(dps)'],
            size_data['反復回数'],
            size_data['計算時間(秒)'],
            '-',
            alpha=0.5
        )
    
    ax.set_xlabel('精度 (dps)', fontsize=12)
    ax.set_ylabel('反復回数', fontsize=12)
    ax.set_zlabel('計算時間 (秒)', fontsize=12)
    ax.set_title('多倍長精度CG法: 精度・反復回数・計算時間の関係', fontsize=14)
    
    # カラーバーと凡例を追加
    cbar = fig.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('精度 (dps)', fontsize=12)
    ax.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig('mpmath_3d_plot.png', dpi=300)
    print("3Dグラフを保存しました: mpmath_3d_plot.png")

def plot_iteration_efficiency(df):
    """精度と反復効率（反復回数/行列サイズ）の関係をプロット"""
    # 反復効率 = 反復回数/行列サイズ
    df['反復効率'] = df['反復回数'] / df['行列サイズ']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 各行列サイズごとにプロット
    for size in sorted(df['行列サイズ'].unique()):
        size_data = df[df['行列サイズ'] == size]
        ax.plot(size_data['精度(dps)'], size_data['反復効率'], 'o-', linewidth=2,
               label=f'行列サイズ={size}')
    
    ax.set_xlabel('精度 (dps)', fontsize=12)
    ax.set_ylabel('反復効率 (反復回数/行列サイズ)', fontsize=12)
    ax.set_title('多倍長精度CG法: 精度と反復効率の関係', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('mpmath_efficiency_plot.png', dpi=300)
    print("反復効率のグラフを保存しました: mpmath_efficiency_plot.png")

def generate_all_plots(csv_file):
    """すべてのグラフを生成する"""
    df = load_experiment_data(csv_file)
    if df is None:
        return
    
    print(f"\n実験データの統計情報:")
    print(df.describe())
    
    # 各種グラフの生成
    plot_convergence_by_precision(df)
    plot_time_by_precision(df)
    plot_time_vs_matrix_size(df)
    plot_error_by_precision(df)
    plot_combined_results(df)
    plot_iteration_efficiency(df)
    
    print("\nすべてのグラフを生成しました。")

if __name__ == "__main__":
    print("共役勾配法の実験データの可視化ツール")
    print(f"データファイル: {csv_file}")
    
    # すべてのグラフを生成
    generate_all_plots(csv_file)