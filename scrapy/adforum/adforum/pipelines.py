# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time

import MySQLdb
import MySQLdb.cursors
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class AdforumPipeline(object):
    def process_item(self, item, spider):
        return item


class AdforumImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['imageSmall'] is not None and item['imageSmall'] != '':
            image_link = item['imageSmall']
            src = item['icon']
            yield scrapy.Request(image_link, meta={'src': src})
        image_list = item['images']
        for image in image_list:
            image_urls = image
            src = image_urls
            yield scrapy.Request(image_urls, meta={'src': src})

    def file_path(self, request, response=None, info=None):
        image_urls = request.meta['src'].split('/')[-1]
        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        filename = u'/{0}/{1}'.format(current_time, image_urls)
        return filename


class AdforumFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        video_list = item['file_urls']
        for video in video_list:
            file_urls = video
            src = file_urls
            yield scrapy.Request(file_urls, meta={'src': src})

    def file_path(self, request, response=None, info=None):
        video_urls = request.meta['src'].split('/')[-1]
        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        filename = u'/{0}/{1}'.format(current_time, video_urls)
        return filename


class MysqlTwistedPipeline(object):
    """docstring for MysqlTwistedPipeline"""

    # 采用异步的机制写入mysql
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        # insert_sql, params = item.get_insert_sql()
        # print (insert_sql, params)
        # cursor.execute(insert_sql, params)
        insert_sql = """INSERT INTO ad_guider.ad_case(caTitle,caPostDate,caResources,caOriginalUrl,caCampaign,caCategory,caMedia,caLanguage,caPlatform,caAgency,caMade,caLabel,caUID) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        # 可以只使用execute，而不需要再使用commit函数
        cursor.execute(insert_sql,
                       (item["caTitle"], item["caPostDate"], item["caResources"], item["caOriginalUrl"],
                        item["caCampaign"], item["caCategory"], item["caMedia"], item["caLanguage"], item["caPlatform"],
                        item["caAgency"], item["caMade"], item['caLabel'], item['caUID']))
        insert_sql = """SELECT caId FROM ad_guider.ad_case WHERE caUID = %s"""
        cursor.execute(insert_sql, (item["caUID"],))
        insertId = cursor.fetchone()
        insert_sql = """INSERT INTO ad_guider.ad_case_desc VALUES(%s,%s)"""
        cursor.execute(insert_sql, (insertId['caId'], item["caDesc"]))
        insert_sql = """INSERT INTO ad_guider.ad_case_detail VALUES(%s,%s)"""
        cursor.execute(insert_sql, (insertId['caId'], item["caDetail"]))
        insert_sql = """INSERT INTO ad_guider.ad_case_parter VALUES(%s,%s)"""
        cursor.execute(insert_sql, (insertId['caId'], item["caParters"]))
        insert_sql = """INSERT INTO ad_guider.ad_case_prize VALUES(%s,%s)"""
        cursor.execute(insert_sql, (insertId['caId'], item["caPrize"]))
        insert_sql = """INSERT INTO ad_guider.ad_case_refer VALUES(%s,%s)"""
        cursor.execute(insert_sql, (insertId['caId'], item["caRefer"]))
