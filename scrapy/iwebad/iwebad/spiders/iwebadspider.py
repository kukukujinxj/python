# -*- coding: utf-8 -*-
import re
import time
import uuid

import scrapy

from ..items import IwebadItem


class IwebadspiderSpider(scrapy.Spider):
    name = 'iwebadspider'
    allowed_domains = ['iwebad.com']
    # 案例
    start_urls = ['http://iwebad.com/case/']

    # TVC
    # baseUrl = "http://iwebad.com/video/index_"
    # pageNum = 1
    # start_urls = [baseUrl + str(pageNum) + '.html']

    def parse(self, response):
        node_list = response.xpath("//div[@class='works']")
        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        for node in node_list:
            item = IwebadItem()

            item['caTitle'] = node.xpath("./div/div/div/h4/a/text()").extract()[0].strip()
            item['caCampaign'] = '[{"id":-1,"title":"' + item['caTitle'] + '"}]'
            item['caDesc'] = node.xpath("./div/div[2]/text()").extract()[0].strip()
            item['caPostDate'] = node.xpath("./div/div/div/h4/span/text()").extract()[0].replace('/', '').strip()
            item['caCategory'] = '[{"id":-1,"title":"' + node.xpath("./div/div/div/a[1]/text()").extract()[0].replace(
                '/', '').strip() + '","level":-1}]'
            item['imageSmall'] = 'http://iwebad.com' + node.xpath("./div/a/img/@src").extract()[0].strip()
            imageSmall_list = node.xpath("./div/a/img/@src").extract()[0].strip().split('/')
            item['caResources'] = '{"mdType":1,"pic":["/codespace/product/' + str(current_time) + '/pic/' + \
                                  imageSmall_list[len(imageSmall_list) - 1] + '"]}'
            # 案例
            item['caOriginalUrl'] = "http://iwebad.com/case/"
            # TVC
            # item['caOriginalUrl'] = "http://iwebad.com/video/"
            item['caLanguage'] = '[{"汉语":1}]'
            item['caPlatform'] = '[{"网络":18}]'
            # 案例
            item['caAgency'] = '[{"id":-1,"title":"' + node.xpath("./div/div/div/a[2]/text()").extract()[
                0].strip() + '"}]'
            label_list = node.xpath("./div/div/div/a/text()").extract()
            flag = True
            item['caLabel'] = '['
            for label in label_list:
                if flag:
                    item['caLabel'] += '{"' + label + '": -1}'
                    flag = False
                else:
                    item['caLabel'] += ', {"' + label + '": -1}'
            item['caLabel'] += ']'
            url = node.xpath("./div/div/div/h4/a/@href").extract()[0]
            yield scrapy.Request(url, meta={"item": item}, callback=self.sonparse)

        # TVC
        # if self.pageNum < 172:
        #     self.pageNum += 1
        #     url = self.baseUrl + str(self.pageNum) + '.html'
        #     yield scrapy.Request(url, callback=self.parse)

    def sonparse(self, response):
        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item = response.meta['item']
        node_list = response.xpath("//div[@class='news_ckkk ']")
        item['caDetail'] = node_list.extract()[0].strip()
        # 案例
        res = re.sub(r"(/d/file/interactive-marketing/[\S]*-advertising/)", '77code_space_editor_place77{filepath}',
                     item['caDetail'])
        # TVC
        # res = re.sub(r"(/d/file/video/[\S]*/)", '77code_space_editor_place77{filepath}', item['caDetail'])
        file_path = '/codespace/product/%s/pic/' % str(current_time)
        item['caDetail'] = res.format(filepath=file_path)
        item['images'] = response.xpath("//p/img/@src").extract()
        # item['videos'] = response.xpath("//p/iframe/@src | //p/embed/@src").extract()[0]
        item['caMade'] = ''
        item['caParters'] = ''
        if response.xpath("//div[@class='fh nninfok']/div/div/span[2]/text()[2]"):
            item['caMade'] = response.xpath("//div[@class='fh nninfok']/div/div/span[2]/text()[2]").extract()[
                0].replace(':', '').strip()
            if item['caMade'] == '' or item['caMade'] == ':':
                item['caMade'] = response.xpath("//div[@class='fh nninfok']/div/div/span[2]/a[2]/text()").extract()[
                    0].replace(':', '').strip()
        if response.xpath("//div[@class='fh nninfok']/div/div/span/a[2]/text()"):
            item['caParters'] = response.xpath("//div[@class='fh nninfok']/div/div/span/a[2]/text()").extract()[
                0].strip()
        if item['caParters'] == '':
            item['caParters'] = '[{"其他职位":[""]}]'
        else:
            item['caParters'] = '[{"其他职位":["' + item['caParters'] + '"]}]'
        item['caMade'] = '[{"id":-1,"title":"' + item['caMade'] + '"}]'
        # TVC
        # item['caAgency'] = item['caMade']
        item['caUID'] = str(uuid.uuid1())
        item['caMedia'] = '[{"TVC": 5}]'
        item['caPrize'] = '[{"name":"","index":"","grade":""}]'
        yield item
