import MeCab
import pickle
from gensim import corpora
from gensim import models
from gensim.models.doc2vec import TaggedDocument

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
    #lines = mecab.parse(doc.words.decode('utf-8')).splitlines()
    lines = mecab.parse(doc.words).splitlines()
    words = []
    for line in lines:
        chunks = line.split('\t')
        # レポートの各行から、動詞・形容詞・名詞(数を除く)の情報のみを取り出す
        if len(chunks) > 3 and (chunks[3].startswith('動詞') or chunks[3].startswith('形容詞') or (chunks[3].startswith('名詞') and not chunks[3].startswith('名詞-数'))):
            words.append(chunks[0])
    sentences.append(TaggedDocument(words=words, tags=doc.tags))

# textsは文書ごとの単語リスト
texts = []
for sentence in sentences:
    texts.append(sentence.words)

# 単語->id変換の辞書作成
dictionary = corpora.Dictionary(texts)

# 文書ごと含まれる単語idの個数を算出
corpus = list(map(dictionary.doc2bow,texts))

# 文書のファイルパスとコーパスを紐づけて保存
filecorpus = []
for (sentence, corpus_part) in zip(sentences, corpus):
    filecorpus.append([sentence.tags, corpus_part])
with open('filecorpus.dat', 'wb') as fp:
    pickle.dump(filecorpus, fp)

# LDAで分類するトピックの数を入力してもらう
topic_N = ''
while True:
    print('いくつに分類しますか？')
    topic_N = input('>> ') # python3系でのやりかた
    if topic_N.isdecimal():
        break
    else :
        print('数字じゃないとだめです。')

# 前処理として単語にTF-IDFで重み付け
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

# LDAモデルの生成
lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, num_topics=topic_N, id2word=dictionary)

# 生成したモデルを保存
lda.save('lda.model')
