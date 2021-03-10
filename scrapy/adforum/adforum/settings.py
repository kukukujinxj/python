# -*- coding: utf-8 -*-

# Scrapy settings for adforum project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'adforum'

SPIDER_MODULES = ['adforum.spiders']
NEWSPIDER_MODULE = 'adforum.spiders'

IMAGES_STORE = "E:/myProjects/PythonProject/python/untitled/adforum/data/pic/"
FILES_STORE = "E:/myProjects/PythonProject/python/untitled/adforum/data/video/"

MYSQL_HOST = "localhost"
MYSQL_DBNAME = "ad_guider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"

# SPLASH_URL = 'http://localhost:8050'
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

DOWNLOAD_TIMEOUT = 1800

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'adforum (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32
# CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_DOMAIN = 4
CONCURRENT_REQUESTS_PER_IP = 16
# CONCURRENT_REQUESTS_PER_IP = 4

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Language': 'en',
    ':scheme': 'https',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://cn.adforum.com/creative-work/search?brand=&media_strkey=&location=&activity_strkey=&agname=&award=&companycredits=&peoplecredits=&advertiser=&title=&yearange=1999-2019&keyword=&o=relevance',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'Cookie': '_ga=GA1.2.2110938729.1558754033; __gads=ID=7216308c2eeb3e66:T=1558754487:S=ALNI_MbAZxK2ZSE7AnrQnb_g_YPSxAGFig; _gid=GA1.2.1273062064.1558922868; __stripe_mid=0cd7b667-8bab-401b-b226-9aade9da1262; FWKCountry=CN; XSRF-TOKEN=eyJpdiI6IlVIaSt2dEdjb2FSTTNmMUQ1Z21xRmc9PSIsInZhbHVlIjoiRUp6WDBWTExlRlhQc1BlRitiZXN2K0U0RmlQSU9kUnhSYndMNmI1ZFNZUmNOTW5wSFd2cVhDcURRajNrdlRiQXJvWDZCODZqQlJcL0dvYmV4b1wvbjF6Zz09IiwibWFjIjoiYTNjMmUxM2MyZDM1ZDc2YjE1MjYxZDkyMzRmMTM3OTkyYjEzM2E5NjMxZWZiZTExYWI1ZjVkOTRkMDllOWYwMiJ9; adforum_session=eyJpdiI6IncrQVdhZnZtcnZmZ1lJTXJ1YTl6dUE9PSIsInZhbHVlIjoiUDFTSVpXTW51KzJKZENcL05vb1FmS3pMNTVNTndzTG9oOFVSSFNOcThtWEpWaXI1MXI3eFdOaXB0ZWlyZUxrRTBMR0dMb2M0S2ZTQXB4bTd1aG9FbFhnPT0iLCJtYWMiOiJlNWVkZWIxOGM3MzBmNTE0NjM5ZWRlMWM5OWVjNmEzODRlNTc1MTUzOTc2NDBlMjRmODFjYmJiNTU3NjIyNGNlIn0%3D; _gat=1',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'adforum.middlewares.AdforumSpiderMiddleware': 543,
    # 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'adforum.middlewares.AdforumDownloaderMiddleware': 543,
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'adforum.pipelines.AdforumPipeline': 300,
    'adforum.pipelines.AdforumImagesPipeline': 400,
    'adforum.pipelines.AdforumFilesPipeline': 500,
    'adforum.pipelines.MysqlTwistedPipeline': 600,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 16.0
# AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
