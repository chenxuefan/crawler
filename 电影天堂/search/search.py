'''
@author: 人人都爱小雀斑
@time: 2020/2/26 13:15
@desc:
'''
import time,progressbar
import urllib.parse
import requests,threading
from bs4 import BeautifulSoup
def spider1(name):#阳光电影
    name_parse=urllib.parse.quote(name,encoding="gbk")#转换编码，加密
    # print(time.process_time())
    #https://www.dy2018.com/e/search/result/?searchid=96978
    url="http://s.ygdy8.com/plus/so1.php?typeid=1&keyword="+name_parse
    r=requests.get(url)
    r.encoding="gbk"
    root=BeautifulSoup(r.text,"lxml")
    tables=root.find("div",attrs={"class":"co_content8"}).find_all("table")#
    if tables==[]:print("抱歉，暫時無此電影。")
    for t in tables:
        name=t.find("a").text
        href="http://s.ygdy8.com"+t.find("a")["href"]
        print(name,href)
def spider2(name):#电影天堂
    name_parse=urllib.parse.quote(name,encoding="gbk")#转换编码，加密
    # print(time.process_time())
    #https://www.dy2018.com/e/search/result/?searchid=96978
    url="https://www.dy2018.com/e/search/result/?searchid=97255"
    r=requests.get(url)
    r.encoding="gbk"
    root=BeautifulSoup(r.text,"lxml")
    tables=root.find("div",attrs={"class":"co_content8"}).find_all("table")#
    if tables==[]:print("抱歉，暫時無此電影。")
    for t in tables:
        name=t.find("a").text
        href="http://s.ygdy8.com"+t.find("a")["href"]
        print(name,href)
def gui_tk():
    import tkinter as tk
    window = tk.Tk()
    window.title('@author billie')
    # 标签
    tk.Label(window, cnf={'text': '请输入电影名称：'}).pack(side=tk.LEFT,padx=0,pady=0)
    # 输入框
    input = tk.Entry(window)
    input.pack(side=tk.LEFT,padx=10,pady=0)
    # 按钮
    tk.Button(window, cnf={'text': '查询', 'command': lambda: spider1(input.get())}).pack(side=tk.LEFT,padx=20,pady=0)
    window.mainloop()
while True:
    # name=input("请输入电影名称：")#"神奇"#
    # name="速度"
    # b=time.time()
    # # spider1(name)
    # e=time.time()
    # print(divmod(round(e-b),60))

    gui_tk()
