# -*- coding: utf-8 -*-

import logging

from scrapy.exceptions import CloseSpider
from scrapy.spider import Spider, Request
from scrapy.http import FormRequest
from leancloud import Query, init
from sjs.utils import LeanCloudError, Question
from sjs.items import QuestionItem

logger = logging.getLogger(__name__)
init('dtWwd7NTgHeB5WQHEg87E4bP-gzGzoHsz', '02E6cjvFpHDB9qJKoyULiU3k')


class AnsSpider(Spider):
    name = "ans"
    start_urls = (
        'http://www.yitiku.cn/login/',
    )

    def parse(self, response):
        logger.debug('start form request')
        """
        account:985677283@qq.com
        password:ytzyqpb1314
        remember:on
        """
        return FormRequest.from_response(
            response,
            formdata={
                'account': '985677283@qq.com',
                'password': 'ytzyqpb1314'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        logger.debug('login form response parsing')

        if "authentication failed" in response.body:
            raise CloseSpider('login failed')
        if "进入我的主页" in response.body:
            # TODO: question.origin_url and state = ?
            query_state = Query(Question)
            query_state.equal_to('state', 1)

            query_subject = Query(Question)
            query_subject.equal_to('subject', '高中数学')

            main_query = Query.and_(query_state, query_subject)
            main_query.limit(5)
            # for i in xrange(5):
            yield Request(url='http://www.yitiku.cn/shiti/1217235.html',
                          callback=self.parse_answer)

    def parse_answer(self, response):
        # all_info = HtmlXPathSelector(response)
        point_urls = response.xpath('//div[@class="quesTxt quesTxt2"]/ul[1]/li/div/a/@href').extract()
        point_texts = response.xpath('//div[@class="quesTxt quesTxt2"]/ul[1]/li/div/a/text()').extract()[0]

        analysis = response.xpath('//div[@class="quesTxt quesTxt2"]/ul[2]/li[1]/div[@class="editorBox"]').extract()[0]
        answer = response.xpath('//div[@class="quesTxt quesTxt2"]/ul[2]/li[2]/div[@class="editorBox"]').extract()[0]

        """
        title = response.xpath('/html/head/title/text()').extract()[0]
        kaodian = response.xpath('/html/body//div[@class="quesTxt quesTxt2"]/ul[1]/li[1]/fond/text()')
        analysis = response.xpath('/html/body//div[@class="quesTxt quesTxt2"]/ul[2]/li[1]/fond/text()').extract()
        # analysis = response.xpath('/html/body//div[@class="quesTxt quesTxt2"]/ul[2]/li[1]/fond/text()').extract()
        print title
        print kaodian
        print analysis
        """
        print analysis
        print point_texts
        print answer
        data = {
            'origin_url': "/shiti/%s" % response.url.split('/')[-1],
            'point_urls': point_urls,
            'point_texts': point_texts,
            'analysis': analysis,
            'answer': answer
        }

        yield QuestionItem(**data)

