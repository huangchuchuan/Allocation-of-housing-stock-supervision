# -*- coding: utf-8 -*-

import os
import sys
import requests
import datetime
import traceback
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')


class HousingStockSpider():
    BASE_URL = 'http://www.tjfdc.com.cn/pages/xwzw/clfbfqk.aspx?SelMnu=CLFBFQK&fid='
    AJAX_URL = 'http://www.tjfdc.com.cn/pages/xwzw/Data/clfbfqkHandler.ashx'
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.ini')
    DATA_FILE = os.path.join(os.path.dirname(__file__), 'total_data.csv')
    default_headers = {
        'Host': 'www.tjfdc.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://www.tjfdc.com.cn/Pages/xwzw.aspx',
    }
    ajax_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Host': 'www.tjfdc.com.cn',
        'Origin': 'http://www.tjfdc.com.cn',
        'Referer': 'http://www.tjfdc.com.cn/pages/xwzw/clfbfqk.aspx?SelMnu=CLFBFQK',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    default_query_dict = {
        'selmnu': 'CLFBFQK',
        'rows': 1,
        'dt': u'Wed May 03 2017 22:56:04 GMT 0800 (中国标准时间)',
        'gRow_': 20,
        'gPage_': 1,
        'txtDate': '2017-05-03',
    }
    default_config_dict = {
        'start_date': '1967-01-01',
    }

    def __init__(self):
        if not os.path.exists(HousingStockSpider.DATA_PATH):
            print u'正在创建数据文件夹...'
            os.mkdir(HousingStockSpider.DATA_PATH)
        try:
            resp = requests.get(HousingStockSpider.BASE_URL)
            if resp.status_code == 200:
                print u'初始化成功'
        except:
            traceback.print_exc()
            print u'初始化失败，请截图联系作者'

    def get_data_by_date(self, date_str):
        # 初始化参数
        gPage_ = 1
        gRow_ = 20
        current_dt = datetime.datetime.now()
        dt = current_dt.strftime(u'%a %b %d %Y %H:%M:%S GMT 0800 (中国标准时间)')
        txtDate = date_str
        HousingStockSpider.default_query_dict['gPage_'] = gPage_
        HousingStockSpider.default_query_dict['gRow_'] = gRow_
        HousingStockSpider.default_query_dict['dt'] = dt
        HousingStockSpider.default_query_dict['txtDate'] = txtDate
        rows_list = []
        try:
            # 获取数据总量
            resp = requests.get(url=HousingStockSpider.AJAX_URL, params=HousingStockSpider.default_query_dict)
            json_data = resp.json()
            total = json_data['total']  # "rows": [{ "ID": "1","cell": ["1","32470-001978","宝坻区宝鑫景苑东湖园1-2-10"]},]
            HousingStockSpider.default_query_dict['gRow_'] = total  # 更换请求的数据量为最大值，加快速度
            # 获取所有数据
            resp = requests.get(url=HousingStockSpider.AJAX_URL, params=HousingStockSpider.default_query_dict)
            json_data = resp.json()
            rows = json_data['rows']
            for row in rows:
                items = list()
                items.append(date_str)
                items.append(row['cell'][1])
                items.append(row['cell'][2])
                rows_list.append(items)
            print u'成功抓取{}的数据，共{}条，成功{}条'.format(date_str, total, len(rows_list))
        except:
            traceback.print_exc()
            print u'抓取失败，请截图联系作者'
        return rows_list

    def auto_fetch(self):
        # 检查配置文件
        if not os.path.exists(HousingStockSpider.CONFIG_FILE):
            print u'正在重新生成配置文件...'
            with open(HousingStockSpider.CONFIG_FILE, 'w') as f:
                f.write('[default]'+os.linesep)
                for key, value in HousingStockSpider.default_config_dict.iteritems():
                    f.write(('%s = %s'+os.linesep) % (key, value))
        # 读取开始日期
        cf = ConfigParser.ConfigParser()
        cf.read(HousingStockSpider.CONFIG_FILE)
        try:
            start_date_str = cf.get('default', 'start_date')
        except:
            print u'正在重新生成配置文件...'
            with open(HousingStockSpider.CONFIG_FILE, 'w') as f:
                f.write('[default]' + os.linesep)
                for key, value in HousingStockSpider.default_config_dict.iteritems():
                    f.write(('%s = %s' + os.linesep) % (key, value))
            cf = ConfigParser.ConfigParser()
            cf.read(HousingStockSpider.CONFIG_FILE)
        # 当前日期
        curr_date = datetime.datetime.now()
        # 转换日期
        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        except:
            print u'配置文件格式不对，应用默认配置'
            start_date = datetime.datetime.strptime(HousingStockSpider.default_config_dict['start_date'], '%Y-%m-%d')
        # 爬取
        while start_date <= curr_date:
            date_str = start_date.strftime('%Y-%m-%d')
            data_list = self.get_data_by_date(date_str)
            if data_list:
                # 写单独文件
                with open(os.path.join(HousingStockSpider.DATA_PATH, '{}.csv'.format(date_str)), 'w'):
                    for data in data_list:
                        line = ','.join(data)
                        f.write(line+os.linesep)
                # 写汇总文件
                with open(HousingStockSpider.DATA_FILE, 'a'):
                    for data in data_list:
                        line = ','.join(data)
                        f.write(line+os.linesep)
            # 日期自增
            start_date += datetime.timedelta(days=1)
        # 写回配置
        cf.set('default', 'start_date', start_date.strftime('%Y-%m-%d'))
        cf.write(open(HousingStockSpider.CONFIG_FILE))


if __name__ == '__main__':
    spider = HousingStockSpider()
    spider.auto_fetch()
