#!/usr/bin/env python

import os
import sys

# ファイル名称
TEXT_DOCUMENTS = 'textdocs.dat' # 文書をテキスト化したリスト
WORDS_DOCUMENTS = 'wordsdocs.dat' # 文書から抽出した単語のリスト
DOC2VEC_MODEL = 'doc2vec.model' # doc2vecの学習済みモデル

# 必要ファイルの確認
if not os.path.isfile(TEXT_DOCUMENTS):
    print('ファイルがありません: ' + TEXT_DOCUMENTS)
    print('Windowsで作成し、このスクリプトと同じ場所にコピーしてください。')
    sys.exit(1)

# 形態素解析の実施
if not os.path.isfile(WORDS_DOCUMENTS) :
    print('形態素解析を実行中')
    import scripts.do_mecab
    print('実行完了!')

# 各種解析の実施
print('文書解析ツールへようこそ。やりたいことを入力してください。')
print('　doc2vec: doc2vecによる解析を行います。(学習に時間がかかることがあります。)')
print('　TF-IDF: 各文書中の単語についてTF-IDFを算出します。')
print('　LDA: LDAによる解析を行います。')
print('　clear: 現在の解析データを削除します。')
print('　exit: 文書解析ツールを終了します。')

while True:
    command = input('>> ')
    if command ==  'doc2vec':
        if os.path.isfile(DOC2VEC_MODEL) :
            # 学習済みモデルがある場合、検索を実施
            import scripts.search_doc2vec
            break
        else :
            # 学習済みモデルがない場合、学習を実施
            print('学習済みモデル未作成のため、学習を行います。')
            import scripts.train_doc2vec
            break
        break
    elif command == 'TF-IDF':
        import scripts.do_tfidf
        break
    elif command == 'LDA':
        import scripts.do_lda
        break
    elif command == 'clear':
        # テキストデータおよび単語リストを削除
        if os.path.isfile(WORDS_DOCUMENTS) :
            os.remove(WORDS_DOCUMENTS)
        if os.path.isfile(TEXT_DOCUMENTS) :
            os.remove(TEXT_DOCUMENTS)
        if os.path.isfile(DOC2VEC_MODEL) :
            os.remove(DOC2VEC_MODEL)
        break
    elif command == 'exit':
        print('bye!')
        break
    else:
        print('上記のいずれかを入力してください。')
