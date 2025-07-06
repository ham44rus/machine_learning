# 1. データの準備と標準化
library(clustrd) # [cite: 5]
data(USArrests) # [cite: 6]
USArrests_selected <- USArrests[, c("Murder", "Assault", "UrbanPop")] # 
USArrests_scaled <- scale(USArrests_selected)

# 2. 距離行列の計算とクラスタリングの実行
d <- dist(USArrests_scaled, method = "euclidean") # 
hc <- hclust(d, method = "ward.D2") # 

# 3. デンドログラムの作成
# hang = -1は見やすくするために枝の高さを揃えるオプション
# cex = 0.6は文字サイズを調整するオプション
plot(hc, hang = -1, cex = 0.6, main = "Dendrogram of USArrests") #

# (b)で実行したクラスタリング結果(hc)を4つのクラスターに分割
clusters <- cutree(hc, k = 4) # 

# 分割結果の確認
print(clusters)

# (参考)クラスター番号ごとに州の名前を一覧表示するプログラム
 for (i in 1:4) {
   cat("Cluster", i, ":\n")
   print(names(clusters[clusters == i]))
   cat("\n")
 }