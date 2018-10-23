import sys
import os
import comtypes.client
# python 3.6   安装依赖  pip install comtypes
def d2p(doc_name,pdf_name):
    in_file=doc_name
    out_file=pdf_name
    # create COM object
    word=comtypes.client.CreateObject('Word.Application')
    doc=word.Documents.Open(in_file)
    # 需要注意的是，这里的FileFormat为17，就对应着是wdFormatpdf
    doc.SaveAs(out_file,FileFormat=17)
    doc.Close()
    word.Quit()
#获取文件夹
file_path="C:/Users/office/Desktop/"
# 读取所有文件目录
file_list=os.listdir(file_path)
for word_path in file_list:
    doc_name=file_path+word_path
    pdf_name=file_path+word_path.split(".")[0]+".pdf"

    print(doc_name)
    print(pdf_name)
    # 外加文档判断条件
    # 判断文档名是不是以C开头
    if word_path[0]!="C":
        continue
    else:
        d2p(doc_name,pdf_name)
