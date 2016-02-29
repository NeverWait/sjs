# # coding: utf-8
#
# import time
# import logging
# import sjs.settings
# import random
# from leancloud import Object, Query, LeanCloudError, init
# from scrapy.exceptions import CloseSpider
#
#
# __author__ = 'think'
#
#
# init('dtWwd7NTgHeB5WQHEg87E4bP-gzGzoHsz', '02E6cjvFpHDB9qJKoyULiU3k')
#
#
# class ProxyNode(Object):
#     pass
#
# class ProxySpiderMiddleware(object):
#     def __init__(self, settings):
#         self.baned_list = self.get_baned_proxies()
#         self.proxies = {}
#         self.last_time = time.time()
#         self.min_proxy_size = 15
#         self.update_cycle = 720
#
#     @staticmethod
#     def get_baned_proxies():
#         query = Query(ProxyNode)
#         query.equal_to('state', 1)
#         query.descending('createdAt')
#         try:
#             nodes = query.find()
#         except LeanCloudError as e:
#             if e.code != 101:
#                 raise CloseSpider('cannot touch leancloud')
#             return {}
#         return {node.get('proxy'): 1 for node in nodes}
#
#     @property
#     def proxy_list(self):
#         now = time.time()
#         if len(self.proxies) > self.min_proxy_size and now - self.last_time > self.update_cycle:
#             logging.info('local proxies')
#             return self.proxies.keys()
#
#         query = Query(ProxyNode)
#         query.equal_to('state', 0)
#         query.greater_than_or_equal_to('timestamp', int(now - self.update_cycle))
#
#         try:
#             nodes = query.find()
#         except LeanCloudError as e:
#             if e.code != 101:
#                 raise CloseSpider('can not touch leancloud')
#             nodes = []
#
#         remote = {node.get('proxy'): 1 for node in nodes}
#         if len(nodes) >= self.min_proxy_size:
#             self.proxies = remote
#             logging.info('leancloud proxies')
#             return self.proxies.keys()
#
#         delta, results = self.min_proxy_size - len(nodes), dict()
#         while delta > 0:
#             proxies = self.request_proxy_server()
#             for proxy in proxies:
#                 key = 'http://%s' % proxy
#                 if key in self.baned_list or key in remote:
#                     continue
#                 query = Query(ProxyNode)
#                 query.equal_to('proxy', key)
#                 try:
#                     node = query.first()
#                 except LeanCloudError:
#                     node = ProxyNode()
#                     node.set('proxy', key)
#                 node.set('state', 0)
#                 node.set('timestamp', int(time.time()))
#                 node.save()
#                 results[key] = 1
#             delta -= len(results)
#
#         results.update(remote)
#         self.proxies = results
#         logging.info('proxy server proxies')
#         return self.proxies.keys()
#
#     @classmethod
#     def from_crawer(cls, crawler):
#         return cls(crawler.settings)
#
#     def process_request(self, request, spider):
#         enabled = getattr(sjs.settings, 'PROXY_ENABLED', None)
#         if enabled is None or not enabled:
#             return
#         if 'www.yitiku.cn' not in request.url and \
#             'ip138.com' not in request.url and \
#             'httpbin.org' not in request.url:
#             return
#         if 'proxy' in request.meta:
#             return
#         proxy = getattr(sjs.settings, 'HTTP_PROXY', None)
#         if proxy is None:
#             proxy = random.choice(self.proxy_list)
#         logging.info('proxy-----%s' % proxy)
#         request.meta['proxy'] = proxy
#
#     def process_exception(self, request, exception, spider):
#         if 'proxy' in request.meta:
#             proxy = request.meta['proxy']
#             logging.info('Removeing failed proxy <%s>, %d proxy left' % (proxy, len(self.proxies)))
#             self.baned_list[proxy] = 1
#             try:
#                 del self.proxies[proxy]
#             except KeyError:
#                 pass
#             query = Query(ProxyNode)
#             query.equal_to('proxy', proxy)
#             try:
#                 one = query.first()
#             except:
