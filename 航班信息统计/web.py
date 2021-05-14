# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/12/31 5:36 上午
@Describe 
"""

from flask import Flask
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/city/')
def hello():
    with open('./city.json','r') as f:
        print(f.read())
        jsonStr = json.load(f)
        return json.dumps(jsonStr)



if __name__ == '__main__':
    app.run()