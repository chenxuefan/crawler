# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/12/28 2:49 下午
@Describe
目标网站 - https://flightaware.com/
数据分类 - 广州 深圳 珠海 香港 澳门 / 上海 南京 无锡 常州 苏州
数据特征 - 标识符 机型 始发地 出发 到达
"""
import requests,asyncio,aiohttp
from pyquery import PyQuery as pq
import lxml
import threading
import re
import pandas as pd
import csv
import logging

# 设置日志格式
logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


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
        self.df = pd.DataFrame(columns=['标识符', '机型', '始发地', '出发', '到达'])

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
        except:pass



    # 异步HTTP请求
    async def fetch(self,sem,session,url):
        async with sem:
            async with session.get(url=url,verify_ssl=False) as response:
                return await response.text()

    # 解析网页
    async def parser(self,html):


        doc = pq(html)
        trs = doc('.prettyTable').find('tr').items()

        data = []
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
        for i in data:
            self.df.loc[self.df.shape[0] + 1] = i

        self.data += data
        self.page += 1
        self.count += len(data)

        if data != []:print(f"「{self.city}」合计「{self.count}」条 - 第{self.page}页：{data}")


        # if data == []:
        #     print(f'「{self.city}」已结束数据爬取')

        try:
            f = csv.reader(open(f'./tables/{self.city}.csv', 'r'))
            self.dataBase = [i[1:] for i in f]
            for i in data:
                if i not in self.dataBase:
                    self.dataBase.append(i)
                    CONTINUE = True
                    # print(f'「{self.city}」已结束数据爬取')
                elif i in self.dataBase:
                    self.data = self.dataBase
                    CONTINUE = False
        except Exception as err:
            print(err)

    # 处理网页
    async def download(self,sem,url):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                html = await self.fetch(sem,session,url)
                await self.parser(html)
            except Exception as err:
                print(err)


    def mainWork(self):
        if type(self.cityCode) == str:  # 这个城市只有一个机场，只爬一次
            urls = [self.baseUrl.format(self.cityCode,i) for i in range(0,100000,20)]
        elif type(self.cityCode) == list:
            urls = []
            for code in self.cityCode:  # 这个城市有多个机场，爬多几次
                urls += [self.baseUrl.format(code,i) for i in range(0,100000,20)]

        # 利用asyncio模块进行异步IO处理

        sem = asyncio.Semaphore(100)
        tasks = [asyncio.ensure_future(self.download(sem,url)) for url in urls]
        # tasks = asyncio.gather(*tasks)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

        self.df.to_csv(f'./tables/{self.city}.csv')


bi = Flight('北京')
bi.mainWork()


