# -*- coding: utf-8 -*-
import datetime
import re
import time
import uuid

import scrapy

from mysqltest import execute
from ..items import AdsoftItem


class AdsoftspiderSpider(scrapy.Spider):
    name = 'adsoftspider'
    allowed_domains = ['www.adsoftheworld.com']
    start_urls = ['https://www.adsoftheworld.com/']

    def parse(self, response):
        node_list = response.xpath("//article")
        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        for node in node_list:
            item = AdsoftItem()
            item['imageSmall'] = node.xpath("//div[@class='view-content']//img/@src").extract_first()
            image = node.xpath(".//div[@class='content']/a/img/@src").extract_first()
            if image is not None:
                image = image.split('/')
                item['caResources'] = '{"mdType":1,"pic":["/codespace/product/' + str(
                    current_time) + '/pic/' + image[len(image) - 1] + '"]}'
                item['caResources'] = item['caResources'].split('?')[0] + '"]}'
            else:
                item['caResources'] = '{"mdType":1,"pic":[""]}'
            url = node.xpath(".//div[@class='field-name-title']/h4/a/@href").extract_first()
            if url is not None:
                item['caOriginalUrl'] = url
                sql_cmd = 'SELECT * FROM ad_guider.ad_case_refer WHERE caRefer = %s'
                param = (url,)
                ret = execute(sql_cmd, param, 'select')
                if not len(ret):
                    yield scrapy.Request(url, meta={"item": item}, callback=self.sonparse)

        if len(response.xpath("//a[@title='Go to next page']/text()")):
            url = response.xpath("//a[@title='Go to next page']/@href").extract_first()
            print('==================================>' + url)
            yield scrapy.Request("https://www.adsoftheworld.com/" + url, callback=self.parse)

    def sonparse(self, response):
        item = response.meta['item']
        item['caTitle'] = response.xpath("//h1/text()").extract_first()
        postdate = response.xpath(
            "//div[@class= 'field field-name-post-date field-type-ds field-label-inline clearfix']/div/div/text()").extract_first().strip()
        item['caPostDate'] = datetime.datetime.strptime(postdate, '%B %d, %Y').strftime('%Y-%m-%d')
        agency = response.xpath("//div[@class= 'ds-header_left']/div/div/div/a/text()").extract_first()
        if len(str(agency)):
            agency = str(agency).strip()
        else:
            agency = ''
        item['caAgency'] = '[{"id":-1,"title":"' + agency + '"}]'
        item['caCampaign'] = '[{"id":-1,"title":""}]'
        item['caCategory'] = '[{"id":-1,"title":"","level":-1}]'
        media = response.xpath("//div[@class= 'view-content']/a[1]/text()").extract_first()
        if media == 'Print':
            item['caMedia'] = '[{"平面": 7}]'
        elif media == 'Outdoor':
            item['caMedia'] = '[{"户外": 8}]'
        else:
            item['caMedia'] = '[{"TVC": 5}]'
        item['caLanguage'] = '[{"英语":2}]'
        item['caPlatform'] = '[{"网络":18}]'
        # creditTitle = response.xpath("//div[@class= 'field-item']/span/text()").extract()
        # creditsName = response.xpath("//div[@class= 'field-item']/span/a/text()").extract()
        # if str(creditTitle).strip():
        #     creditTitle = creditTitle.replace(',', '').split('\n')
        #     creditsName = creditsName.split('\n')
        credits = response.xpath("//div[@class= 'field-item']//text()").extract()
        credits = ''.join(credits)
        credits = credits.split("\n")
        n = 0
        parter = '['
        name = '{"其他职位":"'
        made = ''
        for credit in credits:
            if credit.split(':')[0] == 'Chief Creative Officer':
                parter = parter + '{"首席创意官":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Creative Directors':
                parter = parter + '{"创意总监":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Executive Creative Director' or credit.split(':')[0] == 'ECD':
                parter = parter + '{"执行创意总监":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Co-Creative Director' or credit.split(':')[0] == 'ECD':
                parter = parter + '{"联合创意总监":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Art Directors':
                parter = parter + '{"美术指导":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Head of Design':
                parter = parter + '{"设计师":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Executive Producer':
                parter = parter + '{"执行制片":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Music Director':
                parter = parter + '{"音乐总监":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Music Producer':
                parter = parter + '{"音乐制作人":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Account Director':
                parter = parter + '{"客户总监":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Account Planner' or credit.split(':')[0] == 'Account Planning':
                parter = parter + '{"客户企划":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Account Manager':
                parter = parter + '{"客户经理":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Account Executive':
                parter = parter + '{"客户执行":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Director':
                parter = parter + '{"导演":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Editor':
                parter = parter + '{"编剧":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Actor':
                parter = parter + '{"演员":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Director Of Photography':
                parter = parter + '{"摄影指导":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Photography':
                parter = parter + '{"摄影师":"' + credit.split(':')[-1] + '"},'
            elif credit.split(':')[0] == 'Producer':
                made = credit.split(':')[-1]
            else:
                name += credit + ','
            n = n + 1
        if len(made):
            item['caMade'] = made
        else:
            item['caMade'] = ''
        if len(name) > 0:
            name = name[:-1]
        name += '"}'
        parter += name
        parter = parter + ']'
        item['caParters'] = parter
        item['caLabel'] = '['
        labelList = response.xpath("//div[@class='view-content']/a/text()").extract()
        for label in labelList:
            item['caLabel'] += '{"' + label + '": -1},'
        item['caLabel'] = item['caLabel'][:-1]
        item['caLabel'] += ']'
        item['caUID'] = str(uuid.uuid1())
        desc = response.xpath("//div[@class='group-body']//p/text()").extract_first()
        if not desc:
            desc = ''
        item['caDesc'] = desc
        detail = response.xpath("//div[@class='s3-media-wrapper']").extract_first()
        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        count = re.findall(r"(https://d3nuqriibqh3vw.cloudfront.net/styles/aotw_detail_ir/s3/)", str(detail))
        if len(count) > 0:
            detail = re.sub(r"(https://d3nuqriibqh3vw.cloudfront.net/styles/aotw_detail_ir/s3/)",
                            '77code_space_editor_place77/codespace/product/{currentdate}/pic/', detail)
        count = re.findall(r"(https://d3nuqriibqh3vw.cloudfront.net/)", str(detail))
        if len(count) > 0:
            detail = re.sub(r"(https://d3nuqriibqh3vw.cloudfront.net/)",
                            '77code_space_editor_place77/codespace/product/{currentdate}/pic/', detail)
        detail = re.sub('{currentdate}', str(current_time), detail)
        item['caDetail'] = re.sub(r"(\?[\S]*)", '"', detail)
        item['caPrize'] = '[{"name":"","index":"","grade":""}]'
        item['images'] = response.xpath(
            "//div[@class='s3-media-wrapper']//div/@poster | //div[@class='s3-media-wrapper']//img/@src").extract()
        item['file_urls'] = response.xpath("//div[@class='s3-media-wrapper']//video/source[1]/@src").extract()
        yield item
