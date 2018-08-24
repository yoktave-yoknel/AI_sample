#同じディレクトリに学習済みモデルが必要 doc2vec.model
#同じディレクトリにテキストが必要　shift_jisであること
#実行時にファイル名を入力　拡張子不要(実行時はnekoでとりあえず動きます）
import MeCab
from gensim import models

DOC_PATH = './{0}.txt'
model = models.Doc2Vec.load('doc2vec.model')

# ファイルから文章を返す
def read_document(path):
    with open(path, 'r', encoding='sjis', errors='ignore') as f:
        return f.read()

# 青空文庫ファイルから作品部分のみ抜き出す
def trim_doc(doc):
    lines = doc.splitlines()
    valid_lines = []
    is_valid = False
    horizontal_rule_cnt = 0
    break_cnt = 0
    for line in lines:
        if horizontal_rule_cnt < 2 and '-----' in line:
            horizontal_rule_cnt += 1
            is_valid = horizontal_rule_cnt == 2
            continue
        if not(is_valid):
            continue
        if line == '':
            break_cnt += 1
            is_valid = break_cnt != 3
            continue
        break_cnt = 0
        valid_lines.append(line)
    return ''.join(valid_lines)

# 文章から単語に分解して返す
def split_into_words(doc, name=''):
    mecab = MeCab.Tagger("-Ochasen")
    valid_doc = trim_doc(doc)
    lines = mecab.parse(doc).splitlines()
    words = []
    for line in lines:
        chunks = line.split('\t')
        if len(chunks) > 3 and (chunks[3].startswith('動詞') or chunks[3].startswith('形容詞') or (chunks[3].startswith('名詞') and not chunks[3].startswith('名詞-数'))):
            words.append(chunks[0])
    return words

def search_similar_texts(sentences):
    newvec = model.infer_vector(sentences)
    most_similar_texts = model.docvecs.most_similar([newvec], topn=10)
    for similar_text in most_similar_texts:
        print(similar_text[0])

if __name__ == '__main__':
    print("file name:")
    file_name = input()
    file_path = DOC_PATH.format(file_name)
    doc = read_document(file_path)
    sentences = split_into_words(doc)
    print()
    search_similar_texts(sentences)



