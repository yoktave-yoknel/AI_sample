import codecs
import os
import subprocess
import pickle
from gensim.models.doc2vec import TaggedDocument

# ファイルパスの一覧を保持するリスト
filelist = []

# "01_filepathlist.txt"からファイルパスを読み込む
# エンコード方式をUTF-8と明示的に指定してファイルを開く
with codecs.open('01_filepathlist.txt', 'r', 'utf-8') as fin:
    for line in fin:
        # 取得した行には改行が含まれているので削除
        line = line.replace('\n', '')
        # 空行と"#"始まりの行はskipする
        if len(line) > 0 and not line.startswith('#'):
            filelist.append(line)

# xdoc2txtを実行するコマンド
# パラメータには以下のものを使用
# -8    出力のエンコードはUTF-8
# -z=0  入力ファイルサイズ無制限(初期値は256MB)
cmd = 'xdoc2txt.exe -8 -z=0 '

# 全ファイル分のテキスト情報を保持するリスト
# TaggedDocumentはファイルのパスと、そのファイルから抽出したテキストとで構成される
textlist = []

for filepath in filelist:
    # 存在しないファイルについては警告を表示し処理をskip
    if not os.path.isfile(filepath):
        print('error: file is not found. ' + filepath)
        continue
    
    f = open(filepath, mode='r' , encoding='utf-8')
    
    text = f.read()
    
    f.close
    
    textlist.append(TaggedDocument(words=text, tags=[filepath]))

# 単語リストを保存
with open('textlist.dat', 'wb') as fp:
    pickle.dump(textlist, fp)
