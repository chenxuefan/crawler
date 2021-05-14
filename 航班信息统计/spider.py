# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/12/28 2:49 下午
@Describe
目标网站 - https://flightaware.com/
数据分类 - 广州 深圳 珠海 香港 澳门 / 上海 南京 无锡 常州 苏州
数据特征 - 标识符 机型 始发地 出发 到达
"""
import requests,asyncio
from pyquery import PyQuery as pq
import lxml
import threading
import re
import pandas as pd
import csv

class Flight():
    def __init__(self,city):
        self.baseUrl = 'https://flightaware.com/live/airport/{}/arrivals?;offset={};order=actualarrivaltime;sort=DESC'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        self.session = requests.session()
        self.page = 0
        self.count = 0
        self.data = []
        self.city = city
        self.cityCode = self.getAirportCode(city=city)

    def getAirportCode(self,city):# 获取对应城市的机场代码
        url = f'https://airportcode.51240.com/{city}__airportcodesou/'
        try:
            r = requests.get(url = url,headers = self.headers)
            doc = pq(r.text)
            msglist = doc('td').text().split(' ')[0].split('\n')[5:]
            print(msglist)

            if len(msglist) == 5: # 只有一个机场
                treeCode = msglist[1]
                fourCode = msglist[2]
                return fourCode # 返回机场代码
            elif len(msglist) > 5: # 有多个机场
                fourCodeList = []
                for i in msglist:
                    if len(i) == 4:
                        for en in i: contain_en = bool(re.search('[a-zA-Z]', en)) # 判断是否有英文字符
                        if contain_en: fourCodeList.append(i)# true，则为正确的四字代码
                return fourCodeList # 返回机场代码列表

        except Exception  as e:print(e)

    def login(self):
        loginUrl = 'https://flightaware.com/account/session'
        r = self.session.get(url=loginUrl,headers=self.headers)
        token = re.search("<input type='hidden' name='token' value='(.*?)'>", r.text).group(1)
        self.session.post(
            url=loginUrl,
            headers=self.headers,
            data={'flightaware_username': 'BillieChan',
                  'flightaware_password': 'a1222222222',
                  'token': token}
        )

    def spider(self,code):

        data = []

        r = self.session.get(
            url=self.baseUrl.format(code,self.count)
        )
        r.encoding = 'utf-8'

        doc = pq(r.text)
        trs = doc('.prettyTable').find('tr').items()

        for tr in trs:
            try:
                l = tr.text().split('\n')
                Ident = l[0]
                Type = l[1]
                Origin = l[2]
                Departure = l[3]
                Arrival = l[4]
                data.append([Ident,Type,Origin,Departure,Arrival])
            except: pass
        data = data[2:]

        self.data += data
        self.page += 1
        self.count += len(data)

        print(f"「{self.city}」合计「{self.count}」条 - 第{self.page}页：{data}")

        # 下一页
        CONTINUE = True

        if data == []:
            CONTINUE = False
            print(f'「{self.city}」已结束数据爬取')

        # try:
        #     f = csv.reader(open(f'./tables/{self.city}.csv', 'r'))
        #     self.dataBase = [i[1:] for i in f]
        #     for i in data:
        #         if i not in self.dataBase:
        #             self.dataBase.append(i)
        #             CONTINUE = True
        #             # print(f'「{self.city}」已结束数据爬取')
        #         elif i in self.dataBase:
        #             self.data = self.dataBase
        #             CONTINUE = False
        # except Exception as err:
        #     print(err)

        if CONTINUE:
            # threading.Thread(target=self.spider,args=(code,)).start()
            self.spider(code=code)
    def mainWork(self):
        self.login() # 登录
        try: # 开爬
            if type(self.cityCode) == str: # 这个城市只有一个机场，只爬一次
                self.spider(self.cityCode)
            elif type(self.cityCode) == list:
                for code in self.cityCode: # 这个城市有多个机场，爬多几次
                    self.spider(code=code)

            columns = ['标识符', '机型', '始发地', '出发', '到达']
            df = pd.DataFrame(columns=columns, data=self.data)
            df.to_csv(f'./tables/{self.city}.csv', encoding='utf-8')
        except: # 出错啦！
            print(f"第「{self.page}」页出错了")
        finally: # 保存数据至本地
            pass

b = Flight('苏州')
b.mainWork()

