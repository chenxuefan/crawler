# -*- coding: utf-8 -*-
"""
# Talk is cheap,show me the codes!

@Author billie
@Time 2020/7/19 9:17 下午
@Describe 

"""

import smtplib  # 发邮件
from email.mime.multipart import MIMEMultipart # 用于构建邮件对象
from email.header import Header # 用于构建邮件头
from email.mime.text import MIMEText # 用于构建内容文本
from email.mime.image import MIMEImage #
from email.mime.audio import MIMEAudio #
from email.mime.application import MIMEApplication #
import psutil,threading,schedule,time

class email():
    def __init__(self):
        # -----------------------基本信息------------------------
        # 服务器，端口
        self.host = 'smtp.qq.com'
        self.port = 465
        # 发送者，授权码（非密码）
        self.sender = '2380540710@qq.com'
        self.password = 'ghioratrikzeebbj'
        # 接收者
        self.receivers = '2380540710@qq.com'  # 添加多个账户时采用列表形式
        # 邮件内容
        self.msg = MIMEMultipart() # 构造一个MIMEMultipart对象代表邮件本身
        # ------------------------------------------------------

    def get_msg(self,new_dy,att_file_path=None,att_file_name=None):

        # 构建邮件头
        self.msg['From'] = Header('人人都爱小雀斑','utf-8')  # 发件人的名称或地址
        self.msg['To'] = Header('billie','utf-8')  # 发件人邮箱地址
        self.msg['Subject'] = Header('电影天堂最新电影资源','utf-8')  # 主题

        # 1、邮件文本内容
        '''
        构建文本：MIMEText(_text=text, _subtype='plain', _charset='utf-8')
        '''
        # 1.1、发送内容为字符串文本
        text = ''
        # 构建纯文本的邮件内容，plain代表纯文本11
        string_of_email = MIMEText(_text=text, _subtype='plain', _charset='utf-8')#内容，内容类型，编码

        # 1.2、发送内容为html格式
        html = ''
        for title,href in new_dy.items():
            html += f"<ul><li>{title}</li><li><a href='{href}'>{href}</a></li></ul>"
        html = "<table>" + html + "</table>"


        html_of_email = MIMEText(html,'html','utf-8')

        # 添加内容文本到邮件
        self.msg.attach(html_of_email)




    def send_email(self):
        # ----------------------登录并发送------------------------
        try:
            # 开启发信服务
            server = smtplib.SMTP_SSL(self.host)
            # 连接服务与端口
            server.connect(self.host, self.port)
            # 登录发信邮箱
            server.login(self.sender, self.password)
            # 发送邮件（发信人，接收者，邮件内容）
            server.sendmail(from_addr=self.sender,
                            to_addrs=self.receivers,
                            msg=self.msg.as_string())
            # 关闭服务器
            server.quit()
            # 设定间隔时间发送
            # threading.Timer(1000,send_email).start()
        except smtplib.SMTPException as e:
            print(e)
    def send(self,new_dy):
        self.get_msg(new_dy)
        self.send_email()


