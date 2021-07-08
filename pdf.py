# -*- coding: utf-8 -*-
import requests
import re

def getFilename_fromCd(cd):
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]
def read_2():
    import slate3k as slate

    with open('1.pdf', 'rb') as f:
        doc = slate.PDF(f)
    for i in range(len(doc)):
        print(re.sub(r'\n\n', ' ', doc[i]))
    # print(doc)
# def read_pdf():
#
# # importing required modules
#     import PyPDF2
#
#     # creating a pdf file object
#     pdfFileObj = open('1.pdf', 'rb')
#
#     # creating a pdf reader object
#     pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#     print(pdfReader.isEncrypted)
#     # printing number of pages in pdf file
#     print(pdfReader.numPages)
#     # creating a page object
#
#     for i in range(0,pdfReader.numPages):
#         pageObj = pdfReader.getPage(i)
#     # extracting text from page
#         print(pageObj.extractText())
#
#     # closing the pdf file object
#     pdfFileObj.close()
read_2()
#
# url = 'https://egrul.nalog.ru/vyp-download/246C2E2C5E7E3BB382AD39C327F35B811A65B9726BE76CADF484DEB58384F227B9B554EE246E1ECAA6B655FA66794985BCB16BAC738F60D37445805AFCA321BD'
# r = requests.get(url, allow_redirects=True)
# filename = getFilename_fromCd(r.headers.get('content-disposition'))
# open(filename, 'wb').write(r.content)