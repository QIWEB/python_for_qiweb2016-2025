# coding: gbk
filename = 'ssr.txt' # txt�ļ��͵�ǰ�ű���ͬһĿ¼�£����Բ���д����·��
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
