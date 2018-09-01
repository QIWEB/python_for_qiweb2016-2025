# coding: gbk
filename = 'ssr.txt' # txt文件和当前脚本在同一目录下，所以不用写具体路径
pos = []
Efield = []
str =""
with open(filename, 'r',encoding='gb18030',errors='ignore') as file_to_read:
    while True:
        lines=file_to_read.readline()
        if not lines:
            break
        if 'ssr:' in lines:
            str+=lines+"\n"


print(str)
