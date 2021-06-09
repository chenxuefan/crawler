# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/12/31 3:12 上午
@Describe 
"""
import re
import time
import aiohttp
import asyncio
import pandas as pd
import logging

# 设置日志格式
logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

df = pd.DataFrame(columns=['name', 'bank', 'currency', 'startDate',\
                           'endDate', 'period', 'proType', 'profit', 'amount'])

# 异步HTTP请求
async def fetch(sem, session, url):
    async with sem:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
        async with session.get(url, headers=headers, verify_ssl = False) as response:
            return await response.text()

# 解析网页
async def parser(html):
    # 利用正则表达式解析网页
    tbody = re.findall(r"<tbody>[\s\S]*?</tbody>", html)[0]
    trs = re.findall(r"<tr [\s\S]*?</tr>", tbody)
    for tr in trs:
        tds = re.findall(r"<td[\s\S]*?</td>", tr)
        name,bank = re.findall(r'title="(.+?)"', ''.join(tds))
        name = name.replace('&amp;', '').replace('quot;', '')
        currency, startDate, endDate, amount = re.findall(r'<td>(.+?)</td>', ''.join(tds))
        period = ''.join(re.findall(r'<td class="td7">(.+?)</td>', tds[5]))
        proType = ''.join(re.findall(r'<td class="td7">(.+?)</td>', tds[6]))
        profit = ''.join(re.findall(r'<td class="td8">(.+?)</td>', tds[7]))
        df.loc[df.shape[0] + 1] = [name, bank, currency, startDate, endDate, \
                                   period, proType, profit, amount]

    logger.info(str(df.shape[0])+'\t'+name)

# 处理网页
async def download(sem, url):
    async with aiohttp.ClientSession() as session:
        try:
            html = await fetch(sem, session, url)
            await parser(html)
        except Exception as err:
            print(err)

# 全部网页
urls = ["https://www.rong360.com/licai-bank/list/p%d"%i for i in range(1, 8641)]

# 统计该爬虫的消耗时间
print('*' * 50)
t3 = time.time()

# 利用asyncio模块进行异步IO处理
loop = asyncio.get_event_loop()
sem=asyncio.Semaphore(100)
tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
tasks = asyncio.gather(*tasks)
loop.run_until_complete(tasks)

df.to_csv('./rong360.csv')

t4 = time.time()
print('总共耗时：%s' % (t4 - t3))
print('*' * 50)

