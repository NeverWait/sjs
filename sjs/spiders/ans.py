# -*- coding: utf-8 -*-

import logging

from scrapy.exceptions import CloseSpider
from scrapy.spiders import Spider, Request
from scrapy.http import FormRequest
from scrapy.utils.request import request_fingerprint
from leancloud import Query, init, Object
import random
from bs4 import BeautifulSoup
import sjs.settings
from qiniu import Auth, BucketManager
from proxy_base import CookiesProxySpider
# from sjs.utils import LeanCloudError, Question
# from sjs.items import QuestionItem

logger = logging.getLogger(__name__)
init('dtWwd7NTgHeB5WQHEg87E4bP-gzGzoHsz', '02E6cjvFpHDB9qJKoyULiU3k')
Question = Object.extend("Question")

"""
本爬虫是抓取试题的解析和答案，流程是：
1 访问易题库登陆页面，先登陆（注意：每个科目的老师只能看所教科目的试题答案，高中数学老师只能看高中数学试题的答案，无法查看其他科目答案）
2 从leancloud里读取没有答案的试题
3 访问这些试题的页面，获取答案、解析、知识点
4 保存到数据库
5 建立和知识点的关系
"""

# class AnsSpider(CookiesProxySpider):
class AnsSpider(Spider):
    name = "ans"
    custom_settings = {
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2
    }
    start_urls = (
        'http://www.baidu.com',
    )
    def parse(self, response):
        print response.xpath('/html/head/title/text()').extract()[0]
    # def __init__(self, *a, **kw):
    #     super(AnsSpider, self).__init__(*a, **kw)
    #     self._bucket_mgr = None
    #     self._bucket = getattr(sjs.settings, 'PIPELINE_QINIU_BUCKET', None)
    #     self._key_prefix = getattr(sjs.settings, 'PIPELINE_QINIU_KEY_PREFIX', None)
    #     self.juan_cache = None
    #     aa = self.aa
    #     print aa
    #     # self.account = None
    #     # print self.account
    #
    # @property
    # def bucket_mgr(self):
    #     """
    #     get qiniu bucket manager
    #     :return:
    #     """
    #     if not self._bucket_mgr:
    #         ak = getattr(sjs.settings, 'PIPELINE_QINIU_AK', None)
    #         sk = getattr(sjs.settings, 'PIPELINE_QINIU_SK', None)
    #         q = Auth(ak, sk)
    #         self._bucket_mgr = BucketManager(q)
    #     return self._bucket_mgr
    #
    # def fetch_file(self, url):
    #     if url[0:3] != 'www':
    #         url = 'http://www.yitiku.cn%s' % url
    #     request = Request(url, meta={'qiniu_key_generator': 'qiniu_key_generator'})
    #     key = '%s%s' % (self._key_prefix, request_fingerprint(request))
    #     if not self._bucket:
    #         logger.error('No bucket specified')
    #         raise IOError
    #     if not key:
    #         logger.error('No key specified')
    #         raise IOError
    #     ret, error = self.bucket_mgr.fetch(url, self._bucket, key)
    #     if ret:
    #         return {
    #             'url': url,
    #             'checksum': ret['hash'],
    #             'bucket': self._bucket,
    #             'key': ret['key']
    #         }
    #     else:
    #         raise IOError
    #
    # # def parse(self, response):
    # #     # formdata={
    # #     #         'account': user,
    # #     #         'password': pwd,
    # #     #         'remember': 'on'
    # #     #     },
    # #     logger.debug('start form request')
    # #
    # #     # user = self.account
    # #     # pwd = self.password
    # #     # proxy = self.proxy
    # #     user = '985677283@qq.com'
    # #     pwd = 'ytzyqpb1314'
    # #
    # #     logger.info(user)  # 输出使用的是那个账号
    # #
    # #     return FormRequest.from_response(
    # #         response,
    # #         formdata={
    # #             'account': user,
    # #             'password': pwd,
    # #         },
    # #         callback=self.after_login
    # #     )
    # #
    # # def after_login(self, response):
    # #     logger.debug('login form response parsing')
    # #
    # #     if "authentication failed" in response.body:
    # #         raise CloseSpider('login failed')
    # #     if "进入我的主页" in response.body:
    # #
    # #         title = response.xpath('/html/head/title/text()').extract()[0]
    # #         logger.info(title)
    # #         query_answer = Query(Question)  # 查询出答案为空的试题
    # #         query_answer.equal_to('answer', None)
    # #
    # #         query_subject = Query(Question)  # 查询科目为高中数学的试题
    # #         query_subject.equal_to('subject', '高中数学')
    # #
    # #         main_query = Query.and_(query_answer, query_subject)  # and查询
    # #         main_query.limit(2)  # 每次限定五个
    # #
    # #         results = main_query.find()
    # #         results_len = len(results)  # 查询结果有可能不足五个，所以循环的长度不能使用5
    # #
    # #         for i in xrange(results_len):
    # #             res_url = results[i].get('origin_url')  # 格式为/shiti/774552.html
    # #             question_url = 'http://www.yitiku.cn%s' % res_url
    # #
    # #             logger.info('crawling %s' % question_url)
    # #
    # #             yield Request(url=question_url,
    # #                           callback=self.parse_answer)
    # #
    # # def parse_answer(self, response):
    # #     analysis_answer_list = response.xpath('//div[@class="quesTxt quesTxt2"]').extract()  # 包含试题解析和答案的div标签
    # #     if len(analysis_answer_list) == 0:  # 该爬虫有可能被禁
    # #         # TODO:爬虫被禁，更换用户
    # #         logger.debug('reqeust forbiden!!!')
    # #     else:
    # #         analysis_answer_label = analysis_answer_list[0]
    # #         analysis_answer_soup = BeautifulSoup(analysis_answer_label, 'lxml')
    # #         analysis_div = analysis_answer_soup.find('div', class_='editorBox')  # 找到试题解析的div
    # #
    # #         analysis_imgs = []
    # #         analysis_imgs_list = analysis_div.find_all('img')
    # #         analysis_imgs_count = len(analysis_imgs_list)
    # #         if analysis_imgs_count == 1:
    # #             analysis_imgs.append(self.fetch_file(analysis_div.find('img')['src']))  # 保存试题解析的图片的信息
    # #             analysis_div.find('img')['src'] = '0'  # 把图片的src改为序号
    # #         elif analysis_imgs_count > 1:
    # #             analysis_imgs.append(self.fetch_file(analysis_div.find('img')['src']))  # 由于find_next_siblings是从第二个开始的，先保存试题解析的第一个的图片的信息
    # #             analysis_div.find('img')['src'] = '0'  # 把第一个图片的src改为序号
    # #             m = 1
    # #             for each_analysis_img in analysis_div.img.find_next_siblings('img'):
    # #                 analysis_img_url = each_analysis_img['src']
    # #                 analysis_imgs.append(self.fetch_file(analysis_img_url))
    # #                 each_analysis_img['src'] = str(m)
    # #                 m += 1
    # #         analysis = str(analysis_div)  # 无论解析内容是否存在，标签一定存在,有的有图片有的没有图片。由于需要修改图片的src，所以此句要放到后面
    # #
    # #         answer_label = analysis_answer_soup.find('font', text='答案').find_next_sibling()  # 找到答案的标签，无论答案是否存在，答案的标签一定存在，答案标签是<div>或者<b>
    # #
    # #         answer_imgs = []
    # #         answer_imgs_list = answer_label.find_all('img')
    # #         answer_imgs_count = len(answer_imgs_list)
    # #         if answer_imgs_count == 1:
    # #             answer_imgs.append(self.fetch_file(answer_label.find('img')['src']))  # 保存图片信息
    # #             answer_label.find('img')['src'] = '0'  # 修改图片的序号
    # #         elif answer_imgs_count > 1:
    # #             answer_imgs.append(self.fetch_file(answer_label.find('img')['src']))  # find_next_siblings是从第二个img开始的，所以需要先把第一个加入
    # #             answer_label.find('img')['src'] = '0'
    # #             n = 1
    # #             for each_answer_img in answer_label.img.find_next_siblings('img'):
    # #                 answer_img_url = each_answer_img['src']
    # #                 answer_imgs.append(self.fetch_file(answer_img_url))
    # #                 each_answer_img['src'] = str(n)
    # #                 n += 1
    # #         answer = str(answer_label)  # 由于需要修改图片的src，所以此句要放到后面
    # #
    # #     question_url_split = response.url.split('/')
    # #     url_split_len = len(question_url_split)
    # #     if question_url_split[url_split_len-1] == '':
    # #         origin_url = '/shiti/%s' % question_url_split[url_split_len-2]
    # #     origin_url = '/shiti/%s' % question_url_split[url_split_len-1]
    # #     print origin_url + '******'
    # #     data = {
    # #         'analysis': analysis,
    # #         'analysis_imgs': analysis_imgs,
    # #         'answer_imgs': answer_imgs,
    # #         'answer': answer,
    # #         'origin_url': origin_url
    # #
    # #     }
    # #
    # #     query = Query(Question)
    # #     query.equal_to('origin_url', data['origin_url'])
    # #     results = query.first()
    # #     for k in data:
    # #         results.set(k, data[k])
    # #     results.save()
