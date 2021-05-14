# -*- coding: utf-8 -*-
'''
@Author billie
@Date 2020/4/11 15:33
@Describe 

'''
import re
import time
from DL import *
start=time.time()

def call_me_by_your_name():
    import requests
    from lxml import etree
    url='https://movie.douban.com/subject/27192462/photos?type=R'
    r=requests.get(url,headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'})
    # print(r.text)
    tree=etree.HTML(r.text)
    hrefs=tree.xpath('//*[@id="content"]/div/div[1]/ul/li/div/a/img/@src')
    names=list(tree.xpath('//div[@class="name"]/text()'))
    name=''
    for i in names:name+=str(i)
    names=re.findall('(\w+)',name)
    for i in range(len(hrefs)):
        with open(names[i]+'.jpg','wb')as F:
            r=requests.get(hrefs[i])
            F.write(r.content)
        print(hrefs[i])
def intouchables():
    from lxml import etree
    def dl(url):
        r = requests.get(url, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'})
        # print(r.text)
        tree = etree.HTML(r.text)
        hrefs = tree.xpath('//*[@id="content"]/div/div[1]/ul/li/div[1]/a/img/@src')
        names = list(tree.xpath('//div[@class="name"]/text()'))
        name = ''
        for i in names: name += str(i)
        names = re.findall('(\w+)', name)
        for i in range(len(hrefs)):
            with open('./触不可及海报/'+names[i] + '.jpg', 'wb')as F:
                r = requests.get(hrefs[i])
                F.write(r.content)
                print(names[i],hrefs[i],r.content)
        try:
            url=tree.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href')[0]
            dl(url)
        except :pass
    base_url = 'https://movie.douban.com/subject/6786002/photos?type=R'
    dl(url=base_url)
def the_gentleman():
    from lxml import etree
    def dl(url,name):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        # 创建会话对象session
        session = requests.Session()
        #访问首页
        r1=session.get(url='https://www.douban.com/',
                    headers=headers)
        # 登录豆瓣
        r2=session.post(url='https://accounts.douban.com/j/mobile/login/basic',
                     headers=headers,
                     data={
                         'name': '17796376426',
                         'password': 'Aa1222222222',
                         'remember': 'true'},
                     cookies=r1.cookies.get_dict()
                     )
        print(r2.text)
        cookies = r1.cookies.get_dict()
        r = session.get(url=url,headers=headers,cookies=cookies)
        # print(r.text)
        tree = etree.HTML(r.text)
        hrefs = tree.xpath('//*[@id="content"]/div/div[1]/ul/li/div[1]/a/img/@src')
        for i in range(len(hrefs)):
            href = hrefs[i].replace('/m/', '/raw/')
            r = session.get(url=href,headers=headers,cookies=cookies)
            with open('./绅士们剧照/'+str(name)+ '.jpg', 'wb')as F:
                F.write(r.content)
            print(name,href,r.content)
            name += 1
        try:
            url=tree.xpath('//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href')[0]
            dl(url,name)
        except :pass
    base_url = 'https://movie.douban.com/subject/30211998/photos?type=S'
    name = 1
    dl(url=base_url,name=name)

# intouchables()
the_gentleman()
end=time.time()
m,s=divmod(round(end-start),60)
print('\n'+'[下载用时]：{} m {} s'.format(m,s))