# -*- coding: utf-8 -*-
'''
@Author billie
@Date 2020/4/11 9:48
@Describe 

'''
import requests,re
from lxml import etree
from bs4 import BeautifulSoup
def spider():
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    r=requests.get('https://www.worldometers.info/coronavirus/',headers=headers)
    r.encoding='utf-8'
    tree=etree.HTML(r.text)
    ths=tree.xpath('//*[@id="main_table_countries_today"]/thead/tr/th/text()')
    ths=[ths[i]+' '+ths[i+1] for i in range(0,16,2)]
    print(ths)
    trs=tree.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr[8]/td/text()')
    print(trs[:8])
    tplt = "{0:<10}\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\t{5:<10}\t{6:<10}\t{7:<10}"
    for i in ths:print(i,end='  ')
    print('\n')
    for i in trs:print(i,end='  ')

spider()

