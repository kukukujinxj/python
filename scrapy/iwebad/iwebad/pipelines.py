# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import MySQLdb
import MySQLdb.cursors
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class IwebadPipeline(object):
    def __init__(self):
        self.f = open("G:/servlet_project/python/untitled/iwebad/data/iwebad_pipeline.json", "wb")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(content.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.f.close()


class IwebadImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_link = item['imageSmall']
        src = image_link
        yield scrapy.Request(image_link, meta={'src': src})
        image_list = item['images']
        for image in image_list:
            image_urls = 'http://iwebad.com' + image
            src = image_urls
            yield scrapy.Request(image_urls, meta={'src': src})

    # def item_completed(self, results, item, info):
    #     image_result = [x for ok, x in results if ok]
    #     print("*" * 50)
    #     print(results)
    #     print(image_result)
    #     print("*" * 50)
    #     for image in image_result:
    #         path_list = image['path'].split('/')[-1]
    #         url_list = image['url'].split('/')[-1]
    #         # print("*" * 50)
    #         # print(image)
    #         # print("*" * 50)
    #         os.rename(images_store + 'full/' + path_list, images_store + url_list)

    def file_path(self, request, response=None, info=None):
        image_urls = request.meta['src'].split('/')[-1]
        path = image_urls
        return path


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
        # print("*" * 50)
        # print(insertId)
        # print("*" * 50)
        insert_sql = """INSERT INTO ad_guider.ad_case_desc VALUES(%s,%s)"""
        cursor.execute(insert_sql, (insertId['caId'], item["caDesc"]))
        insert_sql = """INSERT INTO ad_guider.ad_case_detail VALUES(%s,%s)"""
        cursor.execute(insert_sql, (insertId['caId'], item["caDetail"]))
        insert_sql = """INSERT INTO ad_guider.ad_case_parter VALUES(%s,%s)"""
        cursor.execute(insert_sql, (insertId['caId'], item["caParters"]))
        insert_sql = """INSERT INTO ad_guider.ad_case_prize VALUES(%s,%s)"""
        cursor.execute(insert_sql, (insertId['caId'], item["caPrize"]))
