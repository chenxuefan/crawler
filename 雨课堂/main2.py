# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/12/3 8:21 下午
@Describe 
"""
import os
import re
import threading
import time
import datetime
import pandas as pd
from lxml import etree
import requests
from pprint import pprint
import selenium.webdriver
from selenium.webdriver.chrome.options import Options as CO#谷歌浏览器option
from selenium.webdriver.firefox.options import Options as FO#火狐浏览器option
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#显式等待
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#
import chart
from progressbar import *

class Yuketang:
    def __init__(self):
        self.login_url = "https://sziit.yuketang.cn/pro/portal/home/"
        self.dataDic = dict()
        self.bar=ProgressBar(widgets=[Percentage(),Bar('#'), ' ', Timer(), ' ', ETA(), ' '])#,term_width=12,FileTransferSpeed(),
    def Explicit_Waits(self,driver, way, path):#显式等待
        try:
            ele = WebDriverWait(driver, 150).until(
                EC.presence_of_element_located((way, path)))
            return ele
        except Exception as e:
            print('元素寻找失败： ' + str(e))
    # 爬取数据
    def login(self):
        # 创建浏览器对象
        options = CO()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = selenium.webdriver.Chrome(options=options)  #
        try:
            print("使用本地保存的cookies...")
            self.cookies = eval(open('./bd_login_cookies.txt', 'r').read())  #
            print(self.cookies)
            for cookie in self.cookies:
                if 'expiry' in cookie:
                    del cookie['expiry']
                try:self.driver.add_cookie(cookie)
                except:pass
            self.driver.refresh()
        except Exception as err:
            # print(err)

            print("正在扫码登录...")
            self.Explicit_Waits(self.driver,By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button')
            self.driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button').click() # 点击登陆按钮
            self.Explicit_Waits(self.driver,By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button')

            time.sleep(10) # 扫码时间为5秒，扫码不成功则报错，程序停止
            self.cookies = self.driver.get_cookies()  # 拿到登陆后的cookies，里面有很多参数后面会用到
            with open('./bd_login_cookies.txt', 'w')as f:f.write(str(self.cookies)) # 保存cookies至本地

            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/button').click()  # 点击我的学习空间
            self.Explicit_Waits(self.driver, By.XPATH, '//*[@id="pane-student"]/div/div[1]/div/div')
            self.driver.find_element_by_xpath('//*[@id="pane-student"]/div/div[1]/div/div').click()  # 点击形势与政策
            chapter_list = self.driver.find_elements_by_class_name('chapter-list')
            # pprint(cookies)
            for chapter in chapter_list:  # 遍历每一个专题content
                contents = chapter.find_elements_by_class_name('content')
                for content in contents:
                    print(content)
                    content.find_elements_by_class_name('leaf-title text-ellipsis').click()

        print(len(self.cookies),self.cookies)
        pprint(self.cookies[0])
        pprint(self.cookies[1])
        pprint(self.cookies[2])
        pprint(self.cookies[3])
        pprint(self.cookies[4])



        # time.sleep(1000)
    def get_message(self):

        headers = {
            'authority': 'sziit.yuketang.cn',
            'method': 'GET',
            'path': '/mooc-api/v1/lms/user/user-courses/?status=1&page=1&no_page=1&term=latest&uv_id={}'.format(self.cookies[4]['value']),
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'university_id={}; platform_id=3; user_role=3; csrftoken={}; sessionid={}; platform_id=3; university_id={}; user_role=3; sessionid={}'.format(
                self.cookies[4]['value'],self.cookies[1]['value'],self.cookies[2]['value'],self.cookies[4]['value'],self.cookies[2]['value'],
            ),
            'referer': 'https://sziit.yuketang.cn/pro/courselist',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'university-id': self.cookies[4]['value'],
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'x-csrftoken': self.cookies[1]['value'],
            'xtbz': 'cloud'}

        # 必要参数的获取
        uv_id = self.cookies[-1]['value']  # university_id
        product_list = requests.get(
            url='https://sziit.yuketang.cn/mooc-api/v1/lms/user/user-courses/?status=1&page=1&no_page=1&term=latest&uv_id={}'.format(uv_id),
            headers=headers)  # 包含所有课程的详细参数信息
        product_list.encoding="utf-8"
        product_list = product_list.json()['data']['product_list']
        # pprint(product_list)
        classroom_id = product_list[0]['classroom_id'] # classroom_id,0表示所有课程列表中第一位，即形式与政策
        sign = product_list[0]['course_sign'] # course_sign,0表示所有课程列表中第一位，即形式与政策
        cource_id = product_list[0]['course_id']
        course_chapter = requests.get(
            url = 'https://sziit.yuketang.cn/mooc-api/v1/lms/learn/course/chapter?cid={}&sign={}&term=latest&uv_id={}'.format(classroom_id,sign,uv_id),
            headers = headers)
        course_chapter.encoding = 'utf-8'
        course_chapter = course_chapter.json()['data']['course_chapter']
        # pprint(course_chapter)

        for chapter in course_chapter:
            for section_leaf in chapter['section_leaf_list']:
                video_id = section_leaf['id']
                print(video_id)
                info = requests.get(
                    url='https://sziit.yuketang.cn/mooc-api/v1/lms/learn/leaf_info/{}/{}/?sign={}&term=latest&uv_id={}'.format(classroom_id,video_id,sign,uv_id),
                    headers = headers
                ).json()['data']

                # pprint(info)
                ccid = info['content_info']['media']['ccid']
                sku_id = info['sku_id']
                ts = time.time() # 当前时间戳

                user_id = requests.get(
                    url='https://sziit.yuketang.cn/edu_admin/check_user_session/?_={}'.format(ts),
                    headers = headers
                ).json()['data']['user_id']

                video_length = requests.get(
                    url='https://sziit.yuketang.cn/video-log/get_video_watch_progress/?cid={}&user_id={}&classroom_id={}&video_type=video&vtype=rate&video_id={}&snapshot=1&term=latest&uv_id={}'.format(cource_id,user_id,classroom_id,video_id,uv_id),
                    headers = headers
                ).json()['{}'.format(video_id)]['video_length']
                print(video_length)

                data = {
                    'heart_data': [
                        {
                            'c': cource_id,
                            'cc': ccid,
                            'classroomid': classroom_id,
                            'cp': video_length,
                            'd': video_length,
                            'et': "heartbeat",
                            'fp': 0,
                            'i': 5,
                            'lob': "cloud4",
                            'n': "ws",
                            'p': "web",
                            'pg': "{}_17h6k".format(video_id),
                            'skuid': sku_id,
                            'sp': 1,
                            'sq': 18,
                            't': "video",
                            'tp': video_length,
                            'ts': ts,
                            'u': user_id,
                            'uip': "",
                            'v': video_id
                        }
                    ]
                }
                r = requests.post(
                    url='https://sziit.yuketang.cn/video-log/heartbeat/',
                    headers = headers,
                    data = data
                )
                print(r.text)
            pprint(chapter)




    # 主函数
    def main(self):
        print("")

        # login
        self.login()
        self.get_message()

billie=Yuketang()
billie.main()