# -*- coding: utf-8 -*-

import time

# Scrapy settings for mySpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'govbuy_spider'

SPIDER_MODULES = ['govbuy_spider.spiders']
NEWSPIDER_MODULE = 'govbuy_spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 增加全局并发数,单序执行时，修改为1
CONCURRENT_REQUESTS = 32
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Cookie': 'CP_IsMobile=false; ASP.NET_SessionId=x1lpapmpqdumhawj5pxw5are; __RequestVerificationToken=IQ-xH1AdgP8W3AksCS9Qw6-yHqNdwCViZR7vIkb0_1DrzaXe2nrviNTtsMplqCNGKg7N6GAD2clNZGBs5J2N4bb25KA1; dpi=1; screenWidth=1920; screenHeight=1080; ai_user=2GpVL|2020-09-11T01:14:03.098Z; CP_TrackBrowser={"doNotShowLegacyMsg":false,"supportNewUI":true,"legacy":false,"isMobile":false}; _ga=GA1.2.468594231.1599786852; _gid=GA1.2.924705759.1599786852; nmstat=1599786896081; _pk_ses.2759.0fa5=*; viewportHeight=937; viewportWidth=1903; responsiveGhost=0; ai_session=nPTIJ|1599786852185|1599787600354.75; _pk_id.2759.0fa5=18b0892ea798fc4d.1599786873.1.1599787622.1599786873.'
}

USER_AGENT_LIST=[
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    # 'govbuy_spider.middlewares.GovbuySpiderSpiderMiddleware': 543,
    # 'govbuy_spider.middlewares.MyproxiesSpiderMiddleware': 300,
}


# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'govbuy_spider.middlewares.IngoreHttpRequestMiddleware': 543,
    # 'govbuy_spider.middlewares.MyproxiesSpiderMiddleware': 300,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'govbuy_spider.pipelines.GovbuySpiderPipeline': 100,
    # 'govbuy_spider.pipelines.DownloadFilesPipeline': 150,
    # 'govbuy_spider.pipelines.InsertDBPipeline': 200,
    # 'govbuy_spider.pipelines.Ceshi': 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# # 启用logging
# LOG_ENABLED = True
# # log编码
# LOG_ENCODING ='utf-8'
# # 设置日志路径
# LOG_FILE = "./debug"+time.strftime("%m-%d")+'.log'
# # 设置日志级别
# LOG_LEVEL = 'DEBUG'
# # log输出重定向,全部输出
# LOG_STDOUT = True

# 允许重定向，针对下载时候出现302状态， 无法下载的问题
MEDIA_ALLOW_REDIRECTS = True




# MYSQL_HOST = '192.168.30.140'
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'govbuy'
# MYSQL_USER = 'cao'
MYSQL_USER = 'root'
MYSQL_PASSWD = '920618hwl.'
# MYSQL_PASSWD = 'baocheng'  create database govbuy charset=utf8;






REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_DB = 9












# 文件下载路径
FILES_STORE = 'D:/doc&pdf&png/'


# 允许下载的文件扩展名
ALLOWED_FILE_NAME = ['.doc', '.pdf', '.docx', '.xls', '.xlsx', '.zip', '.pptx', '.jpg']

HTTPERROR_ALLOWED_CODES = [400]

# 文件下载大小
DOWNLOAD_WARNSIZE = 0

# 下载器超时时间
DOWNLOAD_TIMEOUT = 900
DOWNLOAD_FAIL_ON_DATALOSS = False

# 请求间隔
# DOWNLOAD_DELAY = 1

# 文件下载缓存时间
FILES_EXPIRES = 0
#
# COMMANDS_MODULE = 'govbuy_spider.commands'

TELNETCONSOLE_PORT = [4093, 4241]




IPPOOL=[
    {"ipaddr":"192.168.2.43:1088"},
    # {"ipaddr":"183.164.239.201:9999"},

]





