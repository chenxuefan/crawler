# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2021/5/23 12:18 上午
@Describe
    - 爬取unsplash.com网站图片
"""
import requests
import re
import random
import traceback
import logging
import os
import schedule
import time
from functools import wraps
from lxml import etree
import urllib.parse
import asyncio
import aiohttp


class Config:
    base_url = 'https://unsplash.com/'
    topic_utl = 'https://unsplash.com/t'
    download_url = 'https://unsplash.com/photos/{}/download?force=true'
    Log_path = 'upslash.log'


# 日志初始化
logging.basicConfig(
    # filename=Config.Log_path,
    level=logging.INFO,
    format='%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # logging.info(f"正在执行 - {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(repr(e)+'\n'+traceback.format_exc())
    return wrapper


@log
async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        async with session.get(url, headers=headers, verify_ssl=False) as resp:
            return await resp.text()


@log
async def get_topics() -> dict:
    text = await fetch(Config.topic_utl)
    eletree = etree.HTML(text)
    topics = eletree.xpath('//*[@class = "_2tgoq _2WvKc"]/text()')
    urls = eletree.xpath('//*[@class = "_2tgoq _2WvKc"]/@href')
    urls = [urllib.parse.urljoin(Config.base_url, url) for url in urls]
    return dict(zip(topics, urls))


@log
async def parse(text: str) -> str:
    ids = re.findall('<a itemProp="contentUrl"(.*?)href="(.*?)">', text)
    ids = [i[-1].split('/')[-1] for i in ids]
    id = random.choice(ids)
    url = Config.download_url.format(id)
    return url


@log
async def download(type: str, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, verify_ssl=False) as resp:
            filename = dict(resp.headers)['Content-Disposition']
            filename = re.search(r'filename="(.*?)"', filename).group(1)
            content = await resp.read()
            path = os.path.join(os.getcwd(), f'images/{type}/')
            if not os.path.exists(path):
                os.mkdir(path)
            with open(os.path.join(path, filename), 'wb') as f:
                f.write(content)
            with open(os.path.join(path, 'main.jpg'), 'wb') as f:
                f.write(content)
                logging.info(f'已下载 - {type}/{filename}')


async def process(type: str, url: str):
    return await download(type, await parse(await fetch(url)))


@log
async def main():
    topics = await get_topics()

    tasks = []
    for type, url in topics.items():
        task = asyncio.ensure_future(process(type, url))
        tasks.append(task)

    return await asyncio.wait(tasks)


if __name__ == '__main__':
    done, pending = asyncio.run(main())
    pass
    # schedule.every().day.at('00:00').do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
