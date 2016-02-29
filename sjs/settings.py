# -*- coding: utf-8 -*-

import logging
# Scrapy settings for sjs project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sjs'

SPIDER_MODULES = ['sjs.spiders']
NEWSPIDER_MODULE = 'sjs.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sjs (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN=16
CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
# COOKIES_ENABLED=False  # cookies一定要开启，否则在登陆网站抓取答案的时候会出错

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
# }
# PROXY_ENABLED = False
# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'sjs.middlewares.MyCustomSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# # See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     'sjs.middlewares.MyCustomDownloaderMiddleware': 543,
#     'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 544,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'sjs.middlewares.RotateUserAgentMiddleware': 560
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapy_qiniu.QiniuPipeline': 10,
    'sjs.pipelines.LeanCloudPipeline': 300
}

PIPELINE_QINIU_AK = '3xw5uASc565Mr44Vlt0iimqsZoBk3I0nM88YEjSP'
PIPELINE_QINIU_SK = 'ExEjTZG2QCVBktGMuM3YluorvQ28qQ5utK5mobRP'
PIPELINE_QINIU_ENABLED = 1
PIPELINE_QINIU_BUCKET = 'cache'
PIPELINE_QINIU_KEY_PREFIX = 'http://7xr69d.com1.z0.glb.clouddn.com/'

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
AUTOTHROTTLE_ENABLED=True
# The initial download delay
AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED=True
HTTPCACHE_EXPIRATION_SECS=0
HTTPCACHE_DIR='httpcache'
HTTPCACHE_IGNORE_HTTP_CODES=[]
HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.RFC2616Policy'
DOWNLOAD_TIMEOUT = 30
LOG_LEVEL = logging.DEBUG