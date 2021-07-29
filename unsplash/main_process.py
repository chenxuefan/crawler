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
import logging,os
import schedule
import time
from functools import wraps
from lxml import etree
import urllib.parse
import threading
import multiprocessing


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
    def wrapper(*args,**kwargs):
        try:
            # logging.info(f"正在执行 - {func.__name__}")
            return func(*args,**kwargs)
        except Exception as e:
            logging.error(repr(e)+'\n'+traceback.format_exc())
    return wrapper


#------------------------------------| main process |----------------------------------------


@log
def request(url:str) -> str:
    r = requests.get(url=url,
                     headers={
                         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
                     })
    return r.text

@log
def get_topics() -> dict:
    text = request(Config.topic_utl)
    eletree = etree.HTML(text)
    topics = eletree.xpath('//*[@class = "_2tgoq _2WvKc"]/text()')
    urls = eletree.xpath('//*[@class = "_2tgoq _2WvKc"]/@href')
    urls = [urllib.parse.urljoin(Config.base_url,url) for url in urls]
    return dict(zip(topics,urls))

@log
def parse(text:str) -> str:
    ids = re.findall('<a itemProp="contentUrl"(.*?)href="(.*?)">', text)
    ids = [i[-1].split('/')[-1] for i in ids]
    id = random.choice(ids)
    url = Config.download_url.format(id)
    return url

@log
def download(type:str,url:str):
    r = requests.get(url)
    filename = re.search('filename="(.*?)"',r.headers['Content-Disposition']).group(1)
    content = r.content
    path = os.path.join(os.getcwd(),f'images/{type}/')
    if not os.path.exists(path): os.mkdir(path)
    # with open(os.path.join(path,filename),'wb') as f:
    #     f.write(content)
    with open(os.path.join(path,'main.jpg'),'wb') as f:
        f.write(content)
    logging.info(f'已下载 - {type}/{filename}')

@log
def main():
    topics = get_topics()

    processes = []
    for type, url in topics.items():
        process = multiprocessing.Process(target=download, args=(type, parse(request(url), )))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f'共耗时 - {end-start} s')
    # schedule.every().day.at('00:00').do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

