# -*- coding: utf-8 -*-
"""
@Author billie
@Date 2020/12/28 2:49 下午
@Describe 
"""
from spider import Flight
from multiprocessing import Process,Pool
import time
# b = Flight(city='上海')
# print(b.cityCode)
# b.mainWork()
if __name__ == '__main__':
    begin_time = time.time()

    cityPool = ['深圳','广州','珠海','香港','澳门','北京','上海','南京','无锡','常州'] # 待爬取的城市
    p = Pool() # 进程池
    for city in cityPool:
        billie = Flight(city=city)
        p.apply_async(func=billie.mainWork)
    p.close()
    p.join()

    end_time = time.time()
    time = end_time - begin_time
    m, s = divmod(round(time), 60)
    print("用时：{}min{}s".format(m, s))