# -*- coding: utf-8 -*-
"""
# Talk is cheap,show me the codes!

@Author billie
@Time 2020/8/14 12:33 上午
@Describe 

"""
def douban_cqc():
    import requests
    import logging
    import json
    from os import makedirs
    from os.path import exists

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s')

    INDEX_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/movie/?limit={limit}&offset={offset}'
    DETAIL_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/movie/{id}'
    LIMIT = 10
    TOTAL_PAGE = 10
    RESULTS_DIR = 'results'
    exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

    def scrape_api(url):
        logging.info('scraping %s...', url)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            logging.error('get invalid status code %s while scraping %s', response.status_code, url)
        except requests.RequestException:
            logging.error('error occurred while scraping %s', url, exc_info=True)

    def scrape_index(page):
        url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
        return scrape_api(url)

    def scrape_detail(id):
        url = DETAIL_URL.format(id=id)
        return scrape_api(url)

    def save_data(data):
        name = data.get('name')
        data_path = f'{RESULTS_DIR}/{name}.json'
        json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    def main():
        #
        import pymongo
        client = pymongo.MongoClient(host='localhost',port=27017)
        db = client['movie'] #指定操作其中一个数据库
        collection  = db['movies'] #指定一个集合，声明一个 Collection 对象
        #
        for page in range(1, TOTAL_PAGE + 1):
            index_data = scrape_index(page)
            for item in index_data.get('results'):
                id = item.get('id')
                detail_data = scrape_detail(id)
                collection.insert(dict(detail_data))
                logging.info('detail data %s', detail_data)
                save_data(detail_data)

    if __name__ == '__main__':
        main()

douban_cqc()