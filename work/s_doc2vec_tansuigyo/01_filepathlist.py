import os

path = '../wikipwdia/test2/'
files = []

f = open('01_filepathlist.txt', mode='w' , encoding='utf-8')
files = os.listdir(path)

for file in files:
    f.writelines(path + file + "\n")

f.close
