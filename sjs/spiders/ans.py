# -*- coding: utf-8 -*-

import logging

from scrapy.exceptions import CloseSpider
from scrapy.spider import Spider, Request
from scrapy.http import FormRequest
from leancloud import Query, init, Object
import random
from bs4 import BeautifulSoup
from scrapy.selector import Selector
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
# 登陆信息
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


class AnsSpider(Spider):
    name = "ans"
    start_urls = (
        'http://www.yitiku.cn/login/',
    )

    def parse(self, response):
        logger.debug('start form request')

        user = random.choice(log_info.keys())  # 随机选择一个用户登陆
        pwd = log_info[user]

        return FormRequest.from_response(
            response,
            formdata={
                'account': user,
                'password': pwd,
                'remember': 'on'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        logger.debug('login form response parsing')

        if "authentication failed" in response.body:
            raise CloseSpider('login failed')
        if "进入我的主页" in response.body:
            query_answer = Query(Question)  # 查询出答案为空的试题
            query_answer.equal_to('answer', None)

            query_subject = Query(Question)  # 查询科目为高中数学的试题
            query_subject.equal_to('subject', '高中数学')

            main_query = Query.and_(query_answer, query_subject)  # and查询
            main_query.limit(3)  # 每次限定五个

            results = main_query.find()
            results_len = len(results)  # 查询结果有可能不足五个，所以循环的长度不能使用5
            print results_len
            print '!!!'
            for i in xrange(results_len):
                res_url = results[i].get('origin_url')  # 格式为/shiti/774552.html
                question_url = 'http://www.yitiku.cn%s' % res_url
                print question_url + '####'
                yield Request(url=question_url,
                              callback=self.parse_answer)

    def parse_answer(self, response):
        analysis_li = response.xpath('//div[@class="quesTxt quesTxt2"]/ul[2]/li[1]').extract()  # 有的为空
        if len(analysis_li) == 0:  # 如果提取的解析的li标签为空，说明该用户可能被屏蔽
            # TODO:更换用户重新爬取
            pass
        else:
            # 取出li标签中的div标签
            # TODO:将其中的图片路径提取出来保存到七牛上面
            analysis_div = response.xpath('//div[@class="quesTxt quesTxt2"]/ul[2]/li[1]/div[@class="editorBox"]').extract()[0]
            analysis = analysis_div

        answer_li = response.xpath('//div[@class="quesTxt quesTxt2"]/ul[2]/li[2]').extract()[0]  # 答案格式是<div>或者<b>，但是前一个标签都是font

        answer_soup = BeautifulSoup(answer_li, 'lxml')  # 从中选出font标签的后一个标签，
        answer_label = answer_soup.find('font').find_next_sibling()  # div或者b或者None
        if answer_label != None:
            answer_label_str = str(answer_label)
            if answer_label_str[0:2] == '<b':  # 说明为b标签
                answer = Selector(text=answer_label_str).xpath('//b/text()').extract()[0]
            elif answer_label_str[0:2] == '<d':
                # TODO:把里面的图片取出来
                answer = Selector(text=answer_label_str).xpath('//div[@class="editorBox"]').extract()[0]
            else:  # 另作处理
                answer = ''
        else:
            answer = ''
        data = {
            'origin_url': "/shiti/%s" % response.url.split('/')[-1],
            # 'point_urls': point_urls,
            # 'point_texts': point_texts,
            'analysis': analysis,
            'answer': answer
        }

        query = Query(Question)
        query.equal_to('origin_url', data['origin_url'])
        results = query.first()
        results.set('analysis', data['analysis'])
        results.set('answer', data['answer'])

        results.save()
