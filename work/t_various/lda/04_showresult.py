import MeCab
import pickle
from gensim import models

# filecorpus.datから文書のファイルパス-コーパスを紐づけた情報を復元
with open('filecorpus.dat', 'rb') as fp:
    filecorpus = pickle.load(fp)

# 生成したLDAモデルを読み込み
lda = models.LdaModel.load('lda.model')

# 各トピックに含まれる単語(関連性の高い上位10件)を表示
print('***relevant words to topic***')
for i in range(0, lda.num_topics):
    print('topic', i, ': ', lda.show_topic(i, topn=10))

# 各ドキュメントについて、各トピックに属する確率を表示
print('***relevance between document and topic***')
for doc in filecorpus:
    print(doc[0], ' : ' ,lda.get_document_topics(doc[1]))
