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

class Config:
    TYPE = {
        'Wallpapers':'https://unsplash.com/t/wallpapers',
        'Nature_url':'https://unsplash.com/t/nature',
        'People':'https://unsplash.com/t/people',
        'Architecture':'https://unsplash.com/t/architecture',
        'Current Events':'https://unsplash.com/t/current-events',
        'Business & Work':'https://unsplash.com/t/business-work',
        'Experimental':'https://unsplash.com/t/experimental',
        'Fashion':'https://unsplash.com/t/fashion',
        'Film':'https://unsplash.com/t/film',
        'Health & Wellness':'https://unsplash.com/t/health',
        'Interiors':'https://unsplash.com/t/interiors',
        'Street Photography':'https://unsplash.com/t/street-photography',
        'Technology':'https://unsplash.com/t/technology',
        'Travel':'https://unsplash.com/t/travel',
        'Textures & Patterns':'https://unsplash.com/t/textures-patterns',
        'Animals':'https://unsplash.com/t/animals',
        'Food & Drink':'https://unsplash.com/t/food-drink',
        'Athletics':'https://unsplash.com/t/athletics',
        'Spirituality':'https://unsplash.com/t/spirituality',
        'Arts & Culture':'https://unsplash.com/t/arts-culture',
        'History':'https://unsplash.com/t/history'
    }
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
            logging.info(f"正在执行 - {func.__name__}")
            return func(*args,**kwargs)
        except Exception as e:
            logging.error(repr(e)+'\n'+traceback.format_exc())
    return wrapper


#----------------------------------------------------------------------------
@log
def spider(type:str) -> str:
    url = Config.TYPE[type]
    r = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'})
    return r.text

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
    with open(os.path.join(path,filename),'wb') as f:
        f.write(content)
    with open(os.path.join(path,'main.jpg'),'wb') as f:
        f.write(content)

@log
def main():
    for type in Config.TYPE.keys():
        download(type,parse(spider(type)))


if __name__ == '__main__':
    main()
    # schedule.every().day.at('00:00').do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

