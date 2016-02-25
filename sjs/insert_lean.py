# -*- coding: utf-8 -*-
from leancloud import init, Object, Query
import re
from bs4 import BeautifulSoup
import sjs.settings

init('dtWwd7NTgHeB5WQHEg87E4bP-gzGzoHsz', '02E6cjvFpHDB9qJKoyULiU3k')
Question = Object.extend("Question")

question = Question()

# question.set('origin_url', '/shiti/759210.html')
# question.set('subject', '高中数学')
#
# question.set('origin_url', '/shiti/759214.html')
# question.set('subject', '高中数学')

# question.set('origin_url', '/shiti/759220.html')
# question.set('subject', '高中数学')

question.set('origin_url', '/shiti/772418.html')
question.set('subject', '高中数学')

question.save()
