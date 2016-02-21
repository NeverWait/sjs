# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from leancloud import init, LeanCloudError, Query
from items import AnswerItem, QuestionItem
from utils import Question

class SjsPipeline(object):

    @staticmethod
    def process_question(item):
        origin_url = item['origin_url']
        analysis = item['analysis']
        point_text = item['point_text']
        answer = item['answer']

        query = Query(Question)
        query.equal_to('origin_url', origin_url)

        if origin_url:
            query.include('')

    # origin_url = Field()
    # analysis = Field()
    # point_texts = Field()
    # answer = Field()

