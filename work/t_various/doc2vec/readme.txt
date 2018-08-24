Minimam Viable Product的なものを目指して作ってみました。

・01_filepathlist.txt
　→学習対象となるファイルパスの一覧を記載する。

・02_extracttext.py
　→"01_filepathlist.txt"に記載されたファイルからテキストを抜き出す。
　　抜き出したテキスト情報はtextlist.datとして保存する。
　　(次の学習をクラウドのマシンで行うことを想定)
　　※xdoc2txtを使用するため、Windows PC上で実行する。
　　　また、xdoc2txt.exeはこのファイルと同じところに格納しておく。

・03_train.py
　→テキストを単語分解し、学習を行う。
　　textlist.datにテキスト情報が格納されているため、これを読み込む。
　　学習の結果はdoc2vec.modelに出力し、次の検索に使用する。
　※あらかじめtextlist.datをWindows PCから学習用サーバに移動しておくこと。

・04_search.py
　→学習結果であるdoc2vec.modelを使用して類似文書の検索を行う。
　　"04_search.py list"とすることで学習済みのファイル一覧を表示し、
　　ここに表示されたものから"04_search.py search <ファイル名>"で類似文書を検索する。
