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
    Log_path = 'unsplash.log'


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
async def parse(text: str):
    ids = re.findall('<a itemProp="contentUrl"(.*?)href="(.*?)">', text)
    ids = [i[-1].split('/')[-1] for i in ids]
    id = random.choice(ids)
    # url = Config.download_url.format(id)
    urls = [Config.download_url.format(id) for id in ids]
    return urls


@log
async def download(type: str, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, verify_ssl=False) as resp:
            # logging.info(resp.content_disposition)
            filename = dict(resp.headers)['Content-Disposition']
            filename = re.search(r'filename="(.*?)"', filename).group(1)
            content = await resp.read()
            path = os.path.join(os.getcwd(), f'./images/{type}/')
            if not os.path.exists(path):
                os.makedirs(path)
            with open(os.path.join(path, filename), 'wb') as f:
                f.write(content)
            # with open(os.path.join(path, 'main.jpg'), 'wb') as f:
            #     f.write(content)
            logging.info(f'已下载 - {type}/{filename}')


async def process(type: str, url: str):
    return await download(type, url)


@log
async def main():
    topics = await get_topics()

    tasks = []
    for type, url in topics.items():
        dl_url = await parse(await fetch(url))
        if isinstance(dl_url, list):
            task = [asyncio.create_task(process(type, url)) for url in dl_url]
            tasks += task
        elif isinstance(dl_url, str):
            task = asyncio.create_task(process(type, url))
            tasks.append(task)
    print(tasks.__len__())
    # await asyncio.wait(tasks)
    # return tasks


def run():
    start = time.time()

    # 方法1 - asyncio.run() (python3.7)
    done, pending = asyncio.run(main())

    # 方法2 - loop.run_until_complete()
    # loop = asyncio.get_event_loop()
    # tasks = loop.run_until_complete(main())
    # done, pending = loop.run_until_complete(asyncio.wait(tasks))

    end = time.time()
    logging.info(f'共耗时 - {end - start} s')


if __name__ == '__main__':
    run()
