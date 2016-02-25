# coding: utf-8
import re
import sys
from bs4 import BeautifulSoup, Comment
from leancloud import Query, LeanCloudError, Object
from sjs.items import QuestionItem

__author__ = 'chengchang'


class Range(Object):
    pass


class Juan(Object):
    pass


class Question(Object):
    pass


class QuestionTest(Object):
    pass


class PointType(Object):
    pass


class Point(Object):
    pass


def insert_or_update(model, cond, data, saving=True):
    query = Query(model)
    for k, v in cond.items():
        query.equal_to(k, v)
    try:
        one = query.first()
    except LeanCloudError:
        one = model()
    for k, v in data.items():
        one.set(k, v)
    if saving:
        one.save()
    return one


sys.setrecursionlimit(10000)


def traverse_point(subject, point_type, items, parent=None, prefix=''):
    for i, el in enumerate(items):
        # print prefix, i, el.label.a.string,
        is_leaf = el.ul is None
        origin_url = el.label.a['href']
        data = {
            'origin_url': origin_url,
            'is_leaf': is_leaf,
            'type': point_type,
            'order': i,
            'subject': subject,
            'text': el.label.a.string
        }

        query = Query(Point)
        query.equal_to('origin_url', origin_url)
        try:
            point = query.first()
        except LeanCloudError:
            point = Point(**data)
        else:
            for k, v in data.items():
                point.set(k, v)
        if parent:
            point.set('parent', parent)
        point.save()

        if not is_leaf:
            traverse_point(subject, point_type, el.ul, point, '--' + prefix)
            # traverse(el.ul, '--' + prefix, None)


def is_image_content(soup):
    flag = True
    for tag in ['span', 'p', 'table', 'br', 'u', 'i']:
        flag = flag and len(soup.find_all(tag)) == 0
    return flag and len(soup.find_all('img')) == 1


def clean_url(origin_urls):
    for i, url in enumerate(origin_urls):
        if url.endswith('/'):
            origin_urls[i] = origin_urls[i][:-1]
    return origin_urls


def parse_juan_questions(subject, response):

    question_divs = response.xpath('//*[@class="quesdiv"]/div[1]').extract()
    origin_urls = response.xpath('//*[@id="js_qs"]/li[2]/a/@href').extract()
    types = response.xpath('//*[@id="js_qs"]/input[2]/@value').extract()
    levels = response.xpath('//*[contains(@class, "handle")]/div/u[1]/i/text()').extract()
    view_nums = response.xpath('//*[contains(@class, "handle")]/div/u[2]/i/text()').extract()

    origin_urls = clean_url(origin_urls)
    questions = []
    # for i, html in enumerate(question_divs[5:6]):
    for i, html in enumerate(question_divs):
        soup = BeautifulSoup(html, 'lxml')
        for el in soup.find_all(text=lambda text: isinstance(text, Comment)):
            el.extract()
        num = soup.find(text=re.compile('\d+.'))
        if num:
            num.extract()
        for el in soup.find_all('font', class_='reportError'):
            el.extract()
        for el in soup.find_all('img', class_='new'):
            el.extract()
        for el in soup.find_all('span', class_='colf43'):
            el.extract()
        for el in soup.find_all('a'):
            for child in el.contents:
                el.replace_with(child)

        image_urls = []
        for k, el in enumerate(soup.find_all('img')):
            lazy = el.get('lazy-src')
            if lazy:
                url = el['lazy-src']
            else:
                url = el['src']

            if url.startswith('/'):
                url = 'http://www.yitiku.cn%s' % url

            image_urls.append(url)
            el['src'] = k
            del el['lazy-src']

        item = QuestionItem(**{
            'origin_url': origin_urls[i],
            'level': levels[i],
            'type': types[i],
            'view_num': int(view_nums[i]),
            'content_div': soup.div,
            'file_urls': image_urls,
            'subject': subject,
            'has_image_content': is_image_content(soup),
            'point': None
        })

        query = Query(Question)
        query.equal_to('origin_url', item['origin_url'])
        try:
            question = query.first()
        except LeanCloudError:
            questions.append(item)
        else:
            remote = question.get('has_image_content')
            local = item['has_image_content']
            if remote == local and local is False:
                break
            else:
                questions.append(item)
    return questions


def parse_questions(point, response):
    content_divs = response.xpath('//*[@class="quesdiv"]').extract()
    origin_urls = response.xpath('//*[@id="js_qs"]/li[2]/a/@href').extract()
    types = response.xpath('//*[@id="js_qs"]/input[2]/@value').extract()
    levels = response.xpath('//*[contains(@class, "handle")]/div/u[1]/i/text()').extract()
    view_nums = response.xpath('//*[contains(@class, "handle")]/div/u[2]/i/text()').extract()
    subjects = response.xpath('//*[@id="js_qs"]/input[1]/@value').extract()

    origin_urls = clean_url(origin_urls)
    questions = []
    for i, html in enumerate(content_divs):
        soup = BeautifulSoup(html, 'lxml')
        for el in soup.find_all(text=lambda text: isinstance(text, Comment)):
            el.extract()
        for el in soup.find_all('font', class_='reportError'):
            el.extract()
        for el in soup.find_all('img', class_='new'):
            el.extract()
        for el in soup.find_all('span', class_='colf43'):
            el.extract()

        for el in soup.find_all('a'):
            for child in el.contents:
                el.replace_with(child)

        image_urls = []
        for k, el in enumerate(soup.find_all('img')):
            lazy = el.get('lazy-src')
            if lazy:
                url = el['lazy-src']
            else:
                url = el['src']

            if url.startswith('/'):
                url = 'http://www.yitiku.cn%s' % url

            image_urls.append(url)
            el['src'] = k
            del el['lazy-src']

        questions.append(QuestionItem(**{
            'origin_url': origin_urls[i],
            'level': levels[i],
            'type': types[i],
            'view_num': int(view_nums[i]),
            'content_div': soup.div.find('div'),
            'subject': subjects[i],
            'has_image_content': is_image_content(soup),
            'point': point,
            'file_urls': image_urls
        }))
    return questions