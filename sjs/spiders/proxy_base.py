# coding: utf-8

import logging
from scrapy import Spider
from scrapy.exceptions import CloseSpider
from scrapy.http import Request, FormRequest
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.defer import TimeoutError
from twisted.internet.error import ConnectionRefusedError
from leancloud import Object, Query, LeanCloudError, init
import requests
from bs4 import BeautifulSoup
import user_agent
from requests.exceptions import ConnectionError

__author__ = 'think'

init('dtWwd7NTgHeB5WQHEg87E4bP-gzGzoHsz', '02E6cjvFpHDB9qJKoyULiU3k')
logger = logging.getLogger('unstable_proxy')
ProxyNode = Object.extend('ProxyNode')
YTKAccount = Object.extend('YTKAccount')


class CookiesProxySpider(Spider):
    """
    代理状态码说明：
    0 代表可用
    1 代表正在使用
    2 代表被禁
    3 代表不能使用
    """
    name = 'proxy'
    start_urls = (
        'http://www.yitiku.cn/login/',
    )

    def get_leancloud_proxies(self):
        """
        返回不可用的或者正在使用的代理
        """
        query = Query(ProxyNode)
        query.select('proxy')
        query.contained_in('state', [1, 2, 3])
        try:
            unavailables = query.find()
        except LeanCloudError as e:
            logger.error(e)
            raise CloseSpider('leancloud cannot reach')
        # TODO: list to dict
        # key in dict/list
        unavailables_list = []
        for i in unavailables:
            unavailables_list.append(i.get('proxy'))
        unavailables_set = set(unavailables_list)
        return unavailables_set

    def get_kdl_api(self):
        """
        获取新的代理
        """
        # url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=995647001425869&num=30&area_ex=%E6%BE%B3%E9%97%A8%2C%E9%A6%99%E6%B8%AF&b_pcchrome=1&b_pcie=1&b_pcff=1&b_android=1&b_iphone=1&b_ipad=1&protocol=2&method=2&an_ha=1&quality=2&sep=4'
        url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=995647001425869&num=30&area_ex=%E6%BE%B3%E9%97%A8%2C%E9%A6%99%E6%B8%AF&port_ex=9000%2C8080%2C8090&b_pcchrome=1&b_pcie=1&b_pcff=1&b_android=1&b_iphone=1&b_ipad=1&protocol=2&method=2&an_ha=1&sep=4'
        proxies = requests.get(url)
        proxies_list = proxies.content.split('|')
        head_proxies_list = ['http://%s' % i for i in proxies_list]
        head_proxies_set = set(head_proxies_list)
        return head_proxies_set

    def test_proxy(self):
        """
        经过测试返回一个可用的代理
        """
        unavailable_set = self.get_leancloud_proxies()
        new_proxies_set = self.get_kdl_api()
        difference_set = new_proxies_set - unavailable_set

        for each_proxy in difference_set:
            http_proxy = {'http': each_proxy}
            try:
                visit_ip = requests.get('http://www.ipip.net/', proxies=http_proxy, timeout=5)
            except:
                # logger.info('proxy unavailable', each_proxy)
                print 'proxy unavailable', each_proxy
                self.save_proxy(each_proxy, 3)
                continue
            if visit_ip.status_code == 200:
                # logger.debug('ipip status code 200')
                print 'ipip status code 200'

                ip_html = visit_ip.content
                ip_soup = BeautifulSoup(ip_html, 'lxml')
                ip_div = ip_soup.find('div', class_='ip_text')
                each_ip_split = each_proxy.split('//')[1]
                print ip_div.text.split(u'：')[1]
                print each_ip_split.split(':')[0]
                if ip_div.text.split(u'：')[1] == each_ip_split.split(':')[0]:
                    logger.info('use this ip: ', each_proxy)
                    print 'use this ip: ', each_proxy
                    self.save_proxy(each_proxy, 0)
                    return each_proxy
                    # print each_proxy
                    # break
                else:
                    # logger.debug('ip is not proxy')
                    print 'ip is not proxy'
                    self.save_proxy(each_proxy, 3)
            else:
                # logger.debug('ipip status is !200')
                print 'ipip status is !200'
                self.save_proxy(each_proxy, 3)

    def get_account(self):
        """
        获取没有使用的易题库账号
        """
        query = Query(YTKAccount)
        try:
            query.select('email', 'password')
            query.equal_to('state', 0)
            ytk_account = query.first()
            email = ytk_account.get('email')
            password = ytk_account.get('password')
            ytk_account.set('state', 1)
            ytk_account.save()
        except LeanCloudError as e:
            logger.error(e)
            raise CloseSpider('leancloud cannot reach')
        return [email, password]

    def save_proxy(self, proxy, state):
        """
        保存账号
        """
        proxy_node = ProxyNode()
        try:
            proxy_node.set('proxy', proxy)
            proxy_node.set('state', state)
            proxy_node.save()
        except LeanCloudError as e:
            logger.error(e)
            raise CloseSpider('leancloud cannot reach')

    def __init__(self, *a, **kw):
        super(CookiesProxySpider, self).__init__(*a, **kw)
        # ytk_account = self.get_account()
        # self.account = ytk_account[0]
        # self.password = ytk_account[1]
        # self.proxy = self.test_proxy()

    def parse(self, response):
        logger.debug('start form request')

        # user = self.account
        # pwd = self.password
        # proxy = self.proxy
        # meta={'proxy': proxy},
        # 您当前的IP：92.222.237.93
        user = '882349sina_163@2925.com'
        pwd = 'caoshi'
        proxy = 'http://103.251.43.53:80'
        logger.info(user)  # 输出使用的是那个账号

        return FormRequest.from_response(
            response,
            formdata={
                'account': user,
                'password': pwd,
                'remember': 'on',
            },
            meta={
                'cookiejar': 1,
            },
            callback=self.after_login
        )

    def after_login(self, response):
        logger.debug('login form response parsing')

        if "authentication failed" in response.body:
            raise CloseSpider('login failed')
        if "进入我的主页" in response.body:
            print response.xpath('/html/head/title/text()').extract()[0]
            print response.headers
            print response.headers.getlist('Set-Cookie')
            question_url = 'http://www.yitiku.cn/shiti/772565.html'
            yield Request(url=question_url,
                          meta={'cookiejar': response.meta['cookiejar']},
                          headers=response.headers,
                          callback=self.parse_answer)
        else:
            print 'log error'

    def parse_answer(self, response):
        analysis_answer_list = response.xpath('//div[@class="quesTxt quesTxt2"]').extract()
        print analysis_answer_list
        print response.headers.getlist('Set-Cookie')
        print response.meta['cookiejar']

    @staticmethod
    def error_handle(failure):
        if failure.check(HttpError):
            logger.error('HTTP Error: %s' % failure.value.response.url)
        elif failure.check(TimeoutError):
            logger.info('Timeout Error')
        elif failure.check(ConnectionRefusedError):
            logger.info('Connection Refused Error')


# if __name__ == '__main__':
#     spider = CookiesProxySpider()
#     aa = spider.get_account()
#     print aa[0], aa[1]