'''
@author: 人人都爱小雀斑
@time: 2020/2/26 17:57
@desc: pyecharts制作折线图等
'''

import numpy as np
import matplotlib.pyplot as plt
from pyecharts.charts import *
from pyecharts import options as opts
from example.commons import Faker#pip install pyecharts==1.0
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
#信息来自国家卫生健康委员会官方网站
def make_chart_echart(csvName,chartPath,chartName):  # pyechart
    # 变量此时的数据类型:<class 'numpy.ndarray'>，需转化为列表
    (time, confirm, heal, dead, add, suspect) = np.loadtxt(csvName,
                                                           # encoding="",
                                                           skiprows=1,
                                                           dtype='str',
                                                           delimiter=',',
                                                           usecols=(0, 1, 2, 3, 4, 5),
                                                           unpack=True)
    # 折线图表
    chart_Line = (
        Line()  # Bar()#init_opts=opts.InitOpts(theme=ThemeType.LIGHT)
            # x轴
            .add_xaxis([i[-4:] for i in list(time)])#[::-1]列表反转
            # y轴
            .add_yaxis("确诊",
                       list(confirm),
                       linestyle_opts=opts.LineStyleOpts(width=2),  # 线条样式
                       is_smooth=True,  # 平滑曲线
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.1),  # 区域渲染
                       label_opts=opts.LabelOpts(is_show=False)  # 显示具体数据True
                       )
            .add_yaxis("治愈", list(heal), label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("死亡", list(dead), label_opts=opts.LabelOpts(is_show=False))
            .add_yaxis("新增确诊", list(add), label_opts=opts.LabelOpts(is_show=False))  # True
            .add_yaxis("疑似病例", list(suspect), label_opts=opts.LabelOpts(is_show=False))
            # 全局配置项
            .set_global_opts(
            title_opts={"text": chartName+"NCP疫情趋势图", "subtext": "{}".format(" ")},  # 图表标题
            # xaxis_opts={"name":"日期"},
            xaxis_opts=opts.AxisOpts(
                name="日期",
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True), boundary_gap=False,  # 图像贴近y轴
            ),
            # yaxis_opts={"name":"人数",}
            yaxis_opts=opts.AxisOpts(
                name="人数",
                # type_="log",is_scale=True,#10,100,1000
                splitline_opts=opts.SplitLineOpts(is_show=True),  # 水平分割线
            )
        )
        # 系列配置项(需放置最后)
        # .set_series_opts(
        #     symbol_size=[34, 30],
        # areastyle_opts=opts.AreaStyleOpts(opacity=0.5),#渲染
        # label_opts=opts.LabelOpts(is_show=False),#显示数据
        # )
    )
    chart_Line.width = '200'

    make_snapshot(snapshot,chart_Line.render(chartPath+chartName+".html"), 'chart_echart.png')

    # 地理图表
    chart_Geo = (
        Geo()
            .add_schema(maptype="china")
            .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="Geo-基本示例"),
        )
    )
    # print([list(z) for z in zip(Faker.provinces, Faker.values())])
    page = Page().add(chart_Line, chart_Geo).page_title = "NCP疫情动态"  # 网页标头


def make_chart_plt(csvName,chartPath,chartName):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # 变量此时的数据类型:<class 'numpy.ndarray'>
    time=np.loadtxt(csvName,skiprows=1,dtype=str,delimiter=',',usecols=0,unpack=False)
    # t=np.loadtxt(filename,skiprows=1,dtype=str,delimiter=",")
    (confirm, heal, dead) = np.loadtxt(csvName,
                                                           skiprows=1,
                                                           dtype=str,
                                                           delimiter=',',
                                                           usecols=(1, 2, 3),
                                                           unpack=True)
    time=[i[-4:] for i in time]
    confirm=[int(i) for i in confirm]
    heal=[int(i) for i in heal]
    dead=[int(i) for i in dead]

    plt.figure(figsize=(10,6),dpi=200)
    plt.plot(time,confirm, linewidth=1, label="确诊", )
    plt.plot(time,heal, linewidth=1, label="治愈")
    plt.plot(time,dead, linewidth=1, label="死亡")
    # plt.xticks(time)
    plt.grid()
    plt.xticks(range(0,90,3),rotation=45)  # 旋转45度显示
    # plt.yticks(range(min(confirm), max(confirm) + 1))
    # plt.ylim((0, 20))
    plt.xlabel("日期")
    plt.ylabel("人数")
    plt.suptitle("中国NCP疫情趋势图")
    plt.title("@author:billie(数据来自国家卫生健康委员会官方网站)",loc='right')
    plt.legend()  # 设置图例的前题是y指定了label
    plt.savefig("{}{}".format(chartPath,'chart_plt.png'))
    plt.show()