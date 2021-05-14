# -*- coding: utf-8 -*-
'''
@Author billie
@Date 2020/3/17 13:50
@Describe 

'''
import requests,time,datetime,threading,re
from lxml import etree
from progressbar import *
def spider():
    count=1
    date=datetime.date(2020,1,21)
    while count:
        print(date)
        if int(date.strftime("%Y%m%d"))<=20200205:pdfinfo=str(date.strftime("%Y%m%d"))+'-sitrep-'+str(count)+'-2019-ncov.pdf'
        else:pdfinfo=str(date.strftime("%Y%m%d"))+'-sitrep-'+str(count)+'-covid-19.pdf'
        url="https://www.who.int/docs/default-source/coronaviruse/situation-reports/{}".format(pdfinfo)
        print(url)
        re=requests.get(url)
        with open("situation-reports/"+pdfinfo,"wb")as f:
            f.write(re.content)
        print(re.content)
        date = date + datetime.timedelta(days=1)
        count+=1

def DL(url,pdfname):
    r = requests.get(url)
    r.encoding='utf-8'
    with open("situation-reports//" + pdfname + ".pdf", "wb")as f:
        f.write(r.content)
    print(pdfname)
def spider2():
    from bs4 import BeautifulSoup
    url = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"
    r=requests.get(url,headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'})
    # boot=BeautifulSoup(r.text,"lxml")
    # ps=boot.find("div",attrs={'id':'PageContent_C006_Col01'}).find_all("p")
    tree=etree.HTML(r.text)
    hrefs=tree.xpath('//*[@id="PageContent_C006_Col01"]/div[1]/div/p/descendant::a/@href')
    print(len(hrefs))#//*[@id="PageContent_C006_Col01"]/div[1]/div/p[1]/strong/a
    for href in hrefs[:-3]:#:[:1]bar(
        # print(href)
        url='https://www.who.int'+href
        # print(url)
        pdfname=re.search("situation-reports/(.*).pdf",url).group(1)
        # threading.Thread(target=DL,args=[url,pdfname]).start()#多线程下载
        DL(url,pdfname)

spider2()
