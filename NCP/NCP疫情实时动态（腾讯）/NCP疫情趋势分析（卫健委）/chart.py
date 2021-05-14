'''
@author: 人人都爱小雀斑
@time: 2020/2/26 17:57
@desc: pyecharts制作折线图等
'''
import time as t
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts.charts import *
from pyecharts import options as opts
# from example.commons import Faker  # pip install pyecharts==1.0
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


# 信息来自国家卫生健康委员会官方网站
def make_chart_echart(csvName, chartName):  # pyechart
    # 变量此时的数据类型:<class 'numpy.ndarray'>，需转化为列表
    (time, confirm, heal, dead, add, suspect, confirm_now) = np.loadtxt(csvName,
                                                           # encoding="",
                                                           skiprows=1,
                                                           dtype='str',
                                                           delimiter=',',
                                                           usecols=(0, 1, 2, 3, 4, 5, 6),
                                                           unpack=True)
    # 折线图表
    chart_Line = (
        Line()  # Bar()#init_opts=opts.InitOpts(theme=ThemeType.LIGHT)
            # x轴
            .add_xaxis([i[-5:].strip('0') for i in list(time)])  # [::-1]列表反转
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
            .add_yaxis("现有确诊", list(confirm_now), label_opts=opts.LabelOpts(is_show=False))
            # 全局配置项
            .set_global_opts(
            title_opts={"text": "中国疫情趋势图"},  # 图表标题@author：Billie , "subtext": "{}".format(t.strftime("%m-%d %H:%M:%S"))
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

    make_snapshot(snapshot, chart_Line.render('./html/main.html'), './charts/' + chartName + '.png')

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


def make_chart_plt(csvName, chartName):
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # windows 正常显示中文标签
    plt.rcParams["font.family"] = 'Arial Unicode MS' # macos 正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # 变量此时的数据类型:<class 'numpy.ndarray'>
    date = np.loadtxt(csvName, skiprows=1, dtype=str, delimiter=',', usecols=0, unpack=False)
    date = [i[-5:].strip('0') for i in date]
    # t=np.loadtxt(filename,skiprows=1,dtype=str,delimiter=",")
    (confirm, heal, dead, add, suspect) = np.loadtxt(csvName,
                                                     skiprows=1,
                                                     dtype=int,
                                                     delimiter=',',
                                                     usecols=(1, 2, 3, 4, 5),
                                                     unpack=True)
#新建图表
    fig = plt.figure(num=1, figsize=(10, 6), dpi=200)
    ax = fig.add_subplot(1, 1, 1,facecolor=None)  # 1个子图对象，位置1，1
#子图相关设置
                                            #marker:标注点样式；markervery:标注间隔；mfc(markerface):颜色；alpha:透明度
    ax.plot(date, confirm, linewidth=1, label="确诊",marker='o', markevery=10,mfc='orange', ms=5, alpha=0.7)
    ax.plot(date, heal, linewidth=1, label="治愈")
    ax.plot(date, dead, linewidth=1, label="死亡")
    ax.plot(date, add, linewidth=1, label="新增确诊")
##    ax.set_xlabel("日期",fontsize="7")
##    ax.set_ylabel("人数",fontsize="7")
    ax.legend()  # 线条注释，设置图例的前题是y指定了label
    ax.spines['top'].set_visible(False)  # 去掉边框
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # xminorLocator = plt.MultipleLocator(50)#x轴的刻度间隔
    # ax.xaxis.set_minor_locator(plt.NullLocator())
    # ax.xaxis.set_major_formatter(plt.NullFormatter())
    #添加标注点注释
    for i in range(0,len(date),30):#horizontalalignment(ha)：设置垂直对齐方式; verticalalignment(va)：设置水平对齐方式
        plt.text(date[i], confirm[i], confirm[i], ha='center', va='bottom', fontsize=10,alpha=0.8,color='mediumvioletred')#dodgerblue#
#描一个点
    # ax.annotate('point', xy=(0,0), xytext=(3, 1.5))  # 添加标注，参数：注释⽂本、指向点、⽂字位置、箭头属性
#全局设置
    # plt.xticks(time)
    plt.grid(b=True, which='major', axis='both', alpha=0.2, color='skyblue', linestyle='--', linewidth=2)
    # plt.xticks(range(0, 80, 10), rotation=None)  # 设置x轴刻度显示旋转45度显示
    # x轴标注
    # plt.xticks(range(0, len(date), 10))  # 以10天为间隔显示
    months = {'1.01': 'Jan', '2.01': 'Feb', '3.01': 'Mar', '4.01': 'Apr', '5.01': 'May', '6.01': 'June', '7.01': 'July',
              '8.01': 'Aug', '9.01': 'Sept', '10.01': 'Oct', '11.01': 'Nov', '12.01': 'Dec'}
    x, val = [], []
    for month in months.keys():
        if month in date:
            x.append(month)
            val.append(months[month])
    plt.xticks(x, val)
    plt.yticks([10000,30000,60000,100000], ['10k', '30k', '60k', '100k'])  #
    plt.suptitle("中国NCP疫情趋势图", fontsize=20)  # 大标题
    plt.title("@author:billie(数据来自国家卫生健康委员会官方网站)", loc='right', fontsize=10)  # 子标题
    plt.savefig("./charts/{}.png".format(chartName))
    # plt.show()
def matplotlib_test():
    import matplotlib.pyplot as plt
    x = np.arange(-5, 5, 0.1)
    y = x * 3
#创建窗口、子图
  # ⽅法1：先创建窗⼝，再创建⼦图。（⼀定绘制）
    fig = plt.figure(num=1, figsize=(15, 8), dpi=80)  # 开启⼀个窗⼝，同时设置⼤⼩，分辨率
    ax1 = fig.add_subplot(2, 1, 1)  # 通过fig添加⼦图，参数：⾏数，列数，第⼏个。
    ax2 = fig.add_subplot(2, 1, 2)  # 通过fig添加⼦图，参数：⾏数，列数，第⼏个。
  # ⽅法2：⼀次性创建窗⼝和多个⼦图。（空⽩不绘制）
    # fig, axes = plt.subplots(4, 1)  # 开⼀个新窗⼝，并添加4个⼦图，返回窗口/⼦图数组
    # ax1 = axes[0]  # 通过⼦图数组获取第⼀个⼦图
  # ⽅法3：⼀次性创建窗⼝和⼀个⼦图。（空⽩不绘制）
    # ax1 = plt.subplot(1, 1, 1, facecolor='white')  # 开⼀个新窗⼝，创建1个⼦图。facecolor设置背景颜⾊
# 获取对窗⼝的引⽤，适⽤于上⾯三种⽅法
    # fig = plt.gcf() #获得当前figure
    # fig=ax1.figure #获得指定⼦图所属窗⼝
    # fig.subplots_adjust(left=0)
# 设置⼦图的基本元素
    from matplotlib.ticker import MultipleLocator
    ax1.set_title('python-drawing')  # 设置图体，plt.title
    ax1.set_xlabel('x-name')  # 设置x轴名称,plt.xlabel
    ax1.set_ylabel('y-name')  # 设置y轴名称,plt.ylabel
    plt.axis([-6, 6, -10, 10])  # 设置横纵坐标轴范围，这个在⼦图中被分解为下⾯两个函数
    ax1.set_xlim(-5, 5)  # 设置横轴范围，会覆盖上⾯的横坐标,plt.xlim
    ax1.set_ylim(-10, 10)  # 设置纵轴范围，会覆盖上⾯的纵坐标,plt.ylim
    xmajorLocator = MultipleLocator(2)  # 定义横向主刻度标签的刻度差为2的倍数。就是隔⼏个刻度才显⽰⼀个标签⽂本
    ymajorLocator = MultipleLocator(3)  # 定义纵向主刻度标签的刻度差为3的倍数。就是隔⼏个刻度才显⽰⼀个标签⽂本
    ax1.xaxis.set_major_locator(xmajorLocator)  # x轴 应⽤定义的横向主刻度格式。如果不应⽤将采⽤默认刻度格式
    ax1.yaxis.set_major_locator(ymajorLocator)  # y轴 应⽤定义的纵向主刻度格式。如果不应⽤将采⽤默认刻度格式
    ax1.xaxis.grid(True, which='major')  # x坐标轴的⽹格使⽤定义的主刻度格式
    ax1.yaxis.grid(True, which='major')  # x坐标轴的⽹格使⽤定义的主刻度格式
    ax1.set_xticks([])  # 去除坐标轴刻度
    ax1.set_xticks((-5, -3, -1, 1, 3, 5))  # 设置坐标轴刻度

    ax1.set_xticklabels(labels=['x1', 'x2', 'x3', 'x4', 'x5'], rotation=-30, fontsize='small')  # 设置刻度的显⽰⽂本，rotation旋转⾓度，fontsize字体⼤⼩
    plot1 = ax1.plot(x, y, marker='o', color='g', label='legend1')  # 点图：marker图标
    plot2 = ax1.plot(x, y, linestyle='--', alpha=0.5, color='r', label='legend2')  # 线图：linestyle线性，alpha透明度，color颜⾊，label图例⽂本
    ax1.legend(loc='upper left')  # 显⽰图例,plt.legend()
    ax1.text(2.8, 7, r'y=3*x')  # 指定位置显⽰⽂字,plt.text()
    ax1.annotate('important point', xy=(2, 6), xytext=(3, 1.5),  # 添加标注，参数：注释⽂本、指向点、⽂字位置、箭头属性
    arrowprops = dict(facecolor='black', shrink=0.05),
    )

    # 显⽰⽹格。which参数的值为major(只绘制⼤刻度)、minor(只绘制⼩刻度)、both，默认值为major。axis为'x', 'y', 'both'
    ax1.grid(b=True, which='major', axis='both', alpha=0.5, color='skyblue', linestyle='--', linewidth=2)
    # axes1 = plt.axes([.2, .3, .1, .1], facecolor='y')  # 在当前窗⼝添加⼀个⼦图，rect=[左, 下, 宽, ⾼]，是使⽤的绝对布局，不和以存在窗⼝挤占空间
    # axes1.plot(x, y)  # 在⼦图上画图
    plt.savefig('aa.jpg', dpi=400, bbox_inches='tight')  # savefig保存图⽚，dpi分辨率，bbox_inches⼦图周边⽩⾊空间的⼤⼩
    plt.show()  # 打开窗⼝，对于⽅法1创建在窗⼝⼀定绘制，对于⽅法2⽅法3创建的窗⼝，若坐标系全部空⽩，则不绘制
# matplotlib_test()
