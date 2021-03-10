# -*- coding: utf-8 -*-
import scrapy

from ..items import FindItem


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ["itcast.cn"]
    start_urls = ["http://www.itcast.cn/channel/teacher.shtml"]

    def parse(self, response):
        node_list = response.xpath("//div[@class='li_txt']")
        for node in node_list:
            item = FindItem()

            name = node.xpath("./h3/text()").extract()
            title = node.xpath("./h4/text()").extract()
            info = node.xpath("./p/text()").extract()

            item['name'] = name[0]
            item['title'] = title[0]
            item['info'] = info[0]

            yield item
