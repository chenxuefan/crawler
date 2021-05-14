# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2021/5/11 11:28 上午
@Describe
需求分析
    - 爬取最新电影数据（电影名称、链接、日期）
    - 保存数据至本地Excel
    - 对比本地数据库，如有更新，发送邮件提醒（附上电影信息、链接）
"""

import requests
from lxml import etree
import os,logging,time,openpyxl,schedule
from functools import wraps
from emailService import email


logging.basicConfig(
    filename='./dytt.log',
    format=f"%(asctime)s %(levelname)s[%(lineno)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level = logging.INFO
)

def log(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            logging.error(repr(e))
    return wrapper


#==========================================


class Dytt:
    def __init__(self):
        self.base_url = "https://www.dy2018.com"
        self.dy_dict = None

    @log
    def spider(self):
        """
        :description : 获取网站当前电影数据，保存电影数据至dy_dict
        """
        r = requests.get(url=self.base_url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'})
        r.encoding = 'gbk'
        eleTree = etree.HTML(r.text)

        titles = eleTree.xpath('//a[text()="2021新片精品"]/../../../../div[@class="co_content222"]/descendant::a/text()')
        hrefs = eleTree.xpath('//a[text()="2021新片精品"]/../../../../div[@class="co_content222"]/descendant::a/@href')[1:]
        hrefs = [self.base_url+href for href in hrefs]

        self.dy_dict = dict(zip(titles,hrefs))
        logging.info(f"已获取电影数据:\n{self.dy_dict}")

    @log
    def get_data(self) -> dict:
        """
        :returns new_data:如有最新的电影数据，则返回，否则返回None
        """
        path = "./dytt.xlsx"
        if not os.path.exists(path):
            return self.dy_dict
        elif os.path.exists(path):
            wb = openpyxl.load_workbook(path)
            ws = wb.active
            database = [cell.value for cell in ws["A"]][1:]
            new_data = {}
            for title in list(self.dy_dict.keys()):
                if title not in database:
                    new_data[title] = self.dy_dict[title]
                    return new_data

            if new_data:
                return new_data
            elif not new_data:
                return None

    @log
    def write(self,new_movie):
        dy_dict = new_movie
        path = "./dytt.xlsx"
        if not os.path.exists(path):
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(['title','hrefs'])
        if os.path.exists(path):
            wb = openpyxl.load_workbook(path)
            ws = wb.active

        start_row = ws.max_row + 1

        for title,href in dy_dict.items():
            ws[f"A{start_row}"] = title
            ws[f"B{start_row}"] = href
            ws[f"C{start_row}"] = time.strftime("%Y/%m/%d")
            start_row += 1

        wb.save(path)

    @log
    def mail(self,new_movie):
        e = email()
        e.get_msg(new_movie)
        e.send_email()

    def main(self):
        self.spider()
        new_movie = self.get_data()
        if new_movie:
            logging.info(new_movie)
            self.write(new_movie)
            self.mail(new_movie)



if __name__ == '__main__':
    # 设定定时
    schedule.every().day.at("09:00").do(Dytt().main)
    while True:
        schedule.run_pending()
        time.sleep(1)
