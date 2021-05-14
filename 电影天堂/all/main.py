'''
@author: 人人都爱小雀斑
@time: 2020/2/25 16:57
@desc:爬取电影天堂全站电影资源链接并保存至csv文件
'''
import urllib

import requests
import urllib.request as ur
from bs4 import BeautifulSoup
import csv
import threading
class MovieHeven():
    def __init__(self):
        # self.base_url="https://www.dytt8.net/html/gndy/dyzz/index.html"
        self.base_url = "https://www.dy2018.com/html/gndy/jddy/"
        self.page=1
        self.No=1
        self.fobj=open("movies.csv", "wt", encoding="utf-8", newline='')

    def spider(self,url):#
        try:
            print("正在爬取第{}页...".format(self.page))
            # time.sleep(1)
            #获取网页链接并读取
            if self.page==1:url=self.base_url#如为第一页
            # gethtml=lambda: requests.get(url)#匿名函数
            # e=threading.Thread(target=gethtml).start()#多线程发送请求
            # html=gethtml()
            html=requests.get(url)
            html.encoding="gb2312"
            html=html.text
            # print(html)
            #beautfulSoup装载文档
            root=BeautifulSoup(html,"lxml")
            #查找所需元素，获取tables列表
            tables=root.find("div",attrs={"class":"co_content8"}).find("ul").find_all("table")
            for table in tables:
                name = table.find("a").text
                href = "http://www.dy2018.com"+table.find("a")["href"]
                # 文件写入操作
                writer = csv.writer(self.fobj)
                writer.writerow([name, href])
                print("No:", self.No, name, href)
                self.No += 1

            #爬取下一页
            self.page+=1
            url=self.base_url+"index_{}.html".format(self.page)
            print(url)
            self.spider(url)

#https://www.dy2018.com/i/99415.html
        except:#没有下一页
            print("finished")
        # except Exception as err:
        #     print(err)
    def main(self):
    ##    threading.Thread(target=spiderA(url)).start()
        import time
        begin_time = time.time()
        self.spider(url="")  # 执行主程序
        self.fobj.close()
        end_time = time.time()
        time = end_time - begin_time
        m, s = divmod(round(time), 60)
        print("用时：{}min{}s".format(m, s))

if __name__ == '__main__':
    billie=MovieHeven()
    billie.main()
