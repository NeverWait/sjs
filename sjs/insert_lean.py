# -*- coding: utf-8 -*-
from leancloud import init, Object, Query
from scrapy.http import Request
# import re
from bs4 import BeautifulSoup
# import sjs.settings
# import urllib2
# import urllib
from requests.exceptions import ConnectionError
import time
import requests

init('dtWwd7NTgHeB5WQHEg87E4bP-gzGzoHsz', '02E6cjvFpHDB9qJKoyULiU3k')

log_info = {
    '8396621sina_qq@2925.com': 'mateng',
    '882349sina_168@2925.com': 'yilian',
    '882349sina_163@2925.com': 'caoshi',
    '882349sina_126@2925.com': 'sunxia',
    '882349sina_yahoo@2925.com': 'liaoli',
    '882349sina_edu@2925.com': 'ouyang',
    '882349sina_sohou@2925.com': 'zhangl',
    '882349sina_qq@2925.com': 'guoliu',
    '882349sina_a@2925.com': 'liuwan',
    '94993308q_gmail@2925.com': 'xinxin',
    '94993308q_126@2925.com': 'lanlan',
    '94993308q_163@2925.com': 'wanliu',
    '94993308q_edu@2925.com': 'liuyan',
    '94993308q_yahoo@2925.com': 'chaoya',
    '94993308q_168@2925.com': 'liwang',
    '94993308q_google@2925.com': 'lisisi',
}
url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=995647001425869&num=30&area_ex=%E6%BE%B3%E9%97%A8%2C%E9%A6%99%E6%B8%AF&port_ex=9000%2C8080%2C8090&b_pcchrome=1&b_pcie=1&b_pcff=1&b_android=1&b_iphone=1&b_ipad=1&protocol=2&method=2&an_ha=1&sep=4'

proxies = requests.get(url)
no_http_proxies_list = proxies.content.split('|')
print no_http_proxies_list
# no_http_proxies_list = ['92.222.237.14:8898']
# new_proxies_list = [i for i in no_http_proxies_list]
# new_proxies_set = set(new_proxies_list)

# proxy = {'http': 'http://92.222.237.26:8888'}
# <div class="ip_text">您当前的IP：175.12.134.83</div>
for i in no_http_proxies_list:
    print '------'
    proxy = {'https': 'http://%s' % i}
    print proxy
    try:
        ip_cont = requests.get('http://www.ipip.net/', proxies=proxy)
    except:
        continue
    if ip_cont.status_code == 200:
        ip_soup = BeautifulSoup(ip_cont.content, 'lxml')
        ip = ip_soup.find('div', class_='ip_text')
        print ip.text
    else:
        print 'error'
    # try:
    #     ip_cont = requests.get('https://api.ipify.org', proxies=proxy)
    # except:
    #     continue
    # if ip_cont.status_code == 200:
    #     print ip_cont.text
    # else:
    #     print 'no'


# class YTKAccount(Object):
#     @property
#     def email(self):
#         return self.get('email')
#
#     @email.setter
#     def email(self, value):
#         return self.set('email', value)
#
#     @property
#     def password(self):
#         return self.get('password')
#
#     @password.setter
#     def password(self, value):
#         return self.setter('password', value)
#
#     @property
#     def state(self):
#         return self.get('state')
#
#     @state.setter
#     def state(self, value):
#         return self.setter('state', value)

# ytk_account1 = YTKAccount()
# ytk_account1.set('email', '882349sina_168@2925.com')
# ytk_account1.set('password', 'yilian')
# ytk_account1.set('state', 0)
#
# ytk_account1.save()

# 获取一个proxy，用它访问ipip，如果获取的查看获取的ip地址
# 地址正确则使用该proxy，不正确的话把该地址存入数据库并且继续判断下一个
# ProxyNode = Object.extend('ProxyNode')
#
# proxy_list = [
#     '112.95.39.99:8090',
#     '117.84.37.217:8090',
#     '117.136.234.6:80',
# ]
# proxy_ip = '117.136.234.6:80'
# req = Request('http://www.yitiku.cn',
#         method='GET',
#         meta={'proxy': 'http://%s' % proxy_ip}
#         )

# print req._get_body.
# proxy_node = ProxyNode()
# for each_ip in proxy_list:
#     proxy_node.set('proxy', 'http://%s' % each_ip)
#     proxy_node.set('state', 3)
#     proxy_node.save()
    # print each_ip
    # each_proxy = {'http': each_ip}
    # # s = requests.Session()
    # try:
    #     ip_content = requests.get('http://www.ipip.net/', proxies=each_proxy)
    #     # print ip_content.content
    #     print ip_content.status_code
    # except ConnectionError as e:
    #     continue
    # # time.sleep(1)
    # # break


"""
邮箱
密码
状态

"""
# class ProxyNode(Object):
#     @property
#     def proxy(self):
#         return self.get('score')
#
#     @proxy.setter
#     def proxy(self, value):
#         return self.set('proxy', value)
#
#     @property
#     def state(self):
#         return self.get('state')
#
#     @state.setter
#     def state(self, value):
#         return self.set('state', value)
#
#     @property
#     def timestamp(self):
#         return self.get('timestamp')
#
#     @timestamp.setter
#     def timestamp(self, value):
#         return self.set('timestamp', value)
#
# proxy_node = ProxyNode()
# proxy_node.set('proxy', 'test')
# proxy_node.set('state', 0)
# proxy_node.set('timestamp', 1454562276)

# ProxyNode = Object.extend('ProxyNode')
# proxy_node = ProxyNode()
#
# proxy_address = 'http://dev.kuaidaili.com/api/getproxy/?orderid=905636753311252&num=30&area=%E4%B8%AD%E5%9B%BD&area_ex=%E6%BE%B3%E9%97%A8%2C%E9%A6%99%E6%B8%AF&b_pcchrome=1&b_pcie=1&b_pcff=1&b_android=1&b_iphone=1&b_ipad=1&protocol=1&method=2&an_ha=1&sep=4'
# proxies = requests.get(proxy_address)
# proxies_list = proxies.content.split('|')
#

# proxy_node.save()
# question.set('origin_url', '/shiti/759210.html')
# question.set('subject', '高中数学')
#
# question.set('origin_url', '/shiti/759214.html')
# question.set('subject', '高中数学')

# question.set('origin_url', '/shiti/759220.html')
# question.set('subject', '高中数学')

# question.set('origin_url', '/shiti/772418.html')
# question.set('subject', '高中数学')
#
# question.save()
