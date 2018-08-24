import pickle
from operator import itemgetter
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

# id->単語変換の辞書作成
dictionary_reverse = {}
for dic in dictionary.token2id.items():
    dictionary_reverse[dic[1]]=dic[0]

print('=== TF-IDF算出中 ===')

# 文書ごとに含まれる単語idの個数を算出
corpus = list(map(dictionary.doc2bow, words))

# TF-IDF modelの生成
tfidf_model = models.TfidfModel(corpus)

# 文書に含まれる単語のTF-IDFを算出
corpus_tfidf = tfidf_model[corpus]

# id->単語へ変換
texts_tfidf = [] # id -> 単語表示に変えた文書ごとのTF-IDF
for doc in corpus_tfidf:
    text_tfidf = []
    for word in doc:
        text_tfidf.append([dictionary_reverse[word[0]],word[1]])
    texts_tfidf.append(text_tfidf)

# 表示
print('=== 各文書中の単語から、TF-IDFの上位を表示します。 ===')
while True:
    print('=== 上位いくつを表示しますか？ ===')
    output_str = input('>> ')
    if output_str.isdecimal():
        break
    else :
        print('=== 数字を入力してください。 ===')

output_num = int(output_str)
for (wordsdoc, vector) in zip(wordsdocs, texts_tfidf):
    print(wordsdoc.tags)
    sorted_vector = sorted(vector, key=itemgetter(1), reverse=True)
    for i in range(output_num):
        print(sorted_vector[i])
