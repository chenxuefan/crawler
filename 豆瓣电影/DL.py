# -*- coding: utf-8 -*-
'''
@Author billie
@Date 2020/3/18 15:11
@Describe 

'''
import requests,time,threading,datetime
def download(path,name,type,href):#
    print("[正在下载]：{}".format(name))
    size=0
    r=requests.get(href,stream=True,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'})
    chunk_size=1024#每次下载的数据大小
    content_size=int(r.headers['content-length'])#总大小
    # print(content_size,r.status_code,r.content,r.text)
    # if r.status_code == 200:
    print("[文件大小]：{:.2f} MB".format(content_size / chunk_size / 1024))#换算单位
    with open(path+'/'+name+'.'+type, "wb")as f:
            for data in r.iter_content(chunk_size=chunk_size):
                f.write(data)
                size += len(data)#已下载文件大小
                print('\r'+'[下载进度]：{} {:.1f}%'.format('>'*int(size*50/ content_size),float(size / content_size * 100)),end='')
def download2(name,url):#极简模式
    import requests
    r=requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'})
    print(r.content)
    with open(name,"wb") as f:
        f.write(r.content)
#Linux基础和操作系统基础
# for i in range(1,63):
#      download(path='Linux基础和操作系统基础',name=str(i),type='jpg',href='https://file.icve.com.cn/ssykt_gen/554/958/8A9EF99DE29E03E18A3BAA9E76352F6C.pdf/{}.png'.format(i))

#用户、权限与系统管理,Sheel脚本语言
# for i in range(39,46):
#     download(path='./Sheel脚本语言',name=str(i),type='png',href='https://file.icve.com.cn/ssykt_gen/379/80/5EE143BCF92C82BF4DE97E35FA53EEEF.pdf/{}.png'.format(str(i)))
#DNS处理模块
# for i in range(1,20):
#     download(path='配置DNS服务器',name=str(i),type='jpg',href='https://file.icve.com.cn/ssykt_gen/389/513/61480484D2AE3B773D8B4C39E6513E34.pptx/{}.png'.format(i))
#qq音乐
# download(path='.',name='i like it',type='mp4',href='https://isure.stream.qqmusic.qq.com/C400000hlg0X2gpXOX.m4a?guid=2331319800&vkey=E97D0A0F74ABE2241B283957E5B179EC647C6CFAAF2E2358CFF5CE24B8667BF7394250CAA60061839B9301DB2A706BB57FB72DC138781298&uin=2854&fromtag=66')
#linux文件与磁盘管理
# for i in range(1,50):
#     download(path='linux文件与磁盘管理',name=str(i),type='png',href='https://file.icve.com.cn/ssykt_gen/539/1008/86EFC25385255B7C363237524AC5D837.pdf/{}.png'.format(i))

#喜马拉雅
# api_url='https://www.ximalaya.com/revision/play/v1/audio?id=266533503&ptype=1'
# r=requests.get(api_url)
# print(r.content)
#自动化运维课件
# for i in range(1,15):d
#     download(path='IP地址处理模块安装与测试',name=str(i),type='jpg',href='https://file.icve.com.cn/ssykt_gen/945/387/EC460EC05FEBC763FC9D7BDF1D710AFF.pptx/{}.png'.format(i))
#调用模块
###


#https://isure.stream.qqmusic.qq.com/C400004J8zLx2gJV0i.m4a?guid=2331319800&vkey=8886AE52EA515207E537C5F40D0A9A6A5F720D4491642D90D647C8F536C4EC116161155AF6723D879BFB0DE6873E90C817A6EEECD378F274&uin=2854&fromtag=66
#https://y.qq.com/n/yqq/song/004J8zLx2gJV0i.html