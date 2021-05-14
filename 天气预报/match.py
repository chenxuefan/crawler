'''
@author: 人人都爱小雀斑
@time: 2020/3/6 16:03
@desc:
'''
import re
import pandas as pd
fobj=open("城市代码.txt","rt",encoding="utf-8")
city=re.findall("[\u4E00-\u9FA5]+",fobj.read())
fobj=open("城市代码.txt","rt",encoding="utf-8")
code=re.findall("(\d+)",fobj.read())
cityDic=dict()
for c in city:
    for o in code:
        cityDic[c]=o
for i in cityDic:
    print(i,cityDic[i])
print()
df=pd.DataFrame(data=code,index=city)
df.to_csv("城市代码.csv",sep=",",encoding="utf-8")


