# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2021/5/30 5:10 下午
@Describe 
"""
from selenium import webdriver
import requests
import asyncio
import aiohttp

# import http.client
# http.client._MAXLINE = 655360

import urllib.parse
import time,os


class Config:
    base_URL  = 'https://www.huodongxing.com/events'
    cookie_PATH = './login_cookies.txt'

class Huodongxing:
    def __init__(self):
        self.base_url = Config.base_URL
        self.page_count = 200
        self.page = 0

    def _page(self) -> int:
        if self.page < self.page_count:
            self.page += 1
            return self.page

    def login_and_get_cookies(self):
        driver = webdriver.Chrome()
        driver.get(Config.base_URL)
        """手动验证并登录"""
        time.sleep(30)
        with open(Config.cookie_PATH,'w') as f: f.write(str(driver.get_cookies()))
        driver.close()


    def _cookie(self,key:str) -> str:
        cookies = eval(open(Config.cookie_PATH, 'r').read())
        for cookie in cookies:
            return cookie['value'] if cookie['name'] == key else ''

    def requests_request(self) -> str:

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "",
            "Cookie":f"route={self._cookie('route')};ASP.NET_SessionId={self._cookie('ASP.NET_SessionId')};HDX_REGION={self._cookie('HDX_REGION')};_ga={self._cookie('_ga')};Hm_lvt_d89d7d47b4b1b8ff993b37eafb0b49bd={round(time.time())}; AccupassWeb={self._cookie('AccupassWeb')}; Hm_lpvt_d89d7d47b4b1b8ff993b37eafb0b49bd={round(time.time())}",
            "Host": "www.huodongxing.com",
            "Referer": "https://www.huodongxing.com/channel?c=%E4%BA%B2%E5%AD%90",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        }

        s = requests.session()
        # s.max_redirects = 60
        r = s.get(
            url=self.base_url,
            headers=headers,
            params={'page': self._page()}
        )
        r.encoding = 'utf-8'
        return r.status_code, r.text.__len__(),self.page

    async def get(self,url):

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "",
            "Cookie": f"route={self._cookie('route')};ASP.NET_SessionId={self._cookie('ASP.NET_SessionId')};HDX_REGION={self._cookie('HDX_REGION')};_ga={self._cookie('_ga')};Hm_lvt_d89d7d47b4b1b8ff993b37eafb0b49bd={round(time.time())}; AccupassWeb={self._cookie('AccupassWeb')}; Hm_lpvt_d89d7d47b4b1b8ff993b37eafb0b49bd={round(time.time())}",
            "Host": "www.huodongxing.com",
            "Referer": "https://www.huodongxing.com/channel?c=%E4%BA%B2%E5%AD%90",
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        }

        # s = aiohttp.ClientSession()
        conn = aiohttp.TCPConnector(verify_ssl=False)  # 防止ssl报错

        async with aiohttp.request("GET",url=url,connector=conn,headers=headers) as r:
            return await r.text()

    async def aiohttp_request(self,url):
        r = await self.get(url)
        print(r.__len__(),url)
        # return r.status_code, r.text.__len__(),self.page

    def main(self):
        # self.login_and_get_cookies()
        # for _ in range(self.page_count):
        #     # time.sleep(1)
        #     print(self.request())

        tasks = [asyncio.ensure_future(self.aiohttp_request(f"https://www.huodongxing.com/events?page={i}")) for i in range(1, 201)]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    Huodongxing().main()

