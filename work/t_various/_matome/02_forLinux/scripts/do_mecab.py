import MeCab
import pickle
from gensim.models.doc2vec import TaggedDocument

# ファイル名称
# analyze_documents.pyから実行されるので、そこからの相対パス
TEXT_DOCUMENTS = 'textdocs.dat'
WORDS_DOCUMENTS = 'wordsdocs.dat'

# TaggedDocumentのリストを復元
# ファイルのパス(tags)とそのテキスト情報(words)で構成される
with open(TEXT_DOCUMENTS, 'rb') as fp:
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

# 単語リストを保存
with open(WORDS_DOCUMENTS, 'wb') as fp:
    pickle.dump(sentences, fp)
