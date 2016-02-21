# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class QuestionItem(Item):
    origin_url = Field()
    state = Field()

class AnswerItem(Item):
    origin_url = Field()
    analysis = Field()
    point_texts = Field()
    answer = Field()

# class QuestionItem(Item):
#     origin_url = Field()
#     level = Field()
#     type = Field()
#     view_num = Field()
#     subject = Field()
#     has_image_content = Field()
#
#     content_div = Field()
#     point = Field()
#     file_urls = Field()
#     files = Field()