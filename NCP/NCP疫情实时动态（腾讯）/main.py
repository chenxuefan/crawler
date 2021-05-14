'''
@author：Billie
更新说明：
1-28 17:00 项目开始着手，spider方法抓取到第一条疫情数据，save_data_csv方法将疫情数据保存至csv文件
1-29 13:12 目标网页文档树改变，爬取策略修改，建立新方法：spider2
1-30 15:00 新建变量national_confirm,存储全国新增确诊数
1-31 15:00 摸鱼，缝缝补补又一天
2-01 15:00 目标网页文档树又改变了，爬取策略修改，建立新方法：spider3，全国数据改用xpath方法查找，全国数据新增“较昨日+”内容显示
2-02 15:00 建立新方法：save_data_main,存储所有日期的全国动态数据到main.csv,复习numpy,pandas
2-03 15:00 建立新方法：make_pic,使用matplotlib绘图
2-09 10:00 建立新方法：__init__,设置全局变量
2-11 14:00 建立新方法：make_chart,使用pyechart绘制图表
2-16 16:00 新建两个变量 self.icbar_nowConfirm：现有确诊；self.icbar_nowSevere：现有重症
2-26 17:00 查询、图表模块改为外部引用（spider.py,chart.py）
'''
import csv
import pandas as pd
import threading
import time
import os
from chart import *
from spider import spider

class Epidemic():
    def __init__(self):
        self.dataDic=dict()
        self.lastUpdateTime= 0
    def save_data_csv(self,filepath,filename):#存储到allcsv\dailycsv中的csv文件
        # filename="_".join(time.split(":"))
        dataList=list(self.dataDic.values())
        with open(filepath+"//"+filename+".csv","w",newline="",encoding='gbk') as f:
            writer=csv.writer(f)
            writer.writerow(["地区","确诊人数","治愈人数","死亡人数","新增确诊","疑似病例","现有确诊","现有重症"])
            for i in dataList:writer.writerow(i)#写入各个地区的数据
            writer.writerow([self.lastUpdateTime])#最后一行附上截至时间
    def save_data_main(self,filename):#存储所有日期的全国动态数据
        allfile=os.listdir("dailycsv")#所有的目标文件
        columns=["确诊人数", "治愈人数", "死亡人数", "新增确诊", "疑似病例","现有确诊","现有重症"]#df参数1：main.csv的行索引
        index = [file[:-4] for file in allfile]#df参数2：main.csv的列索引,索引为去掉'.csv'的文件名
        data = []#df参数3：写入df的数据
        for file in allfile:#file: 2020-xx-xx xx xx xx.csv
            with open("dailycsv//"+file,"r",encoding='gbk') as f:#打开目标文件
                d=list(csv.reader(f))#读取目标文件数据，返回list
                data.append(d[1][1:])#目标数据是第一行的全国数据，且从第二列开始
        df=pd.DataFrame(data,index=index,columns=columns)#创建dataframe对象
        df.to_csv(filename,encoding="gbk")#将dataframe对象保存至csv文件
    def main(self):
        #获取数据(spider.py中的spider类)
        s = spider()
        s.spider4()
        self.dataDic=s.dataDic
        # for i in self.dataDic:
        #     print(i,self.dataDic[i])
        self.lastUpdateTime=s.lastUpdateTime
        #保存数据
        self.save_data_csv(filepath="allcsv",
                           filename=self.lastUpdateTime.replace(":", " "))  # 存入allcsv文件夹
        self.save_data_csv(filepath="dailycsv",
                           filename=self.lastUpdateTime.replace(":", " ")[:10])  # 存入dailycsv文件夹
        self.save_data_main(filename="main.csv")
        #制作图表
        print("正在生成图表...")
        make_chart_plt(csvName="./main.csv",chartPath='./',chartName='main')
        make_chart_echart(csvName="./main.csv",chartPath='./',chartName='main')
        # if int(time.strftime("%H"))<10: os.startfile(os.getcwd()+"\\main.html")#打开文件
        print("运行时间：",round(time.process_time()),"s")
        #设定运行间隔时间
        threading.Timer(10000,self.main).start()

if __name__ == '__main__':
    billie=Epidemic()
    billie.main()
