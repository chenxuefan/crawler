import re
import threading
# from __future__ import unicode_literals
from wxpy import *
import datetime
import time
from bs4 import BeautifulSoup
from lxml import etree
import urllib.request as ur
import requests
import csv
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import numpy as np
import pandas as pd
import threading

class Weather():
    def __init__(self):
        self.city=""
        self.url="http://www.weather.com.cn"
        self.dataDic = dict()  # 存储已存在的数据，键为日期，值为每一天的天气数据
        self.currentDataList = []  # 存储当前数据
    def spider(self):#selenium方法
        # 无窗口弹出操作
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = selenium.webdriver.Firefox()#options=options
        driver.get(self.url)
        driver.find_element_by_css_selector("input[class='textinput text']").send_keys(self.city)#搜索框#输入城市名
        driver.find_element_by_css_selector("input[class='btn ss']").click()#确定按钮#回车
        time.sleep(2)
        n = driver.window_handles  # 获取当前页所有窗口句柄
        driver.switch_to.window(n[1])  # 切换到第二个窗口
        driver.find_element_by_xpath('//*[@id="someDayNav"]/li[2]/a').click()#跳转到“七天”页面
        time.sleep(2)
        lis =driver.find_elements_by_css_selector('ul[class="t clearfix"] li')
        #获取接下来七天的天气情况
        print(self.city+"接下来七天的天气:\n")
        for li in lis:
            # 月份+\+日
            date = time.strftime("%m").strip("0") \
                   + "\\" \
                   + re.search("\d+",li.find_element_by_tag_name("h1").text).group()
            wea=li.find_element_by_css_selector('p[class="wea"]').text
            tem=li.find_element_by_css_selector('p[class="tem"]').text.strip("\n")
            win=li.find_element_by_css_selector('p[class="win"]').text
            self.currentDataList.append([date,wea,tem,win])
            print(date,wea,tem,win)
    def spider2(self):#requests方法
        #查找对应城市的城市代码
        code_list = list(csv.reader(open("./城市代码.csv",'r',encoding='utf-8')))  # 创建csv读取对象,返回数组
        code_dic=dict()
        for i in code_list: code_dic[i[0]] = i[1]  # 创建键值对，i类型为list:['city','code']
        code=code_dic[self.city]#根据城市中文名称，查找对应城市的城市代码
        self.url = "http://www.weather.com.cn/weather/{}.shtml".format(code)
        r = requests.get(self.url,
                         headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'})
        r.encoding = "utf-8"
        # 获取接下来七天的天气情况
        print(self.city + "接下来七天的天气:\n")
        root = BeautifulSoup(r.text, "lxml")
        lis = root.find("ul", attrs={'class': 't clearfix'}).find_all("li")
        for li in lis:
            #月份+\+日
            date = time.strftime("%m").strip("0")\
                   +"\\"\
                   +re.search("\d+",li.find("h1").text).group()
            wea = li.find('p',attrs={'class':"wea"}).text
            tem = li.find('p',attrs={'class':"tem"}).text.strip("\n")
            win = li.find('p',attrs={'class':"win"}).text.strip("\n")
            self.currentDataList.append([date, wea, tem, win])
            print(date, wea, tem,win)
    def save_to_csv(self):# 文件写入操作
        #读取本地的天气文件
        try:#如已存在文件，读取
            open("{}天气.csv".format(self.city), "r")#如打开成功，则文件已存在
            base_data = list(csv.reader(open("{}天气.csv".format(self.city))))  # 创建csv读取对象,返回数组
            for i in base_data[1:]:
                self.dataDic[i[0]] = i  # 创建键值对，i类型为list
        except:pass#不存在文件，则跳过
        finally:#创建写入的数据dataDic
            for i in range(7):
                if self.currentDataList[i][0] not in self.dataDic:  # 如不存在此日的天气数据，创建新的键值对
                    self.dataDic[self.currentDataList[i][0]] = self.currentDataList[i]
                elif self.currentDataList[i][0] in self.dataDic:  # 如存在此日的天气数据，用新数据替换值
                    if len(self.currentDataList[i][2]) > 5:
                        self.dataDic[self.currentDataList[i][0]] = self.currentDataList[i]
        #写入新的文件
        with open("./tables/{}天气.csv".format(self.city), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["日期", "天气", "温度", "风向"])
            for i in self.dataDic.values():
                writer.writerow(i)  # 写入天气数据
    def main(self):
        print('@author：人人都爱小雀斑')
        while True:
            try:
                self.city=input("\n>>>请输入您所在的城市：")
        ##        self.city="深圳"
                self.spider2()
                # self.spider()
                self.save_to_csv()
            #except:print("抱歉，无法获取{}的信息".format(self.city))
            except Exception as err:print(err)
if __name__ == "__main__":
    billie=Weather()
    billie.main()
    time.sleep(10)

    
