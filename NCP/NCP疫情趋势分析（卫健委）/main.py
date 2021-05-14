'''
@author: 人人都爱小雀斑
@time: 2020/2/25 16:57
@desc:爬取中共卫健委网站，获取历史疫情数据，绘制图表
2-25 使用火狐浏览器对象，成功爬取到卫健委官网
2-26 加入显式等待，Explicit_Waits模块
2-28 学习正则表达式
2-29 使用正则表达式，编写match函数；save_to_csv()，项目基本成型
'''
import os
import re
import threading
import time
import datetime
import pandas as pd
from lxml import etree
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

class Epidemic:
    def __init__(self):
        self.url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
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
    def spider(self):
        self.driver.get(self.url)  # 发送访问请求
        self.Explicit_Waits(self.driver, By.XPATH, '//div[@class="pagination_index"]')#显式等待在DOM中找到目标元素
        lis = self.driver.find_elements_by_xpath('/html/body/div[3]/div[2]/ul/li')
        # for i in lis:
        #     print(i.text)
        window_1=self.driver.current_window_handle#第一个窗口

        for li in lis:#self.bar(
            #获取数据统计的日期
            date=li.find_element_by_tag_name('span').text
            now = datetime.datetime.strptime(date, '%Y-%m-%d')
            delta = datetime.timedelta(days=1)
            date = (now - delta).strftime('%Y-%m-%d')
            #1.20号之前的不取，结束循环
            if date<time.strftime("2020-01-20"):break
            #点击进入子页面
            li.find_element_by_tag_name('a').send_keys(Keys.ENTER)
            time.sleep(0.1)#不加这行，就会获取不到完整的窗口句柄
            self.driver.switch_to.window(self.driver.window_handles[-1])  #获取当前页所有窗口句柄,切换到第二个窗口
            text=self.Explicit_Waits(self.driver, By.XPATH, '//*[@id="xw_box"]').text.replace("分享到","")
            print(date,"success!")#,end=''
            #将信息写入本地文件
            with open("./texts/{}.txt".format(date), "w",encoding="utf-8") as f:f.write(text)
            #关闭页面
            self.driver.close()
            self.driver.switch_to.window(window_1)  #获取当前页所有窗口句柄,切换到第一个窗口

        # 寻找下一页
        self.Explicit_Waits(self.driver, By.XPATH, '//div[@class="pagination_index"]')#等待在DOM中找到目标元素
        page_index = self.driver.find_elements_by_xpath('//div[@class="pagination_index"]')
        for index in page_index:
            if index.text == "下一页":#如有下一页
                index.find_element_by_tag_name("a").send_keys(Keys.ENTER)#.click()#点击下一页
                time.sleep(0.2)#预留时间加载网页
                self.url=self.driver.current_url
                self.spider()

    # 读取保存在本地的txt文本，进行数据的过滤，提取信息
    def match(self):
        fileList=os.listdir("./texts")
        fileList.sort() # 大到小排序
        fileList = fileList[::-1]
        print("正在处理字符串...")
        for i in fileList:
            # try:
                date=i[5:-4].replace('-','.')#日期
                text=open(os.getcwd()+"/texts/"+i,"rt",encoding="utf-8").read()#文本
                print(date) # ,text
                comp='(31)?(个)?省（(自治)?区、(直辖)?市）(和新疆生产建设兵团)?(.*?)'
                try:confirm_add = re.search(r"新增(新型冠状病毒感染的肺炎)?确诊病例(\d+)",text).group(2)
                except:confirm_add = 0
                confirm = re.search(comp+r"累计(报告)?(新型冠状病毒感染的肺炎)?确诊病例(\d+)",text).group(9)#累计报告确诊病例(\d+)|
                try:heal = re.search(comp+r"累计治愈出院(病例)?(\d+)",text).group(8)
                except:
                    try:heal = re.search(r"已治愈出院(\d+)",text).group(1)
                    except:heal=0
                try:dead = re.search(comp+r"累计死亡(病例)?(\d+)",text).group(8)
                except:
                    try:dead = re.search(r"其中重症(\d+)?例，死亡(\d+)",text).group(2)
                    except:dead=0
                try:suspect = re.search(comp+r"现有疑似病例(\d+)",text).group(7)
                except:
                    try:suspect = re.search(r"累计报告疑似病例(\d+)",text).group(1)
                    except:
                        try:suspect = re.search(r"共有疑似病例(\d+)",text).group(1)
                        except:suspect = 0
                try:confirm_now=re.search(comp+"现有确诊病例(\d+)",text).group(7)
                except:confirm_now=0
                self.dataDic[date]=[confirm,heal,dead,confirm_add,suspect,confirm_now]
                # print(confirm,heal,dead,confirm_add,suspect,confirm_now)
            # except:print('跳过：',i)
            # except Exception as err:print(err)

    # 保存数据至csv文件
    def save_to_csv(self):
        print("正在保存疫情数据到本地...")
        indexs=[i for i in list(self.dataDic.keys())[::-1]]#行索引
        columns=["累计确诊", "累计治愈", "累计死亡", "新增确诊", "疑似病例","现有确诊"]#列索引
        data=list(self.dataDic.values())[::-1]
        df=pd.DataFrame(data=data,index=indexs,columns=columns)
        df.to_csv("./tables/main.csv",encoding="utf-8")
        df2=pd.DataFrame(data=self.dataDic,index=columns)
        df2.to_csv("./tables/maint.csv",encoding="utf-8")

    # 主函数
    def main(self):
        print("正在访问卫健委官方网站...")
        # 无窗口弹出操作
        options = FO()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # 创建火狐浏览器对象,经测试，谷歌浏览器会翻车
        # self.driver = selenium.webdriver.Firefox()  #options=options
        #获取信息并匹配数据
        print("正在获取疫情数据...")
        # self.spider()
        #匹配文本
        self.match()
        #保存到文件
        self.save_to_csv()
        #制作图表
        print("正在生成图表...")
        chart.make_chart_plt(csvName="./tables/main.csv",chartName='chart_plt')
        # chart.make_chart_echart(csvName="./tables/main.csv",chartName='chart_echart')
        print("制作图表成功！")


billie=Epidemic()
billie.main()




