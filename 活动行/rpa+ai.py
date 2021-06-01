# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2021/5/30 2:38 下午
@Describe 
"""
import time
from selenium import webdriver

driver = webdriver.Chrome()
# driver.get('https://www.taobao.com/?spm=a230r.7195193.1581860521.1.15c0580aOi9gMz')
driver.get('https://www.huodongxing.com/events')


try:

            print("使用本地保存的cookies...")
            cookies = eval(open('./login_cookies.txt', 'r').read())  #
            print(cookies)
            for cookie in cookies:
                try:driver.add_cookie(cookie)
                except:pass
            driver.refresh()
            for i in range(1, 200):
                time.sleep(1)
                driver.get(f'https://www.huodongxing.com/events?page={i}')
                print(i, len(driver.page_source))


except:
    pass



