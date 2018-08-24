import os
import sys

def splitFile(arg):

    cf = open('categoryes.txt', mode='r' , encoding='utf-8')

    ides = []
    titles = []
    categoryes = []

    for line in cf.readlines():
    
        spl = line.split(',')
        
        ides.append(spl[0])
        titles.append(spl[1])
        categoryes.append(spl[2])
    
    f = open('corpus.txt', mode='r' , encoding='utf-8')
    
    oCnt = 0
    
    while True:
    
        page_str = get_page(f)
        
        if not page_str:
            f.close
            cf.close
            break
        
        spl2 = page_str.split('\n')
        
        for line in spl2:
        
            if line[0:4] == '<doc':
                
                tempStr = line.replace('<doc ','')
                tempStr = tempStr.replace('>','')
                tempStr = tempStr.replace('\"','')
                
                spl3 = tempStr.split(' ')
                
                dict = get_Coumn(spl3)
        
                id = dict['id']
                wkTitle = dict['title']
                wkTitle = wkTitle.replace('\\','')
                wkTitle = wkTitle.replace('/','')
                wkTitle = wkTitle.replace('|','')
                wkTitle = wkTitle.replace('$','')
                wkTitle = wkTitle.replace('&','')
                
                title = wkTitle
                
                idx = ides.index(id)
                category = categoryes[idx]
                
                if category.find(arg) != -1:
                    w = open('test2/' + title + '.txt', mode='w' , encoding='utf-8')
                
            elif line[0:6] == '</doc>':
                if category.find(arg) != -1:
                    w.close
                    print(title)
                    oCnt = oCnt + 1

            else:               
                if category.find(arg) != -1:
                    wline = line.replace('\n','')
                    wline = wline.replace('\r','')
                    
                    if len(wline) > 0 :
                    
                        w.writelines(wline + '\n')
        
        if oCnt > 1000:
            break
        
        

def get_Coumn(split_Str):
    
    dict = {}
    
    for spl in split_Str:
        
        idx = 0
        colName = ''
        colFlg = True
        valName = ''
        valFlg = False
        
        while idx < len(spl):
            
            if spl[idx] == "=":
                colFlg = False
                valFlg = True
            else:
                if colFlg:
                    colName = colName + spl[idx]
                if valFlg:
                    valName = valName + spl[idx]
            
            idx = idx + 1
        
        dict[colName] = valName
    
    return dict
    
    

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
        line = wiki_file.readline()
        if line == '':
            # readline()が空文字を返したら終了
            return False
        if line.find('<doc') != -1:
            page_started = True
            page_lines.append(line)

    while not page_ended:
        line = wiki_file.readline()
        if line.find('</doc>') != -1:
            page_ended = True
        page_lines.append(line)

    return '\n'.join(page_lines)

if __name__ == '__main__':
    # コマンドライン引数をパース
    args = sys.argv
    if len(args) == 2 :
        arg = args[1]
        splitFile(arg)
    else:
        print('commandError')


