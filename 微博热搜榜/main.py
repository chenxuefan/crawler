
'''
@Author billie
@Date 2020/1/21 8:34
@Describe

'''
import csv
import os

from lxml import etree
import requests
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
import threading
import datetime
import time
import urllib.parse

class HotSearch:
    def __init__(self):
        self.url="https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6"
        self.DataDic = {} #数据字典dataDic
        self.now_date = str(datetime.datetime.now().date()) #当前日期
        self.base_name = [] # 存储已存在文件中的热搜关键词，用作后续数据比对
        self.tplt = "{0:{4}<8}\t{1:{4}<10}\t{2:{4}<15}\t{3:{4}<20}"

    def spider1(self):#selenium方法
        options = Options()
        options.add_argument('--no-sandbox')#root权限
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')#无窗口弹出
        driver=selenium.webdriver.Chrome(options=options)#
        driver.get(self.url)#发送访问请求
        #查找所需元素
        No=driver.find_element_by_xpath('//*[@id="pl_top_realtimehot"]/table/thead/tr/th[1]').text#序号
        keyword = driver.find_element_by_xpath('//*[@id="pl_top_realtimehot"]/table/thead/tr/th[2]').text#热度
        trs =driver.find_elements_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr')#关键词
        tplt = "{0:{4}<8}\t{1:{4}<10}\t{2:{4}<10}\t{3:{4}<10}"
        print(tplt.format(No,"访问数",keyword,"链接",chr(12288))+"\n")
        for tr in trs[1:]:
            self.ranktop=tr.find_element_by_xpath('./td[1]').text#排序
            self.name = tr.find_element_by_xpath('./td[2]/a').text#关键词
            try:self.href = "https://s.weibo.com"+tr.find_element_by_xpath('./td[2]/a').get_attribute('href_to')#["href_to"]
            except:self.href = tr.find_element_by_xpath('./td[2]/a').get_attribute('href')#["href"]
            self.num = tr.find_element_by_xpath('./td[2]/span').text#访问数
            # 输出统计结果
            print(tplt.format(self.ranktop,self.num,self.name,self.href,chr(12288)))
            #添加dataDic字典元素
            self.DataDic[self.name]=self.href
        #输出统计结果（以列表方法）
        # 获取字典键值对（name : href），存为列表
        # item_list = list(dataDic.items())
        # for i in range(len(item_list)):
        #     keyword, href = item_list[i]
        #     print(tplt.format(i+1,keyword,href,chr(12288)))

    def spider2(self):#requests + xpath方法
        r=requests.get(self.url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})
        r.encoding='utf-8'
        html=etree.HTML(r.text)
        trs = html.xpath(f'//tbody/tr')

        print("\n" + self.tplt.format("序号", "访问数", "关键词", "链接", chr(12288)) + "\n")
        for tr in trs[1:]:
            ranktop = tr.xpath('./td[1]')[0].text  # 排序
            name = tr.xpath('./td[2]/a')[0].text  # 关键词
            href = urllib.parse.urljoin("https://s.weibo.com",tr.xpath('./td[2]/a/@href | ./td[2]/a/@href_to')[0])  # ["href_to"]
            num = ' ' if ranktop=='•' else tr.xpath('./td[2]/span')[0].text  # 访问数
            # 输出统计结果
            print(self.tplt.format(ranktop, num, name, href, chr(12288)))
            # 添加dataDic字典元素
            self.DataDic[name] = href

    #储存全部热搜结果为csv文件
    def save_all_datas(self):
        with open("./datas/all_datas.csv","a",newline="",encoding='gbk')as base_data1,\
                open("./datas/all_datas.csv","r",newline="",encoding='gbk')as base_data2:
            #读取本地数据库为base_data
            base_data = csv.reader(base_data2)  # 返回值：[[],[]，]
            for data in base_data:  # data:list
                self.base_name.append(data[1])  # 添加本地文件里的第二列的数据（热搜关键词）
            #判断是否添加数据
            for i in self.DataDic:#遍历当前数据列表
                if i not in self.base_name:#如不在数据库中，则添加数据
                    data = [self.now_date, i, self.DataDic[i]]  # 创建写入数据
                    writer = csv.writer(base_data1)  # 创建csv写入操作对象writer
                    writer.writerow(data)
                    continue#进行下一项的比对

    #储存热搜前三结果为csv文件
    def save_previous_three_datas(self):
        previous_3_keys=list(self.DataDic)[:3]
        with open("./datas/pre_three_datas.csv", "a", newline="",encoding='gbk')as base_data1, \
                open("./datas/pre_three_datas.csv", "r", newline="",encoding='gbk')as base_data2:
            # 读取本地数据库为base_data
            base_data = csv.reader(base_data2)#返回值：[[],[]，]
            for data in base_data:#data:list
                self.base_name.append(data[1])#添加文件里的第二列的数据（热搜关键词）
            # 判断是否添加数据
            for i in previous_3_keys:
                if i not in self.base_name:  # 如不在数据库中，则添加数据
                    data = [self.now_date, i, self.DataDic[i]]  # 创建写入数据
                    writer = csv.writer(base_data1)  # 创建csv写入操作对象writer
                    writer.writerow(data)  # 写入数据
                    continue  #进行下一项的比对

    #储存热搜第一结果为csv文件
    def save_top_datas(self):
        top_key=list(self.DataDic)[0]
        with open("./datas/top_datas.csv", "a", newline="",encoding='gbk')as base_data1, \
                open("./datas/top_datas.csv", "r", newline="",encoding='gbk')as base_data2:
            # 读取本地数据库为base_data
            base_data = csv.reader(base_data2)#返回值：[[],[]，]
            for data in base_data:#data:list
                self.base_name.append(data[1])#添加文件里的第二列的数据（热搜关键词）
            if top_key not in self.base_name:# 如不在数据库中，则添加数据
                data = [self.now_date, top_key, self.DataDic[top_key]]  # 创建写入数据
                writer = csv.writer(base_data1)  # 创建csv写入操作对象writer
                writer.writerow(data)
    #执行任务
    def main(self):
        try:
            print("\n"+str(time.strftime("%H:%M:%S")))#输出当前时间
            #执行主程序
            self.spider2()
            self.save_all_datas()
            self.save_previous_three_datas()
            self.save_top_datas()
            # 设置间隔时间执行程序
            threading.Timer(1000, self.main).start()  # 设定每xxx秒执行一次do_job函数
        # except:#模拟类似断网的状况，使程序不会报错停止
        #     self.main()
        except Exception as err:
            print(err)

if __name__ == '__main__':
    billie=HotSearch()
    billie.main()
    # os.startfile(os.getcwd()+'./back_up.py')#启动备份程序

