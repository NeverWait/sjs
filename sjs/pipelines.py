# coding: utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from leancloud import init, LeanCloudError, Query
from sjs.items import SjRangeItem, BasicJuanItem, JuanItem, PointTypeItem, QuestionItem
from sjs.utils import insert_or_update, Range, Juan, PointType, Question

init('dtWwd7NTgHeB5WQHEg87E4bP-gzGzoHsz', '02E6cjvFpHDB9qJKoyULiU3k')


class LeanCloudPipeline(object):

    @staticmethod
    def process_sj_range(item):
        code = item['code'].strip()
        if not code:
            return
        data = {
            'page_num': int(item['page_num']),
            'code': code,
            'type': 'sj',
            'subject': item['subject']
        }

        query = Query(Range)
        query.equal_to('code', code)
        query.equal_to('type', 'sj')
        try:
            one = query.first()
        except LeanCloudError:
            one = Range()
            last_page_num = 0
            one.set('state', 0)
        else:
            last_page_num = one.get('page_num')
            if last_page_num != data['page_num']:
                one.set('state', 0)
            else:
                one.set('state', 1)
        for k, v in data.items():
            one.set(k, v)
        one.set('last_page_num', last_page_num)
        one.save()
        return item

    @staticmethod
    def process_basic_juan(item):
        origin_url = item['origin_url']
        fields = ['title', 'subject', 'upload_time', 'uploader']
        data = {
            'origin_url': origin_url,
            'view_num': int(item['view_num']),
            'question_num': int(item['question_num']),
            'state': 0
        }
        for f in fields:
            data[f] = item[f]
        insert_or_update(Juan, {'origin_url': origin_url, 'state': 0}, data)

    @staticmethod
    def process_juan(item):
        origin_url = item['origin_url']
        juan = insert_or_update(Juan, {'origin_url': origin_url}, {}, False)
        for f in ['grade', 'usage', 'area', 'year', 'question_urls']:
            juan.set(f, item[f])
        juan.set('state', 1)
        juan.save()
        return item

    @staticmethod
    def process_point_type(item):
        insert_or_update(PointType, {'origin_url': item['origin_url']}, item)

    @staticmethod
    def process_question(item):
        point = item['point']
        query = Query(Question)
        query.equal_to('origin_url', item['origin_url'])

        if point:
            query.include('points')
        try:
            question = query.first()
        except LeanCloudError:
            question = Question()
            question.set('state', 0)
            if point:
                points = question.relation('points')
                points.add(point)
        else:
            if point:
                points = question.relation('points')
                point_query = points.query().equal_to('objectId', point.id)
                try:
                    point_query.first()
                except LeanCloudError:
                    points.add(point)
            else:
                question.set('state', 1)

        for x in item['files']:
            x.pop('path', None)

        if item['has_image_content']:
            if point:
                question.set('small_image', item['files'][0])
            else:
                question.set('big_image', item['files'][0])
        else:
            question.set('content', unicode(item['content_div']))
            question.set('content_images', item['files'])

        for f in ['content_div', 'file_urls', 'files', 'point']:
            del item[f]

        for k, v in item.items():
            question.set(k, v)

        if question.get('small_image') or question.get('big_image'):
            question.set('has_image_content', True)
        question.save()
        # for item serializable
        return item

    def process_item(self, item, spider):

        if isinstance(item, SjRangeItem):
            self.process_sj_range(item)
        elif isinstance(item, BasicJuanItem):
            self.process_basic_juan(item)
        elif isinstance(item, JuanItem):
            self.process_juan(item)
        elif isinstance(item, PointTypeItem):
            self.process_point_type(item)
        elif isinstance(item, QuestionItem):
            self.process_question(item)
        return item
