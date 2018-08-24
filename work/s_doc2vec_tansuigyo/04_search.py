import pickle
import sys
import MeCab
from gensim import models
from gensim.models.doc2vec import TaggedDocument

arg_list = ('list')
arg_search = ('search')
arg_search_Vector = ('search_vec')

# 学習済みのモデルを読み込む
model = models.Doc2Vec.load('doc2vec.model')

# textlist.datからTaggedDocumentのリストを復元
# ファイルのパス(tags)とそのテキスト情報(words)で構成される
# ※引数のファイルパスを学習済みか判定のため。暫定的に使用(本来はDoc2Vecモデルから取得できるかも)
with open('textlist.dat', 'rb') as fp:
    textlist = pickle.load(fp)

def showFileList():
    # 学習済みのファイルを一覧表示
    print('trained files are ...')
    for info in textlist:
        print(info.tags[0])

def showSimilarFile(filepath):
    # 引数で指定されたファイルが、学習済みのファイルであるかを確認
    istrained = False
    for info in textlist:
        if(info.tags[0] == filepath):
            istrained = True
            break
    if not istrained:
        print('"{0}" is not trained file. check valid file by "{1}" option' . format(filepath, arg_list))
        quit()

    # 指定されたファイルに類似するものを表示
    most_similar_texts = model.docvecs.most_similar(filepath)
    print('similar files are ...')
    for similar_text in most_similar_texts:
        print(similar_text)

def showSimilarFileVector(filePath2):
    # 引数で指定されたファイルが、学習済みのファイルであるかを確認
    istrained = False
    for doc in textlist:
        if(doc.tags[0] == filePath2):
            istrained = True
            break
    if not istrained:
        print('"{0}" is not trained file. check valid file by "{1}" option' . format(filePath2, arg_list))
        quit()
    
    # MeCabインスタンスを生成
    # 単語分解した際の出力フォーマットを"chasen"形式にする
    mecab = MeCab.Tagger("-Ochasen")

    # 全ファイル分のTaggedDocumentを保持するリスト
    # TaggedDocumentはファイルのパスと、そのファイルに含まれる単語リストとで構成される
    sentences = []
    i = 1
        
    # テキスト情報を単語に分解し、そのレポートを行ごとに格納
    # テキスト情報はエンコードデータとなっているため、utf-8にデコードすることで文字列として扱うことができる
    lines = mecab.parse(doc.words).splitlines()
    words = []
    for line in lines:
        chunks = line.split('\t')
        # レポートの各行から、動詞・形容詞・名詞(数を除く)の情報のみを取り出す
        if len(chunks) > 3 and (chunks[3].startswith('動詞') or chunks[3].startswith('形容詞') or (chunks[3].startswith('名詞') and not chunks[3].startswith('名詞-数'))):
            words.append(chunks[0])
    #sentences.append(TaggedDocument(words=words, tags=doc.tags))
    
    inferred_vector = model.infer_vector(words)

    # 指定されたファイルに類似するものを表示
    most_similar_texts = model.docvecs.most_similar([inferred_vector], topn=10)
    print('similar files are ...')
    for similar_text in most_similar_texts:
        print(similar_text)

def printUsage():
    print('Usage:')
    print(' {0} {1} -> show valid filepath list'.format(args[0], arg_list))
    print(' {0} {1} <filepath> -> search similar file(s) to <filepath>'.format(args[0], arg_search))

if __name__ == '__main__':
    # 引数チェック("list"または"search <filename>")
    args = sys.argv
    if (len(args) < 2 or 3 < len(args)):
        printUsage()
        quit()

    if args[1] == arg_list:
        # 学習済みファイルの一覧を出力
        showFileList()
    elif args[1] == arg_search:
        # 指定されたファイルに類似するものを出力
        showSimilarFile(args[2])
    elif args[1] == arg_search_Vector:
        # 指定されたファイルに類似するものを出力
        showSimilarFileVector(args[2])
    else:
        printUsage()
