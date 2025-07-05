import numpy as np
import time

# cg_mpmath.py: 多倍長精度CG 法 
import mpmath  # 多倍長精度計算
import mpmath.libmp  # 可能ならばgmpy2を使用

# 計算精度初期設定
mpmath.mp.dps = 30  # 10進精度桁数
input_dps = input('10進精度桁数 dps (推奨: 30, 50, 100, 200, 500): ')
if int(input_dps) > mpmath.mp.dps:
    mpmath.mp.dps = int(input_dps)
print(f'10進精度桁数 = {mpmath.mp.dps}')

# CG法(mpmath版)
def cg(vec_x, mat_a, vec_b, rtol, atol, max_times):
    dim = vec_x.rows
    r = vec_b - mat_a * vec_x
    p = r
    rsold = (r.T * r)[0, 0]  # 内積計算を修正

    init_norm_r = mpmath.norm(r)
    old_norm_r = init_norm_r

    print("CG: iteration, time=, relerr(vec_x)=, relerr(vec_b)=, norm_r_rel")  # 追加情報
    
    for times in range(max_times):
        ap = mat_a * p
        
        # 内積計算を修正
        alpha = rsold / (p.T * ap)[0, 0]
        
        vec_x = vec_x + alpha * p
        r = r - alpha * ap
        rsnew = (r.T * r)[0, 0]  # 内積計算を修正

        

        # 残差ノルムの更新
        new_norm_r = mpmath.norm(r)
        
        # 収束判定
        if new_norm_r <= (rtol * init_norm_r + atol):
            break
        
        beta = rsnew / rsold
        p = r + beta * p
        rsold = rsnew
        
        # 進捗表示
        print(f'{times}, {mpmath.nstr(new_norm_r / init_norm_r)}')

    return times, vec_x

# メイン実行部分
if __name__ == '__main__':
    str_dim = input('正方行列サイズ dim = ')
    dim = int(str_dim)

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
    # rtol, atolは資料から2.00-20, 0.0と読み取れる
    iterative_times, vec_x = cg(vec_x, mat_a, vec_b, 2.00e-20, 0.0, dim * 10)
    time_taken = time.time() - start_time
    
    # 相対誤差の計算
    relerr = mpmath.norm(vec_x - vec_true_x) / mpmath.norm(vec_true_x)
    
    print(f'CG: iteration={iterative_times}, time={time_taken:.4f}s')
    print(f'relerr(vec_x)={mpmath.nstr(relerr)}')