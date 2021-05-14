# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/12/28 2:50 下午
@Describe 
"""

from pyecharts import Map, Geo #pyecharts==0.5.0
import pandas as pd
import  os,csv,requests

data = []
attr = []
value = []
geo_cities_coords = {}


for file in os.listdir('./tables'):
    try:
        f = csv.reader(open('./tables/'+file,'r',encoding='utf-8'))
        city = file.split('.')[0]
        count = len([i for i in f])
        location = requests.get(f'http://restapi.amap.com/v3/geocode/geo?key=488fdb9e5bac7c0291395db0180f130b&address={city}&city={city}').json()['geocodes'][0]['location'].split(',')
        data.append((city,count))
        attr.append(city)
        value.append(count)
        geo_cities_coords[city] = location
    except:pass


geo = Geo("全国主要城市航班热力图",
          "data from flightaware",
          title_color="#000",
          title_pos="left",
          width=1600,
          height=800,
          background_color='#FFFFFF')

geo.add("热力图",
        attr,
        value,
        type='heatmap',
        visual_range=[0, max(value)],
        visual_text_color="#000",
        symbol_size=15,
        is_visualmap=True,
        is_roam=False)
geo.add("地理图",
        attr,
        value,
        type="effectScatter",
        is_random=True,
        effect_scale=5,
        visual_range=[0, max(value)],
        visual_text_color="#000",
        symbol_size=15,
        is_visualmap=True,
        is_roam=False)
# geo.add("坐标图", #标题，构建坐标系的时候已经写好，不需要设置，设为空
#         attr,#城市名
#         value,#各城市的GDP
#         visual_range=[0, 1000],#可视化深浅的范围
#         visual_text_color="#fff",#标签的颜色
#         is_piecewise=True,#设置颜色分段显示
#         visual_split_number=10,#设置10个不同的组
#         symbol_size=7.5,#设置散点大小为7.5
#         is_visualmap=True,#设置颜色与value一一对应，value越高，颜色越深
#         geo_cities_coords=geo_cities_coords#设置散点所在的经纬度
#        )

geo.show_config()
geo.render(path="航班信息.html")