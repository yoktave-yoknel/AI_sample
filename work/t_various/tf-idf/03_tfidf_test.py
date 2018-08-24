import MeCab
import pickle
from operator import itemgetter
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


# TODO: textsは文書ごとの単語リスト
texts = []
for sentence in sentences:
    texts.append(sentence.words)

# 単語->id変換の辞書作成
dictionary = corpora.Dictionary(texts)
# id->単語変換の辞書作成
dictionary_reverse = {}
for dic in dictionary.token2id.items():
    dictionary_reverse[dic[1]]=dic[0]

# 文書ごと含まれる単語idの個数を算出
corpus = list(map(dictionary.doc2bow,texts))

# tfidf modelの生成
test_model = models.TfidfModel(corpus)

# 文書に含まれる単語のtf-idfを算出
corpus_tfidf = test_model[corpus]
# id->単語へ変換
texts_tfidf = [] # id -> 単語表示に変えた文書ごとのTF-IDF
for doc in corpus_tfidf:
    text_tfidf = []
    for word in doc:
        text_tfidf.append([dictionary_reverse[word[0]],word[1]])
    texts_tfidf.append(text_tfidf)

# 表示
print('===結果表示===')
for (sentence, vector) in zip(sentences, texts_tfidf):
    print(sentence.tags)
    sorted_vector = sorted(vector, key=itemgetter(1), reverse=True)
    for i in range(10):
        print(sorted_vector[i])
