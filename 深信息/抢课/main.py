# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 23:39:34 2020

@author: billie

程序运行环境要求：
-python3
-selenium（python第三方库，可用pip安装）
-chromedriver（配置方法可自行百度，需配置对应chrome版本的chromedriver）

网络环境要求：
-学校内网

-----------------具备上述环境要求之后才可成功运行下面的程序--------------------
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

class Spider():
    def spider(self,url,name,passwd,className):
        try:
            # options = Options()
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')

            # options = webdriver.ChromeOptions()
            # options.add_argument('--ignore-certificate-errors')
            
            # 建立一个chrome对象
            driver = webdriver.Chrome()#options=options
            driver.get(url)
            # #-------------------------深信息官网-------------------------
            # # 执行页面向下滑至底部的动作
            # driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # new=driver.find_element_by_xpath('/html/body/div[7]/div/div[1]/ul/li[2]/p[7]/a')
            # new.click()
            #---------------------------登录页面-------------------------------
            time.sleep(2)
            nameInput=driver.find_element_by_id("yhm")#获取用户名输入框
            nameInput.send_keys(name)
            passwdInput=driver.find_element_by_id("mm")#获取密码输入框
            passwdInput.send_keys(passwd)
            login=driver.find_element_by_id("dl")#获取登录按钮
            login.click()#点击登录按钮
            # time.sleep(2)
            #-----------------------教学综合信息服务平台页面---------------------
            # time.sleep(1)
            # time.sleep(5)
            drop=driver.find_element_by_xpath('//*[@id="cdNav"]/ul/li[3]')#获取‘选课’下拉菜单
            drop.click()
            selectClass=driver.find_element_by_xpath('//*[@id="cdNav"]/ul/li[3]/ul/li[2]/a')#获取‘自主选课’链接
            selectClass.click()
            #----------------------------选课页面------------------------------
            # time.sleep()
            # 切换窗口到新打开的页面
            #driver.current_window_handle #当前网页窗口
            n = driver.window_handles  #获取当前页所有窗口句柄
            driver.switch_to.window(n[1])#切换到第二个窗口
            search=driver.find_element_by_xpath('//*[@id="searchBox"]/div/div[1]/div/div/div/div/input')#获取搜索输入框
            search.send_keys(className)#发送输入信息
            button=driver.find_element_by_xpath('//*[@id="searchBox"]/div/div[1]/div/div/div/div/span/button[1]')#获取查询按钮
            button.click()
            # # 执行页面向下滑至底部的动作
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # selectMyLeason=driver.find_element_by_xpath('//*[@id="tr_9A6F97874AF01288E053641E10ACE1E2"]/td[21]/button')#获取选课链接
            # selectMyLeason.click()#选课
            print("选课成功！")
            time.sleep(10000)

        except Exception as err:
            print(err)
# base_url="http://xjwgl2020.frp.sziitjx.cn:8080"#切勿泄露
# base_url="http://xjwgl.frp.sziitjx.cn"
base_url="http://xjwgl.sziit.edu.cn"
url=base_url+"/xtgl/login_slogin.html?language=zh_CN&_t=1577806337435"
billie=Spider()


with open("name&passwd.txt","rt",encoding="utf-8") as f:
    # 1905100343
    # xkxhxk520
    # 股票技术分析
    p=f.readlines()
    #在这里输入你的学号
    name=p[0].strip("\n")
    #在这里输入你的登录密码
    passwd=p[1].strip("\n")
    #在这里输入你想选的课的名称，比如数学建模，程序进入选课页面之后会自动帮你搜索这门课，没有想选的课的话也可留空
    className=p[2]
    billie.spider(url,name,passwd,className)