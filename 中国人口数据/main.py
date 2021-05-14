'''
author:billie

请求参数：sj(时间) zb:(指标)
LAST70：近70年
A0304：人口平均预期寿命；
A0305：人口普查人口基本情况；
A0306：人口抽样调查样本数据；
'''
import os
import time
import requests
import numpy as np
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Line, Bar, Page, Pie
from pyecharts.commons.utils import JsCode
class Population():
    def __init__(self):
        self.url='http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgnd&rowcode=zb&colcode=sj&wds=[]&dfwds={}'
        self.population_Dic={'2019':[140005,71527,68478,84843,55162,10.48,7.14,3.34,25061,97341,17603,43.82942439,25.74557483,18.08384956]}
    def spider(self):
        dfwds1 = '[{"wdcode": "sj", "valuecode": "LAST70"} {"wdcode":"zb","valuecode":"A0301"}]'#总人口
        dfwds2 = '[{"wdcode": "sj", "valuecode": "LAST70"} {"wdcode":"zb","valuecode":"A0302"}]'#人口出生率、人口死亡率、人口自然增长率
        dfwds3 = '[{"wdcode": "sj", "valuecode": "LAST70"} {"wdcode":"zb","valuecode":"A0303"}]'#人口年龄结构和抚养比
        for i in dfwds1,dfwds2,dfwds3:
            response=requests.get(self.url.format(i))
            datanodes=response.json()["returndata"]["datanodes"]
            for node in datanodes:
                # print(node)
                year=node['code'][-4:]#年份
                data=node['data']['data']#数据
                if year in self.population_Dic:#如年份已存在
                    if data == self.population_Dic[year][0]:pass#总人口数据重复
                    else:self.population_Dic[year].append(data)#添加数据项
                else:self.population_Dic[year]=[data]#创建键为年份的键值对
        for i in self.population_Dic:print(i,self.population_Dic[i])#输出字典元素
    def to_csv(self):
        data=self.population_Dic.values()#写入的数据
        index=self.population_Dic.keys()#行索引
        columns=["年末总人口(万人)","男性人口(万人)","女性人口(万人)","城镇人口(万人)","乡村人口(万人)",
                 "人口出生率(‰)","人口死亡率(‰)","人口自然增长率(‰)",
                 "0-14岁人口(万人)","15-64岁人口(万人)","65岁及以上人口(万人)","总抚养比(%)","少儿抚养比(%)","老年抚养比(%)"]#列索引
        df=pd.DataFrame(data,index=index,columns=columns)
        df.to_csv("中国70年人口数据.csv",encoding="gbk")
    def make_chart(self):
        (year,population,men)=np.loadtxt("中国70年人口数据.csv",
                              dtype="str",
                              delimiter=",",
                              skiprows=(1),
                               usecols=(0,1,2),
                              unpack=True)

        year=list(year)[::-1]
        population=list(population)[::-1]

        chart=Line()
        chart.add_xaxis(year)
        chart.add_yaxis("总人口(人)",population)
        # c = Line().add_xaxis(year).add_yaxis("总人口(人)", population)
        # chart.overlap(c)
        chart.width=100
        chart.render("main.html")
        os.startfile(os.getcwd()+"\\main.html")#打开html文件
        print(population)
if __name__ == '__main__':
    billie=Population()
    billie.spider()
    billie.to_csv()
    billie.make_chart()