from leancloud import init
from leancloud import Object
__author__ = 'think'


init('dtWwd7NTgHeB5WQHEg87E4bP-gzGzoHsz', '02E6cjvFpHDB9qJKoyULiU3k')

class Question(Object):
    @property
    def origin_url(self):
        return self.get('origin_url')

    @origin_url.setter
    def origin_url(self, value):
        return self.set('origin_url', value)

    @property
    def state(self):
        return self.get('state')

    @state.setter
    def state(self,value):
        return self.set('state', value)

question = Question()
question.set('origin_url', '/shiti/759219.html')
question.set('state', 0)

question.save()