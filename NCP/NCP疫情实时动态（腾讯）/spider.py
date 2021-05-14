'''
@author: 人人都爱小雀斑
@time: 2020/2/26 16:58
@desc: 爬取数据的四个方法
'''

import json
import requests
import selenium.webdriver
from selenium.webdriver.chrome.options import Options

class spider():
    def __init__(self):
        self.base_url = "https://news.qq.com/zt2020/page/feiyan.htm"
        self.lastUpdateTime = 0  # 数据截至时间
        self.confirm = 0  # 确诊
        self.confirm_add = 0  # 新增确诊
        self.suspect = 0  # 疑似
        self.heal = 0  # 治愈
        self.dead = 0  # 死亡
        self.nowConfirm = 0  # 现有确诊
        self.nowSevere = 0  # 现有重症
        self.dataDic = dict()  # 键为省名，值为省的具体数据

    def spider1(self, url):  # 此方法已失效
        global timeNum, provinceDic
        # 无窗口弹出操作
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = selenium.webdriver.Chrome(options=options)
        driver.get(url)
        timeNum = driver.find_element_by_xpath('//*[@id="charts"]/div[2]/span[1]').text  # 实时
        icbar_confirm = driver.find_element_by_xpath('//*[@id="charts"]/div[3]/div[1]/div[1]').text  # 全国确诊数
        icbar_suspect = driver.find_element_by_xpath('//*[@id="charts"]/div[3]/div[2]/div[1]').text  # 疑似病例数
        icbar_cure = driver.find_element_by_xpath('//*[@id="charts"]/div[3]/div[3]/div[1]').text  # 治愈人数
        icbar_dead = driver.find_element_by_xpath('//*[@id="charts"]/div[3]/div[4]/div[1]').text  # 死亡人数
        print("{}\n全国确诊：{}\n疑似病例：{}\n治愈人数：{}\n死亡人数：{}\n".format(timeNum, icbar_confirm, icbar_cure, icbar_dead,
                                                                icbar_suspect))
        place_current = driver.find_elements_by_css_selector('div[class="place  current"]')  # 湖北省的数据
        place = driver.find_elements_by_css_selector('div[class="place"]')  # 其他省的数据
        place_ = driver.find_elements_by_css_selector('div[class="place  "]')  # 其他省的数据
        place_no_sharp = driver.find_elements_by_css_selector("div[class='place no-sharp ']")  # 自治区的数据
        tplt = "{0:{4}<10}\t{1:{4}<15}\t{2:{4}<15}\t{3:{4}<15}"
        print(tplt.format("地区", "确诊人数", "治愈人数", "死亡人数", chr(12288)) + "\n")
        # 建立一个字典，键为省名，值为省的具体数据
        provinceDic = dict()
        provinceDic["全国"] = ["全国", icbar_confirm, icbar_cure, icbar_dead, icbar_suspect]
        places = place_current + place + place_ + place_no_sharp  # 所有的行省的数据列表合集
        for place in places:
            # print(place.text)
            name = place.find_element_by_css_selector("span[class='infoName']").text
            confirm = place.find_element_by_css_selector("span[class='confirm'] span").text
            try:
                heal = place.find_element_by_css_selector("span[class='heal '] span").text
            except:
                heal = place.find_element_by_css_selector("span[class='heal hide'] span").text
            try:
                dead = place.find_element_by_css_selector("span[class='dead '] span").text
            except:
                dead = place.find_element_by_css_selector("span[class='dead hide'] span").text
            print(tplt.format(name, confirm, heal, dead, chr(12288)))
            provinceDic[name] = [name, confirm, heal, dead]
            # 建立一个字典，键为城市名，值为城市的具体数据
            # citiesDic=dict()
            # citiesDic[name]=[name,confirm,heal,dead]
            # cities=place.find_elements_by_css_selector("div[area={0}]".format(name))
            # for city in cities:#此省的每一个城市
            #     print(city.text)
            #     spans=city.find_elements_by_css_selector("span")
            #     i=0
            #     for span in spans:
            #         # print(i,span.text)
            #         i+=1
            #     name = spans[0].text
            #     confirm = spans[1].text
            #     try:
            #         heal = spans[3].text
            #     except:
            #         heal = spans[3].text
            #     try:
            #         dead = spans[5].text
            #     except:
            #         dead = spans[5].text
            #     citiesDic[name]=[name,confirm,heal,dead]
            #     print(name, confirm, heal, dead)

    def spider2(self, url):  # 1/29目标网页已改变，此方法已失效
        global timeNum, provinceDic
        # 无窗口弹出操作
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = selenium.webdriver.Chrome(options=options)
        driver.get(url)
        timeNum = driver.find_element_by_css_selector("div[class='timeNum'] p[class='d']").text  # 实时
        icbar_confirm = driver.find_element_by_css_selector(
            "div[class='icbar confirm'] div[class='number']").text  # 全国确诊数
        icbar_suspect = driver.find_element_by_css_selector(
            "div[class='icbar suspect'] div[class='number']").text  # 疑似病例数
        icbar_cure = driver.find_element_by_css_selector("div[class='icbar cure'] div[class='number']").text  # 治愈人数
        icbar_dead = driver.find_element_by_css_selector("div[class='icbar dead'] div[class='number']").text  # 死亡人数
        print("\n{}\n全国确诊：{}\n疑似病例：{}\n治愈人数：{}\n死亡人数：{}\n".format(timeNum, icbar_confirm, icbar_suspect, icbar_cure,
                                                                  icbar_dead))
        placeItemWrap = driver.find_elements_by_css_selector('div[class="placeItemWrap current"]')  # 湖北省的数据
        placeItemWrap_ = driver.find_elements_by_css_selector('div[class="placeItemWrap "]')  # 其他省的数据
        abroad = driver.find_elements_by_css_selector(
            'div[class="clearfix placeItem placeArea no-sharp abroad"]')  # 海外国家的数据
        tplt = "{1:{0}<10}\t{2:{0}<15}\t{3:{0}<15}\t{4:{0}<15}\t{5:{0}<15}"
        print(tplt.format(chr(12288), "地区", "新增确诊", "确诊人数", "治愈人数", "死亡人数", ))
        # 建立一个字典，键为省名，值为省的具体数据
        provinceDic = dict()
        places = placeItemWrap + placeItemWrap_ + abroad  # 所有的地区的数据列表合集
        national_confirm = 0  # 全国新增确诊
        for place in places:
            # print(place.text)
            try:  # 国内地区
                name = place.find_element_by_css_selector("h2[class='blue']").text
            except:  # 海外地区
                try:
                    name = place.find_element_by_css_selector("h2[class='blue ']").text
                except:
                    name = place.find_element_by_css_selector("h2[class='blue small']").text
            try:  # 国内新增确诊
                add = place.find_element_by_css_selector("div[class='add ac_add']").text
            except:
                add = 0
            try:  # 国内累计确诊
                confirm = place.find_element_by_css_selector("div[class='confirm']").text
            except:  # 海外累计确诊
                confirm = place.find_elements_by_css_selector("div")[0].text
            try:  # 国内治愈
                heal = place.find_element_by_css_selector("div[class='heal']").text
            except:  # 海外累计治愈
                heal = place.find_elements_by_css_selector("div")[1].text
            try:  # 国内死亡
                dead = place.find_element_by_css_selector("div[class='dead']").text
            except:  # 海外死亡
                dead = place.find_elements_by_css_selector("div")[2].text
            print(tplt.format(chr(12288), name, add, confirm, heal, dead, ))
            provinceDic[name] = [name, confirm, heal, dead, add]
            try:  # 计算全国新增确诊数
                national_confirm += int(add)
            except:  # 数据项为"-"，则跳过
                pass
        provinceDic["全国"] = ["全国", icbar_confirm, icbar_cure, icbar_dead, national_confirm, icbar_suspect]

    def spider3(self):  # 2/1 2/16目标网页已改变;selenium方法
        # 无窗口弹出操作
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = selenium.webdriver.Chrome(options=options)
        driver.get(self.base_url)
        self.lastUpdateTime = driver.find_element_by_xpath('//*[@id="charts"]/div[2]/div[2]/div/p').text[
                              4:23]  # 实时#2020-02-18 07:22:53
        self.confirm = driver.find_element_by_xpath('//*[@id="charts"]/div[2]/div[3]/div[1]/div[2]').text  # 全国确诊数
        self.confirm_add = driver.find_element_by_xpath(
            '//*[@id="charts"]/div[2]/div[3]/div[1]/div[1]/span').text  # 全国确诊数add
        self.suspect = driver.find_element_by_xpath('//*[@id="charts"]/div[2]/div[4]/div[2]/div[2]').text  # 疑似病例数
        self.suspect_add = driver.find_element_by_xpath(
            '//*[@id="charts"]/div[2]/div[4]/div[2]/div[1]/span').text  # 疑似病例数add
        self.heal = driver.find_element_by_xpath('//*[@id="charts"]/div[2]/div[3]/div[2]/div[2]').text  # 治愈人数
        self.heal_add = driver.find_element_by_xpath(
            '//*[@id="charts"]/div[2]/div[3]/div[2]/div[1]/span').text  # 治愈人数add
        self.dead = driver.find_element_by_xpath('//*[@id="charts"]/div[2]/div[3]/div[3]/div[2]').text  # 死亡人数
        self.dead_add = driver.find_element_by_xpath(
            '//*[@id="charts"]/div[2]/div[3]/div[3]/div[1]/span').text  # 死亡人数add
        self.nowConfirm = driver.find_element_by_xpath('//*[@id="charts"]/div[2]/div[4]/div[1]/div[2]').text  # 现有确诊
        self.nowConfirm_add = driver.find_element_by_xpath(
            '//*[@id="charts"]/div[2]/div[4]/div[1]/div[1]/span').text  # 现有确诊add
        self.nowSevere = driver.find_element_by_xpath('//*[@id="charts"]/div[2]/div[4]/div[3]/div[2]').text  # 现有重症
        self.nowSevere_add = driver.find_element_by_xpath(
            '//*[@id="charts"]/div[2]/div[4]/div[3]/div[1]/span').text  # 现有重症add
        self.dataDic["全国"] = ["全国", self.confirm, self.heal, self.dead, self.confirm_add.strip("+"), self.suspect,
                              self.nowConfirm, self.nowSevere]
        hubei = driver.find_elements_by_css_selector('div[class="placeItemWrap current"]')  # 湖北省的数据集
        wuhan = driver.find_elements_by_css_selector("div[city='武汉']")  # 武汉市的数据集
        elprovince = driver.find_elements_by_css_selector('div[class="placeItemWrap"]')  # 其他省的数据集
        abroad = driver.find_elements_by_css_selector(
            'div[class="clearfix placeItem placeArea no-sharp abroad"]')  # 海外国家的数据集
        # tplt = "{1:{0}<10}\t{2:{0}<15}\t{3:{0}<15}\t{4:{0}<15}\t{5:{0}<15}"
        # print(tplt.format(chr(12288),"地区","新增确诊","累计确诊","治愈","死亡",))
        places = hubei + wuhan + elprovince + abroad  # 所有的地区的数据列表合集
        for p in places:  # 查找目标，name\add\confirm\heal\dead
            place = p.find_element_by_css_selector("h2").text  # 湖北/武汉/国内/海外地区
            try:
                add = p.find_element_by_css_selector("div[class='add ac_add ']").text  # 国内新增确诊
            except:
                if place == "武汉":
                    add = p.find_element_by_css_selector("div[class='ac_add ']").text  # 武汉地区新增确诊
                else:
                    add = 0  # 海外地区无数据
            try:
                confirm = p.find_element_by_css_selector("div[class='confirm']").text  # 国内累计确诊
            except:
                if place == "武汉":
                    confirm = p.find_elements_by_css_selector("div")[1].text  # 武汉累计
                else:
                    confirm = p.find_elements_by_css_selector("div")[0].text  # 海外累计确诊
            try:
                heal = p.find_element_by_css_selector("div[class='heal']").text  # 国内治愈人数
            except:
                if place == "武汉":
                    heal = p.find_elements_by_css_selector("div")[2].text  # 武汉治愈人数
                else:
                    heal = p.find_elements_by_css_selector("div")[1].text  # 海外治愈
            try:
                dead = p.find_element_by_css_selector("div[class='dead']").text  # 国内死亡
            except:
                if place == "武汉":
                    dead = p.find_elements_by_css_selector("div")[3].text  # 武汉死亡人数
                else:
                    dead = p.find_elements_by_css_selector("div")[2].text  # 海外死亡人数
            # print(tplt.format(chr(12288),place,add,confirm,heal,dead,))
            self.dataDic[place] = [place, confirm, heal, dead, add]  # 向字典添加数据

    def spider4(self):  # requests方法
        self.url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        r = requests.get(self.url, headers)
        res = json.loads(r.text)
        data_res = json.loads(res['data'])
        self.lastUpdateTime = data_res['lastUpdateTime']
        self.confirm = data_res['chinaTotal']['confirm']
        self.suspect = data_res['chinaTotal']['suspect']
        self.heal = data_res['chinaTotal']['heal']
        self.dead = data_res['chinaTotal']['dead']
        self.nowConfirm = data_res['chinaTotal']['nowConfirm']
        self.nowSevere = data_res['chinaTotal']['nowSevere']
        # 较昨日新增
        self.confirm_add = data_res['chinaAdd']['confirm']
        self.suspect_add = data_res['chinaAdd']['suspect']
        self.dead_add = data_res['chinaAdd']['dead']
        self.heal_add = data_res['chinaAdd']['heal']
        self.nowConfirm_add = data_res['chinaAdd']['nowConfirm']
        self.nowSevere_add = data_res['chinaAdd']['nowSevere']
        # 各个国家的数据字典，键为国家名称，值为四项数据
        countryDic = dict()
        for coutry in data_res['areaTree'][1:]:
            countryDic[coutry['name']] = \
                [coutry['name'],
                 coutry['total']['confirm'],
                 coutry['total']['heal'],
                 coutry['total']['dead']]
        # 中国各个省份的数据字典
        chinaDic = dict()
        chinaDic['中国'] = ['全国', self.confirm, self.heal, self.dead, self.confirm_add, self.suspect, self.nowConfirm,
                          self.nowSevere]
        # 中国所有城市的数据字典
        cityDic = dict()
        for province in data_res['areaTree'][0]['children']:
            # print(province)
            chinaDic[province['name']] = \
                [province['name'],
                 province['total']['confirm'],
                 province['total']['heal'],
                 province['total']['dead']]
            for city in province['children']:
                cityDic[city['name']] = \
                    [city['name'],
                     city['total']['confirm'],
                     city['total']['heal'],
                     city['total']['dead']]
        self.dataDic = {**chinaDic, **countryDic}  # 合并 国家数据集,国内省份数据集
        # 打印当前全国疫情
        print("\n截至{}\n累计确诊：{} {}\n现有疑似：{} {}\n累计治愈：{} {}\n累计死亡：{} {}\n现有确诊：{} {}\n现有重症：{} {}\n"
              .format(self.lastUpdateTime, self.confirm, self.confirm_add, self.suspect, self.suspect_add,
                      self.heal,
                      self.heal_add, self.dead, self.dead_add, self.nowConfirm, self.nowConfirm_add, self.nowSevere,
                      self.nowSevere_add))

    def spider_china(self):  # &callback=jQuery34108082893312274555_1581931200655&_=1581931200656
        global ChinaDic, chinaDic
        url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        r = requests.get(url, headers)
        res = json.loads(r.text)
        data_res = json.loads(res['data'])
        lastUpdateTime = data_res['lastUpdateTime']
        confirm = data_res['chinaTotal']['confirm']
        suspect = data_res['chinaTotal']['suspect']
        heal = data_res['chinaTotal']['heal']
        dead = data_res['chinaTotal']['dead']
        nowConfirm = data_res['chinaTotal']['nowConfirm']
        nowSevere = data_res['chinaTotal']['nowSevere']

        confirm_add = data_res['chinaAdd']['confirm']
        suspect_add = data_res['chinaAdd']['suspect']
        dead_add = data_res['chinaAdd']['dead']
        heal_add = data_res['chinaAdd']['heal']
        nowConfirm_add = data_res['chinaAdd']['nowConfirm']
        nowSevere_add = data_res['chinaAdd']['nowSevere']

        # 已不再更新
        # 各个国家的数据字典，键为国家名称，值为四项数据
        # countryDic = dict()
        # for coutry in data_res['areaTree'][1:]:
        #     countryDic[coutry['name']] = \
        #         [coutry['total']['confirm'],
        #          coutry['total']['heal'],
        #          coutry['total']['dead']]

        # 中国各个省份的数据字典
        chinaDic = dict()
        chinaDic['中国'] = [confirm, heal, dead, confirm_add, suspect, nowConfirm, nowSevere]
        # 中国所有城市的数据字典
        cityDic = dict()
        for province in data_res['areaTree'][0]['children']:
            # print(province)
            chinaDic[province['name']] = \
                [province['total']['confirm'],
                 province['total']['heal'],
                 province['total']['dead']]
            for city in province['children']:
                cityDic[city['name']] = \
                    [city['total']['confirm'],
                     city['total']['heal'],
                     city['total']['dead']]
        ChinaDic = {**chinaDic, **cityDic}
