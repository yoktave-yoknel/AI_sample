import collections
import MeCab
import pickle
from gensim import models
from gensim.models.doc2vec import TaggedDocument

# ハイパーパラメータ:ここから
# ※学習の状況により調整すること
# 学習の上限回数
TRAIN_MAX = 30
# 学習結果の評価に用いる文書の割合(0～1)
SAMPLE_PROPORTION = 0.5
# 精度の閾値(0～1)
PASSING_PRECISION = 0.9
# ハイパーパラメータ:ここまで

# textlist.datからTaggedDocumentのリストを復元
# ファイルのパス(tags)とそのテキスト情報(words)で構成される
with open('textlist.dat', 'rb') as fp:
    textlist = pickle.load(fp)

# MeCabインスタンスを生成
# 単語分解した際の出力フォーマットを"chasen"形式にする
mecab = MeCab.Tagger("-Ochasen")

# 全ファイル分のTaggedDocumentを保持するリスト
# TaggedDocumentはファイルのパスと、そのファイルに含まれる単語リストとで構成される
sentences = []

for doc in textlist:
    # テキスト情報を単語に分解し、そのレポートを行ごとに格納
    # テキスト情報はエンコードデータとなっているため、utf-8にデコードすることで文字列として扱うことができる
    lines = mecab.parse(doc.words.decode('utf-8')).splitlines()
    words = []
    for line in lines:
        chunks = line.split('\t')
        # レポートの各行から、動詞・形容詞・名詞(数を除く)の情報のみを取り出す
        if len(chunks) > 3 and (chunks[3].startswith('動詞') or chunks[3].startswith('形容詞') or (chunks[3].startswith('名詞') and not chunks[3].startswith('名詞-数'))):
            words.append(chunks[0])
    sentences.append(TaggedDocument(words=words, tags=doc.tags))

# 学習モデルを生成
#   size: ベクトル化した際の次元数
#   alpha: 学習率
#   sample：単語を無視する際の頻度の閾値
#   min_count：学習に使う単語の最低出現回数
#   workers：学習時のスレッド数
model = models.Doc2Vec(size=400, alpha=0.0015, sample=1e-4, min_count=1, workers=4)

# Doc2Vecに単語を登録
model.build_vocab(sentences)

# 学習評価に使用するサンプル数と閾値を設定
# ※Python3の四捨五入は「最近接偶数への丸め」となっていることに注意(1.5も2.5も2に丸められる)
sample_num = int(round(len(sentences) * SAMPLE_PROPORTION, 0))
passing_thres = int(round(sample_num * PASSING_PRECISION, 0))

for x in range(TRAIN_MAX):
    print(x)
    # 学習実施
    model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
    ranks = []
    for doc_id in range(sample_num):
        # サンプルとする文書のベクトルを算出
        inferred_vector = model.infer_vector(sentences[doc_id].words)
        # 類似度の順になった文書のリストを取得
        sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
        # 文書のリストの中で、その文書自身が何番目にあるかを調査
        rank = [docid for docid, sim in sims].index(sentences[doc_id].tags[0])
        ranks.append(rank)

    print(collections.Counter(ranks))
    if collections.Counter(ranks)[0] >= passing_thres:
        break

# 学習が完了したのでモデルを保存
model.save('doc2vec.model')
