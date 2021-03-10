# -*- coding: utf-8 -*-
import scrapy

from ..items import TencentItem


class TencentspiderSpider(scrapy.Spider):
    name = 'tencentspider'
    allowed_domains = ['tencent.com']
    baseUrl = "https://hr.tencent.com/position.php?lid=&tid=&keywords=%E8%AF%B7%E8%BE%93%E5%85%A5%E5%85%B3%E9%94%AE%E8%AF%8D&start=0"
    offset = 0
    start_urls = [baseUrl + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = TencentItem()

            item['positionName'] = node.xpath("./td[1]/a/text()").extract()[0]
            item['positionLink'] = node.xpath("./td[1]/a/@href").extract()[0]
            if len(node.xpath("./td[2]/text()")):
                item['positionType'] = node.xpath("./td[2]/text()").extract()[0]
            else:
                item['positionType'] = ""
            item['peopleNumber'] = node.xpath("./td[3]/text()").extract()[0]
            item['workLocation'] = node.xpath("./td[4]/text()").extract()[0]
            item['publishTime'] = node.xpath("./td[5]/text()").extract()[0]

            yield item

        # if self.offset < 20:
        #     self.offset += 10
        #     url = self.baseUrl + str(self.offset)
        #     yield scrapy.Request(url, callback=self.parse)

        if not len(response.xpath("//a[@class='noactive' and @id='next']")):
            url = response.xpath("//a[@id='next']/@href").extract()[0]
            yield scrapy.Request("https://hr.tencent.com/" + url, callback=self.parse)
