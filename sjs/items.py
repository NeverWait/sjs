# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class SjsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BasicJuanItem(Item):
    title = Field()
    origin_url = Field()
    subject = Field()
    question_num = Field()
    view_num = Field()
    upload_time = Field()
    uploader = Field()
    state = Field()
    # question_types ('题型': '数量')


class JuanItem(Item):
    origin_url = Field()
    grade = Field()
    usage = Field()
    area = Field()
    year = Field()
    question_urls = Field()


class SjRangeItem(Item):
    subject = Field()
    code = Field()
    page_num = Field()


class PointTypeItem(Item):
    subject = Field()
    origin_url = Field()
    text = Field()
    book_texts = Field()
    book_urls = Field()


class QuestionItem(Item):
    origin_url = Field()
    level = Field()
    type = Field()
    view_num = Field()
    subject = Field()
    has_image_content = Field()

    content_div = Field()
    point = Field()
    file_urls = Field()
    files = Field()