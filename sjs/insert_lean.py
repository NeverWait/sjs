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

url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=995647001425869&num=30&area_ex=%E6%BE%B3%E9%97%A8%2C%E9%A6%99%E6%B8%AF&port_ex=9000%2C8080%2C8090&b_pcchrome=1&b_pcie=1&b_pcff=1&b_android=1&b_iphone=1&b_ipad=1&protocol=2&method=2&an_ha=1&sep=4'

proxies = requests.get(url)
no_http_proxies_list = proxies.content.split('|')
print no_http_proxies_list
for i in no_http_proxies_list:
    print '------'
    proxy = {'http': 'http://%s' % i}
    print proxy
    try:
        ip_cont = requests.get('http://www.ipip.net/', proxies=proxy, timeout=6)
    except:
        continue
    if ip_cont.status_code == 200:
        ip_soup = BeautifulSoup(ip_cont.content, 'lxml')
        ip = ip_soup.find('div', class_='ip_text')
        print ip.text
    else:
        print 'error'
# """
# 759212
# 759209
# 759217
# 759219
# 759207
# 939675
# 772565
# 761527
# 761528
# """
# Question = Object.extend('Question')
# question = Question()
# question.set('origin_url', '/shiti/761528.html')
# question.set('subject', '高中数学')
# question.save()

