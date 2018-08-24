# doc2vecの学習に使用するハイパーパラメータを設定します。
# 学習を実行するするスクリプト(train_doc2vec.py)から、importされます。

# 学習の上限回数
TRAIN_MAX = 30

# 学習結果の評価に用いる文書の割合(0～1)
SAMPLE_PROPORTION = 0.5

# 精度の閾値(0～1)
PASSING_PRECISION = 0.9
