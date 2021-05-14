# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/12/3 7:52 下午
@Describe 
"""

import requests
import websocket
import json
import cv2 as cv
import numpy as np

userinfo = {}
session = requests.session()

def on_message(ws, message):
    global userinfo
    userinfo = json.loads(message)
    if 'subscribe_status' in userinfo:
        ws.close()
        return
    req = session.get(userinfo['ticket'])
    cv.namedWindow('input_image', cv.WINDOW_AUTOSIZE)
    cv.imshow('input_image', cv.imdecode(np.array(bytearray(req.content), dtype='uint8'), cv.IMREAD_UNCHANGED))
    cv.waitKey(0)
    cv.destroyAllWindows()
def on_error(ws, error):
    print(error)
def on_open(ws):
    ws.send(data=json.dumps({"op":"requestlogin","role":"web","version":1.4,"type":"qrcode","from":"web"}))
    print("open")

# websocket数据交互
ws = websocket.WebSocketApp("wss://www.yuketang.cn/wsapp/",
                                on_message = on_message,
                                on_error = on_error)
ws.on_open = on_open
ws.run_forever()

# 登录
req = session.get("https://www.yuketang.cn/v/course_meta/user_info")
session.post("https://www.yuketang.cn/pc/web_login",data=json.dumps({'UserID':userinfo['UserID'],'Auth':userinfo['Auth']}))

# 获取自己的课程列表
req = session.get("https://www.yuketang.cn/v2/api/web/courses/list?identity=2")
print(json.loads(req.content))