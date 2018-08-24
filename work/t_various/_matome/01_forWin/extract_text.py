#!/usr/bin/env python

import codecs
import os
import subprocess
import sys
import pickle
from gensim.models.doc2vec import TaggedDocument

# ファイル名称
FILE_LIST = 'filepathlist.txt'
XDOC2TXT = 'xdoc2txt.exe'
TEXT_DOCUMENTS = 'textdocs.dat'

# 必要ファイルの確認
if not os.path.isfile(FILE_LIST):
    print('ファイルがありません: ' + FILE_LIST)
    sys.exit(1)
if not os.path.isfile(XDOC2TXT):
    print('ファイルがありません: ' + XDOC2TXT)
    sys.exit(1)

# ファイルパスの一覧を保持するリスト
filelist = []

# ファイル一覧からファイルパスを読み込む
# エンコード方式をUTF-8と明示的に指定してファイルを開く
with codecs.open(FILE_LIST, 'r', 'utf-8') as fin:
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
cmd = XDOC2TXT + ' -8 -z=0 '

# 全ファイル分のテキスト情報を保持するリスト
# TaggedDocumentはファイルのパスと、そのファイルから抽出したテキストとで構成される
textlist = []

for filepath in filelist:
    # 存在しないファイルについては警告を表示し処理をskip
    if not os.path.isfile(filepath):
        print('error: ファイルが見つかりません: ' + filepath)
        continue

    # xdoc2txtを実行
    # 実行失敗時にはエラー送出されるので処理をskip
    try:
        text = subprocess.check_output(cmd + filepath)
    except subprocess.CalledProcessError as e:
        print('error: xdoc2txt.exe実行時にエラーが発生しました: cmd=' + e.cmd  + ' output=' + e.output)
        continue

    textlist.append(TaggedDocument(words=text, tags=[filepath]))

# テキスト情報を保存
with open(TEXT_DOCUMENTS, 'wb') as fp:
    pickle.dump(textlist, fp)

print('処理完了しました。')
print(TEXT_DOCUMENTS + 'を生成したので、Linuxにコピーして解析を実施してください。enjoy!')
