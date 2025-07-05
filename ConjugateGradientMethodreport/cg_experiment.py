import numpy as np
import time
import csv
import os
import mpmath
import mpmath.libmp
from datetime import datetime

# CG法(mpmath版)
def cg(vec_x, mat_a, vec_b, rtol, atol, max_times):
    dim = vec_x.rows
    r = vec_b - mat_a * vec_x
    p = r
    rsold = (r.T * r)[0, 0]

    init_norm_r = mpmath.norm(r)
    old_norm_r = init_norm_r
    
    for times in range(max_times):
        ap = mat_a * p
        
        alpha = rsold / (p.T * ap)[0, 0]
        
        vec_x = vec_x + alpha * p
        r = r - alpha * ap
        rsnew = (r.T * r)[0, 0]

        # 残差ノルムの更新
        new_norm_r = mpmath.norm(r)
        
        # 収束判定
        if new_norm_r <= (rtol * init_norm_r + atol):
            break
        
        beta = rsnew / rsold
        p = r + beta * p
        rsold = rsnew
        
    return times + 1, vec_x  # 反復回数は0から始まるので+1

def run_experiment(dps_values, dim_values):
    # 結果を保存するためのリスト
    results = []
    
    # 実験日時を取得
    now = datetime.now()
    date_str = now.strftime("%Y%m%d_%H%M%S")
    
    # ファイル名の設定
    csv_filename = f'cg_experiment_results_{date_str}.csv'
    txt_filename = f'cg_experiment_results_{date_str}.txt'
    
    # テキストファイルに実験情報を書き込み
    with open(txt_filename, 'w') as txtfile:
        txtfile.write("共役勾配法の精度と行列サイズに関する実験結果\n")
        txtfile.write(f"実験日時: {now.strftime('%Y年%m月%d日 %H:%M:%S')}\n\n")
        txtfile.write(f"使用する精度: {dps_values}\n")
        txtfile.write(f"使用する行列サイズ: {dim_values}\n\n")
        txtfile.write(f"実験開始: {len(dps_values) * len(dim_values)}回の実験を実行します\n\n")
    
    # CSVのヘッダー
    header = ['精度(dps)', '行列サイズ', '反復回数', '計算時間(秒)', '相対誤差']
    
    print(f"実験開始: {len(dps_values) * len(dim_values)}回の実験を実行します")
    
    # 各精度と行列サイズの組み合わせで実験
    for dps in dps_values:
        mpmath.mp.dps = dps
        print(f"\n10進精度桁数 = {mpmath.mp.dps}")
        
        # テキストファイルに記録
        with open(txt_filename, 'a') as txtfile:
            txtfile.write(f"\n10進精度桁数 = {mpmath.mp.dps}\n")
        
        for dim in dim_values:
            print(f"正方行列サイズ dim = {dim} の実験を開始...")
            
            # 行列要素を設定
            mat_a = mpmath.zeros(dim, dim)
            for i in range(dim):
                for j in range(dim):
                    mat_a[i, j] = mpmath.mpf(dim - max(i, j))
            
            # x = [1, 2, ..., dim] の真の解を生成
            vec_true_x = mpmath.matrix([mpmath.mpf(i) for i in range(1, dim + 1)])
            
            # b = A * x を計算
            vec_b = mat_a * vec_true_x

            # CG法実行
            vec_x = mpmath.zeros(dim, 1)  # 初期解をゼロベクトルに設定
            
            start_time = time.time()
            iterative_times, vec_x = cg(vec_x, mat_a, vec_b, 2.00e-20, 0.0, dim * 10)
            time_taken = time.time() - start_time
            
            # 相対誤差の計算
            relerr = mpmath.norm(vec_x - vec_true_x) / mpmath.norm(vec_true_x)
            
            # 結果の表示
            result_str = f'CG: 反復回数={iterative_times}, 時間={time_taken:.4f}秒, 相対誤差={mpmath.nstr(relerr)}'
            print(result_str)
            
            # テキストファイルに記録
            with open(txt_filename, 'a') as txtfile:
                txtfile.write(f"正方行列サイズ dim = {dim}\n")
                txtfile.write(f"{result_str}\n\n")
            
            # 結果をリストに追加
            results.append([dps, dim, iterative_times, time_taken, float(relerr)])
    
    # 結果をCSVファイルに保存
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(results)
    
    # 結果の要約をテキストファイルに追加
    with open(txt_filename, 'a') as txtfile:
        txtfile.write("\n\n実験結果の要約:\n")
        txtfile.write("精度(dps) | 行列サイズ | 反復回数 | 計算時間(秒) | 相対誤差\n")
        txtfile.write("-" * 70 + "\n")
        
        for result in results:
            summary_line = f"{result[0]:<10} | {result[1]:<10} | {result[2]:<8} | {result[3]:<12.4f} | {result[4]:.4e}"
            txtfile.write(summary_line + "\n")
    
    print(f"\n実験完了！結果は以下のファイルに保存されました:")
    print(f"CSVファイル: {csv_filename}")
    print(f"テキストファイル: {txt_filename}")
    
    return results

if __name__ == '__main__':
    # 実験パラメータ
    dps_values = [30, 50, 100, 200, 500]
    dim_values = [500, 600, 700, 800, 900, 1000]
    
    print("共役勾配法の精度と行列サイズに関する実験")
    print(f"使用する精度: {dps_values}")
    print(f"使用する行列サイズ: {dim_values}")
    
    # 実験の実行
    results = run_experiment(dps_values, dim_values)
    
    # 結果の要約
    print("\n実験結果の要約:")
    print("精度(dps) | 行列サイズ | 反復回数 | 計算時間(秒) | 相対誤差")
    print("-" * 70)
    
    for result in results:
        print(f"{result[0]:<10} | {result[1]:<10} | {result[2]:<8} | {result[3]:<12.4f} | {result[4]:.4e}")