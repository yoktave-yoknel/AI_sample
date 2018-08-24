#!/usr/bin/python
# -*- coding: utf-8 -*-

# Wikipediaから記事をパースする
# 2015/03/01のWikipediaの記事数(日本語版):949,220

import argparse
import bz2
import xml.etree.ElementTree as ET


def get_page(wiki_file):
    '''ファイルから<page>〜</page>の文字列を取り出す

    Wikipediaのページの形式
    <page>
        <title>記事のタイトル</title>
        ...
    </page>
    '''
    page_lines = []
    page_started, page_ended = False, False

    while not page_started:
        line = wiki_file.readline().decode()
        if line == '':
            # readline()が空文字を返したら終了
            return False
        if line.find('<page>') != -1:
            page_started = True
            page_lines.append(line)

    while not page_ended:
        line = wiki_file.readline().decode()
        if line.find('</page>') != -1:
            page_ended = True
        page_lines.append(line)

    return '\n'.join(page_lines)


def parse_wiki(input_path):
    '''Wikipediaの圧縮ファイルをパースする'''
    # bz2形式の圧縮ファイルをオープン
    wiki_file = bz2.BZ2File(input_path)
    
    outFile = open('categoryes.txt', mode='w' , encoding='utf-8')
    
    while True:
        # ページ単位でXML形式の文字列取得
        page_str = get_page(wiki_file)
        if not page_str:
            outFile.close
            break

        # XMLをパースする
        root = ET.fromstring(page_str)

        # 例えば記事のタイトルを取得する場合
        # <title>記事のタイトル</title>
        title = root.find('title').text
        id = root.find('id').text
        
        if title.find('Wikipedia:') == -1:

            for rev in root.findall('revision'):
            
                Categoryes = []
                
                text = rev.find('text').text
                
                if text is not None :
                    spl = text.split('\n')
            
                    for line in spl:
                
                        if line.find('[[Category:') != -1:
                    
                            idx = 11
                    
                            ch = ''
                                           
                            while idx < len(line):
                        
                                if line[idx] == ']':
                                    break
                                ch = ch + line[idx]
                        
                                idx = idx + 1
                        
                            Categoryes.append(ch)
            
                    writeLine = id + ',' + title + ',' + '$'.join(Categoryes) + '\n'
                    outFile.writelines(writeLine)
            


if __name__ == '__main__':
    # コマンドライン引数をパース
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_path',
        help=u'Wikipediaの記事の圧縮ファイルのパス (例:jawiki-YYYYMMDD-pages-articles.xml.bz2'
    )
    args = parser.parse_args()
    # ファイルを読みだして記事ごとにパース
    parse_wiki(args.input_path)