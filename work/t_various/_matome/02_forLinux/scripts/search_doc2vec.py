import pickle
import sys
from gensim import models
from gensim.models.doc2vec import TaggedDocument

# ファイル名称
# analyze_documents.pyから実行されるので、そこからの相対パス
WORDS_DOCUMENTS = 'wordsdocs.dat'
DOC2VEC_MODEL = 'doc2vec.model'

# TaggedDocumentのリストを復元
# tag=文書ファイルパス、words=文書中の単語リスト
with open(WORDS_DOCUMENTS, 'rb') as fp:
    wordsdocs = pickle.load(fp)

print('=== 単語と学習済み文書の2通りで類似文書を検索することができます。 ===')
print('　word <調べたい単語1> <調べたい単語2> ...: 単語での検索を行います。')
print('　file <学習済み文書のファイルパス>: 学習済み文書での検索を行います。')
print('　file list: 学習済み文書のファイルパスを一覧表示します。')
print('　exit: 検索を終了します。')


words = [] # 検索に使用する単語リスト
while len(words) == 0 :
    commandline = input('>> ')
    cmd = commandline.split()
    if cmd[0] == 'word' :
        # cmdは['word', <単語1>, <単語2>, ...]となっているので、最初の'word'を除去したものを検索に使用
        cmd.pop(0)
        words = cmd
        if len(words) == 0 :
            print('=== 検索する単語を1つ以上入力してください。 ===')
    elif cmd[0] == 'file' :
        if cmd[1] == 'list' :
            print('=== 学習済み文書のファイルパスの一覧を表示します。 ===')
            for wordsdoc in wordsdocs:
                print(wordsdoc.tags[0])
        else :
            # 指定された学習済み文書の単語リストを検索に使用
            # 入力されたものが学習済み文書のファイルパスに該当するかを確認
            for wordsdoc in wordsdocs:
                if wordsdoc.tags[0] == cmd[1] :
                    words = wordsdoc.words
                    break
            if len(words) == 0 :
                print('=== 学習済み文書のファイルパスに該当するものがありません。 ===')
    elif cmd[0] == 'exit' :
        print('=== bye! ===')
        sys.exit(0)
    else :
        print('=== 上記のいずれかを入力してください。 ===')

# 学習済みのモデルを読み込む
model = models.Doc2Vec.load(DOC2VEC_MODEL)

# 単語リストからベクトルを生成し類似文書を検索
vector = model.infer_vector(words)

print('=== 類似度の高い順に最大10文書を表示します。 ===')
similar_texts = model.docvecs.most_similar([vector], topn=10)
for similar_text in similar_texts:
    print(similar_text[0])
