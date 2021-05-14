# NCP | 爬取国家卫健委网站

## 1. 前言 🇨🇳

### 1.1 目标网站

「[http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml](http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml)」

​	做疫情这个项目的时候，第一个要解决的就是数据来源的问题，想到的最权威的网站就是国家卫生健康委员会的网站了，一开始用requests尝试，失败了，接着用上了selenium模拟网页访问，顺利拿到了数据。

### 1.2 技术栈

python - selenium、pandas、re、echarts、matplotlib

## 2. 项目流程 🚗

### 🐛 数据获取 - selenium

使用谷歌浏览器时挂了，火狐就可以；爬取思路是访问每一天的详情页，接着用元素定位的方法，去获得页面中包含疫情数据的文本。

![image-20201129141538448](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/image-20201129141538448.png)

### 🌲 文本解析 - re

爬取到的数据是文本形式的，因此我用了效率比较高的正则表达式，去从文本中提取数据

![image-20201129141228670](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/image-20201129141228670.png)

### 📈 图表制作 - echarts、matplotlib

趋势图的制作分两种风格，尽力做到最好看。

![chart_echart](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/chart_plt.png)/*matplotlib绘制*/

![chart_echart](https://billie-s-album.oss-cn-beijing.aliyuncs.com/img/chart_echart.png)/*echarts绘制*/

