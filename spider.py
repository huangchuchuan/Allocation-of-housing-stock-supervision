# -*- coding: utf-8 -*-

import os
import sys
import requests
reload(sys)
sys.setdefaultencoding('utf-8')


class HousingStockSpider():
    BASE_URL = 'http://www.tjfdc.com.cn/pages/xwzw/clfbfqk.aspx?SelMnu=CLFBFQK&fid='
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database')
    DATABASE_FILE = os.path.join(DATABASE_PATH, 'record.txt')
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.ini')
    DATA_FILE = os.path.join(os.path.dirname(__file__), 'total_data.csv')
    default_headers = {
        'Host': 'www.tjfdc.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://www.tjfdc.com.cn/Pages/xwzw.aspx',
    }
    default_query_dict = {

    }
    default_config_dict = {

    }

    def __init__(self):
        if not os.path.exists(HousingStockSpider.DATABASE_PATH):
            print u'正在创建数据库文件夹...'
        if not os.path.exists(HousingStockSpider.DATA_PATH):
            print u'正在创建数据文件夹...'
        self.session = requests.Session()
        self.session.headers.update(HousingStockSpider.default_headers)
        resp = self.session.get(HousingStockSpider.BASE_URL)
        if resp.status_code != 200:
            print u'爬虫失效, 请联系作者'
            print resp.content
            self.session = None
        else:
            print u'初始化成功'
            print resp.content
            print resp.cookies
            cookie_dict = resp.cookies.get_dict()
            cookie_list = []
            for key, value in cookie_dict.iteritems():
                cookie_list.append('%s=%s' % (key, value))
            cookie_str = ';'.join(cookie_list)
            self.session.headers.update({'Cookie': cookie_str})


if __name__ == '__main__':
    spider = HousingStockSpider()
