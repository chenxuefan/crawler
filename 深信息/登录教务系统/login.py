# -*- coding=utf-8 -*-
import json
import requests
import time
from lxml import etree
from hex2b64 import HB64
import RSAJS

class Longin():
    def __init__(self, user, password,base_url, login_url, login_KeyUrl):    # 初始化数据
        self.Username = user
        self.Password = password
        nowTime = lambda:str(round(time.time() * 1000))
        self.now_time = nowTime()
        self.base_url=base_url
        self.login_url = login_url
        self.login_Key = login_KeyUrl

    def Get_indexHtml(self):    # 获取教务系统网站
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Referer": self.login_url + self.now_time,
            "Upgrade-Insecure-Requests": "1"
        })
        self.response = self.session.get(self.login_url + self.now_time).content.decode("utf-8")

    def Get_csrftoken(self):    # 获取 csrftoken
        lxml = etree.HTML(self.response)
        self.csrftoken = lxml.xpath("//input[@id='csrftoken']/@value")[0]

    def Get_PublicKey(self):    # 获取公钥参数
        key_html = self.session.get(self.login_Key + self.now_time)
        key_data = json.loads(key_html.text)
        # print(self.login_Key + self.now_time)
        self.modulus = key_data["modulus"]
        self.exponent = key_data["exponent"]

    def Get_RSA_Password(self): # 生成公钥进行加密
        rsaKey = RSAJS.RSAKey()
        rsaKey.setPublic(HB64().b642hex(self.modulus), HB64().b642hex(self.exponent))
        self.enPassword = HB64().hex2b64(rsaKey.encrypt(self.Password))
        
    def Longin_Home(self):  # post 登录, 返回 session 对象
        self.Get_indexHtml()
        self.Get_csrftoken()
        self.Get_PublicKey()
        self.Get_RSA_Password()

        login_data = [("csrftoken", self.csrftoken), ("yhm", self.Username), ("mm", self.enPassword),("mm", self.enPassword)]
        login_html = self.session.post(self.login_url + self.now_time, data=login_data)
        if login_html.url.find("login_slogin.html") == -1:  # 根据 url 是否跳转判断是否登录成功
            print("Login success...")


if __name__ == "__main__":
    base_url = "http://xjwgl2020.frp.sziitjx.cn:8080"
    login_url = base_url + "/xtgl/login_slogin.html?language=zh_CN&_t="  # 登录主页 url
    login_KeyUrl = base_url+"/xtgl/login_getPublicKey.html?time="  # 获取公钥参数的 url
    # login = Longin(name.GetValue(), passwd.GetValue(), login_url, login_KeyUrl,win)
    # 创建类实例对象
    billie = Longin('1801010507', "a122222222",base_url, login_url, login_KeyUrl)
    response_cookies = billie.Longin_Home()
