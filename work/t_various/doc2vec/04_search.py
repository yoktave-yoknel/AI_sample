import pickle
import sys
from gensim import models

arg_list = ('list')
arg_search = ('search')

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
        print(similar_text[0])

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
    else:
        printUsage()
