# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/12/31 4:02 下午
@Describe 
"""

from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts.globals import ChartType,SymbolType
import os,csv

data = []
for file in os.listdir('./tables'):
    try:
        f = csv.reader(open('./tables/'+file,'r',encoding='utf-8'))
        city = file.split('.')[0]
        count = len([i for i in f])
        # location = requests.get(f'http://restapi.amap.com/v3/geocode/geo?key=488fdb9e5bac7c0291395db0180f130b&address={city}&city={city}').json()['geocodes'][0]['location'].split(',')
        data.append([city,count])
    except:pass

c = (
    Geo()
    .add_schema(maptype="china",
                layout_center=['80%','40%'],
                min_scale_limit=1,
                max_scale_limit=2,
                layout_size=0,
                itemstyle_opts=opts.ItemStyleOpts(color="#323c48", border_color="#111"))
    .add(
        "热力图",
        data,
        type_=ChartType.HEATMAP,
        effect_opts=opts.EffectOpts(symbol=SymbolType.ARROW, symbol_size=6, color="blue")
    )
    .add(
        "涟漪散点图",
        data,
        type_=ChartType.EFFECT_SCATTER,
    )
    # .set_global_opts(title_opts=opts.TitleOpts(title="Geo-EffectScatter"))
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(max_=10000),
        title_opts={"text":"全国主要城市航班信息图","subtext":"Data from flightaware.com"}
    )
)

c.width = '1800px'
c.height = '800px'
c.render('航班信息.html')
