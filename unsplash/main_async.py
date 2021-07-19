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
async def parse(type: str, text: str):
    ids = re.findall('<a itemProp="contentUrl"(.*?)href="(.*?)">', text)
    ids = [i[-1].split('/')[-1] for i in ids]
    id = random.choice(ids)
    url = [Config.download_url.format(id)]
    urls = [Config.download_url.format(id) for id in ids]
    return {type : url}


@log
async def download(type: str, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, verify_ssl=False) as resp:
            content_length = resp.headers['Content-Length']
            filesize = int(content_length) / 1024 / 1024
            filename = dict(resp.headers)['Content-Disposition']
            filename = re.search(r'filename="(.*?)"', filename).group(1)
            content = await resp.read()
            path = os.path.join(os.getcwd(), f'./images/{type}/')

            if not os.path.exists(path):
                os.makedirs(path)
            # with open(os.path.join(path, filename), 'wb') as f:
            #     f.write(content)
            with open(os.path.join(path, 'main.jpg'), 'wb') as f:
                f.write(content)
            logging.info(f'已下载 - {type}/{filename} {filesize:.2f} MB')


async def dl_process(type: str, url: str):
    return await download(type, url)

async def url_process(type: str, url: str):
    return await parse(type, await fetch(url))

@log
async def main():
    topics = await get_topics()

    tasks_type = []
    for type, url in topics.items():
        task = asyncio.create_task(url_process(type, url))
        tasks_type.append(task)
    print(len(tasks_type))
    done, pending = await asyncio.wait(tasks_type)

    dl_url_dic = {}  # 待下载的图片文件资源链接
    for task in done:
        type, dl_url = list(task.result().items())[0]
        dl_url_dic[type] = []
        if isinstance(dl_url, list):
            dl_url_dic[type] += dl_url
        elif isinstance(dl_url, str):
            dl_url_dic[type].append(dl_url)

    tasks_dl = []
    for type, dl_url in dl_url_dic.items():
        if isinstance(dl_url, list):
            task = [asyncio.create_task(dl_process(type, url)) for url in dl_url]
            tasks_dl += task
        elif isinstance(dl_url, str):
            task = asyncio.create_task(dl_process(type, dl_url))
            tasks_dl.append(task)

    print(len(tasks_dl))
    done, pending = await asyncio.wait(tasks_dl)
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
