# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 08:36:54 2019

@author: billie
"""
from bs4 import BeautifulSoup
import urllib.request
import time
import random
import threading
# 全局取消证书验证
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#获取网页文件
def getHtml(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
    req = urllib.request.Request(url=url, headers=headers)  
    data=urllib.request.urlopen(req).read()  
    return data.decode()
def download(count,name,src):
    try:
        time.sleep(2)
        resp=urllib.request.urlopen(src)
        data=resp.read()
        f=open("images\\"+name+".jpg","wb")
        f.write(data)
        f.close()
        print(count,"downloaded",name)
    except Exception as err:
        print(err,"failed",name)
def spider(url):
    global page,count
    page+=1
    print("Page",page)
    url=url
    html=getHtml(url)
    root=BeautifulSoup(html,"lxml")#使用BeautifulSoup装载HTML文档
    lis=root.find("ol",attrs={"class":"grid_view"}).find_all("li")


    for li in lis:
        #电影封面图片tag
        img=li.find("div",attrs={"class":"pic"}).find("img")
        #电影封面图片链接
        src=urllib.request.urljoin(url,img["src"])
        #电影名字
        name=li.find("div",attrs={"class":"info"}).find("div",attrs={"class":"hd"}).find("a").find("span").text
        #多线程下载
        count += 1
        T=threading.Thread(target=download,args=[count,name,src])
        T.start()
        #单线程下载
        # download(count,name,src)
    #找到下一页tag的链接
    link=root.find("div",attrs={"class":"paginator"}).find("span",attrs={"class":"next"}).find("a")
    #如果有下一页
    if link:
        href=link["href"]
        url=urllib.request.urljoin(url,href)#获取下一页的url
        spider(url)


def main():
    global page,count
    url="https://movie.douban.com/top250" 
    page=0
    count = 0
    spider(url)

if __name__=="__main__":
    main()
    process_time=time.process_time()
    t=round(process_time)
    m,s=divmod(t,60)

    print("花费时间：{}:{}".format(m,s))