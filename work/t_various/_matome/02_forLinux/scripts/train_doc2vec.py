import collections
import pickle
from gensim import models
from gensim.models.doc2vec import TaggedDocument

# ハイパーパラメータを読み込み
from doc2vec_params import TRAIN_MAX # 学習の上限回数
from doc2vec_params import SAMPLE_PROPORTION # 学習結果の評価に用いる文書の割合(0～1)
from doc2vec_params import PASSING_PRECISION # 精度の閾値(0～1)

# ファイル名称
# analyze_documents.pyから実行されるので、そこからの相対パス
WORDS_DOCUMENTS = 'wordsdocs.dat'
DOC2VEC_MODEL = 'doc2vec.model'

# TaggedDocumentを読み込み
# tag=文書ファイルパス、words=文書中の単語リスト
with open(WORDS_DOCUMENTS, 'rb') as fp:
    wordsdocs = pickle.load(fp)

# 学習モデルを生成
#   size: ベクトル化した際の次元数
#   alpha: 学習率
#   sample：単語を無視する際の頻度の閾値
#   min_count：学習に使う単語の最低出現回数
#   workers：学習時のスレッド数
model = models.Doc2Vec(size=400, alpha=0.0015, sample=1e-4, min_count=1, workers=4)

# Doc2Vecに単語を登録
model.build_vocab(wordsdocs)

# 学習評価に使用するサンプル数と閾値を設定
# ※Python3の四捨五入は「最近接偶数への丸め」となっていることに注意(1.5も2.5も2に丸められる)
sample_num = int(round(len(wordsdocs) * SAMPLE_PROPORTION, 0))
passing_thres = int(round(sample_num * PASSING_PRECISION, 0))

print('=== 学習開始 ===')

for x in range(TRAIN_MAX):
    # 学習実施
    model.train(wordsdocs, total_examples=model.corpus_count, epochs=model.iter)
    ranks = []
    for doc_id in range(sample_num):
        # サンプルとする文書のベクトルを算出
        inferred_vector = model.infer_vector(wordsdocs[doc_id].words)
        # 類似度の順になった文書のリストを取得
        sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
        # 文書のリストの中で、その文書自身が何番目にあるかを調査
        rank = [docid for docid, sim in sims].index(wordsdocs[doc_id].tags[0])
        ranks.append(rank)

    if collections.Counter(ranks)[0] >= passing_thres:
        break

# 学習が完了したのでモデルを保存
model.save(DOC2VEC_MODEL)
print('=== 学習完了 ===')
