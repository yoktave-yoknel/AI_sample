import pickle
from gensim import corpora
from gensim import models
from gensim.models.doc2vec import TaggedDocument

# ファイル名称
# analyze_documents.pyから実行されるので、そこからの相対パス
WORDS_DOCUMENTS = 'wordsdocs.dat'

# TaggedDocumentを読み込み
# tag=文書ファイルパス、words=文書中の単語リスト
with open(WORDS_DOCUMENTS, 'rb') as fp:
    wordsdocs = pickle.load(fp)

# 単語リストをTaggedDoucumentから抽出
words = []
for wordsdoc in wordsdocs:
    words.append(wordsdoc.words)

print('=== 辞書作成中 ===')

# 単語->id変換の辞書作成
dictionary = corpora.Dictionary(words)

print('=== TF-IDF算出中 ===')

# 文書ごとに含まれる単語idの個数を算出
corpus = list(map(dictionary.doc2bow, words))

# 前処理として単語にTF-IDFで重み付け
tfidf_model = models.TfidfModel(corpus)
corpus_tfidf = tfidf_model[corpus]

print('=== LDA実施中 ===')
while True:
    print('=== トピック数を指定してください。 ===')
    topic_num = input('>> ')
    if topic_num.isdecimal():
        break
    else :
        print('=== 数字を入力してください。 ===')

# LDAモデルの生成
lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, num_topics=int(topic_num), id2word=dictionary)

# 各トピックに含まれる単語を表示
print('=== 各トピックに含まれる単語を表示します。 ===')
while True:
    print('=== いくつ表示しますか？ ===')
    output_str = input('>> ')
    if output_str.isdecimal():
        break
    else :
        print('=== 数字を入力してください。 ===')

for i in range(0, lda.num_topics):
    print('topic', i, ': ', lda.show_topic(i, topn=int(output_str)))

# 文書が各トピックに属する確率を表示
print('=== 文書が各トピックに属する確率を表示します。 ===')
for (wordsdoc, corpus_part) in zip(wordsdocs, corpus):
    print(wordsdoc.tags[0], ' : ' , lda.get_document_topics(corpus_part))
