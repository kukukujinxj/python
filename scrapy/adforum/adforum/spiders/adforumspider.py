# -*- coding: utf-8 -*-
import hashlib
import json
import re
import time
import uuid

import scrapy
from scrapy import Selector

from mysqltest import execute
from ..items import AdforumItem


class AdforumspiderSpider(scrapy.Spider):
    name = 'adforumspider'
    allowed_domains = ['cn.adforum.com']
    # start_urls = ['https://cn.adforum.com/creative-work/search?yearange=1999-2019&o=relevance']
    # cookie = 'FWKCountry=CN; _ga=GA1.2.2110938729.1558754033; _gid=GA1.2.174028449.1558754033; __gads=ID=7216308c2eeb3e66:T=1558754487:S=ALNI_MbAZxK2ZSE7AnrQnb_g_YPSxAGFig; _gat=1; XSRF-TOKEN=eyJpdiI6IlZ4NWtrWDFTdVkwdzk0cjdxQXB1cHc9PSIsInZhbHVlIjoiVmZESEhMM0Z1V1NGS1FjK3pVcndoVUo5bWlpVTdpQXo4TDd4YkdRb2lLRm5WXC9DRCtoMm5GSzEwVDBoQkdcLzdWK1gxSU1cL2NQS1RJTmRzM2NpUmtxWnc9PSIsIm1hYyI6IjJjNTczY2I1NjI3YmQ5ZjIzNmI4MTYwNmRlYmM4YzQyN2VlYmY5MGFkMTUwZjdlZmNhY2ZjY2JkMTM2YjE2M2IifQ%3D%3D; adforum_session=eyJpdiI6Ik8ydDM3TnEwS04rS1RIVVwvQWFFWUF3PT0iLCJ2YWx1ZSI6InVuUFlpYWlEQThYbXN0QW0yWkVQSlYrVzk2RjJPcjZCQWJxZWFSWDB5K1c4cUIzS01YN3I0SW1VNFJEbTZMSkFBbnorNHk4S0tyR2pSSXdnVTR5QnV3PT0iLCJtYWMiOiI2N2UzNTMyMGM1NWIxZjk3MDIzMDVmMzQ5ZTdmYjAxNTgwZGM5MTkzYzQyMGFkNWYyN2I5ZTNkOTVkNzJmYjg3In0%3D'
    baseUrl = 'https://cn.adforum.com/search/find/loadmore?yearange=1999-2019&o=relevance&e=creative-work&rtpl=ListAds&l=25&p='
    index = 1
    start_urls = [baseUrl + str(index)]

    # def start_requests(self):
    #     script = """
    #                 function main(splash)
    #                     splash:set_viewport_size(1028, 10000)
    #                     splash:go(splash.args.url)
    #                     local scroll_to = splash:jsfunc("window.scrollTo")
    #                     scroll_to(0, 2000)
    #                     splash:wait(15)
    #                     return {
    #                         html = splash:html()
    #                     }
    #                 end
    #                 """
    #
    #     for url in self.start_urls:
    #         yield SplashRequest(url, callback=self.parse, cookies={'cookie': self.cookie}, meta={
    #             'dont_redirect': True,
    #             'splash': {
    #                 'args': {'lua_source': script, 'images': 0},
    #                 'endpoint': 'execute',
    #                 'url': url
    #             }
    #         })

    def parse(self, response):
        rp = json.loads(response.text)['html']
        sl = Selector(text=rp)
        node_list = sl.xpath("//div[@class='col-lg-4 col-md-4 col-sm-4 col-xs-6']")
        for node in node_list:
            current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            item = AdforumItem()
            item['caTitle'] = ''
            item['caPostDate'] = current_time
            item['caResources'] = ''
            item['caOriginalUrl'] = ''
            item['caCampaign'] = ''
            item['caCategory'] = ''
            item['caMedia'] = ''
            item['caLanguage'] = ''
            item['caPlatform'] = ''
            item['caAgency'] = ''
            item['caMade'] = ''
            item['caLabel'] = ''
            item['caUID'] = ''
            item['caDesc'] = ''
            item['caDetail'] = ''
            item['caParters'] = ''
            item['caPrize'] = ''
            item['caRefer'] = ''
            item['imageSmall'] = node.xpath(".//img/@data-src").extract_first()
            image = node.xpath(".//img/@data-src").extract_first()
            if image is not None:
                name = hashlib.md5(image.encode('utf-8'))
                item['caResources'] = '{"mdType":1,"pic":["/codespace/product/' + str(
                    current_time) + '/pic/' + str(name.hexdigest()) + '.jpg"]}'
                item['icon'] = '/' + str(name.hexdigest()) + '.jpg'
            else:
                item['caResources'] = ''
            url = node.xpath(".//a[@class='b-latest-ads__item__link']/@href").extract_first()
            if url is not None:
                url = 'https://cn.adforum.com' + url
                item['caOriginalUrl'] = url
                # time.sleep(1)
                sql_cmd = 'SELECT * FROM ad_guider.ad_case WHERE caOriginalUrl = %s'
                param = (url,)
                ret = execute(sql_cmd, param, 'select')
                if len(ret) == 0:
                    yield scrapy.Request(url, meta={"item": item}, callback=self.sonparse)

        if self.index < 7812:
            self.index += 1
            url = self.baseUrl + str(self.index)
            print('==================================>' + url)
            yield scrapy.Request(url, callback=self.parse)

    def sonparse(self, response):
        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item = response.meta['item']
        item['caTitle'] = response.xpath("//span[@class='quotes']/text()").extract_first()
        infos = response.xpath("//tr").extract()
        # infoValue = response.xpath("//tr/td[@class='value' and not(@itemprop='description')]//text()").extract()
        # infoValue = ';'.join(infoValue)
        # infoValue = re.sub(r"([\r\n+])", '', infoValue)
        # infoValue = re.sub(r"([\r\n\s]{2,})", '', infoValue)
        # infoValue = re.sub(r"(;{2,})", ';', infoValue)
        # infoValue = infoValue.strip(";")
        # infoValue = infoValue.split(";")
        i = 0
        role1 = []
        role2 = []
        role3 = []
        role4 = []
        role5 = []
        role6 = []
        role7 = []
        role8 = []
        role9 = []
        role10 = []
        role11 = []
        role12 = []
        role13 = []
        role14 = []
        role15 = []
        role16 = []
        role17 = []
        role18 = []
        role19 = []
        role20 = []
        role22 = []
        role23 = []
        role24 = []
        role25 = []
        role37 = []
        role38 = []
        role48 = []
        parter = '['
        referList = []
        for info in infos:
            if i >= len(infos):
                break
            info = Selector(text=info)
            key = info.xpath("//td[@class='key']/text()").extract_first()
            if key is not None:
                key = key.strip()
            else:
                key = ''
            key = key.strip()
            value = info.xpath("//td[@class='value']//text()").extract()
            if value is not None:
                value = ''.join(value)
                value = re.sub(r"([\r\n\s]{2,})", '', value)
                value = value.strip()
            else:
                value = ''
            if key == '??????':
                item['caTitle'] = value
            elif key == 'Posted':
                posted = value.split("???")
                if len(posted[0].strip()) < 2:
                    posted[0] = '0' + posted[0].strip()
                posted = posted[-1].strip() + '-' + posted[0].strip() + '-01'
                item['caPostDate'] = posted
            elif key == '??????????????????':
                posted = value.split("/")
                if len(posted[-1].strip()) < 2:
                    posted[-1] = '0' + posted[-1].strip()
                posted = posted[0].strip() + '-' + posted[-1].strip() + '-01'
                item['caPostDate'] = posted
            elif key == '????????????':
                item['caCampaign'] = '[{"' + value + '":-1}]'
            elif key == '????????????':
                item['caCategory'] = '[{"id":-1,"title":"' + value + '","level":-1}]'
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                if value.strip() == '?????????':
                    item['caMedia'] = '[{"?????????":1}]'
                elif value.strip() == '?????????':
                    item['caMedia'] = '[{"?????????":2}]'
                elif value.strip() == 'vlog':
                    item['caMedia'] = '[{"vlog":3}]'
                elif value.strip() == '?????????':
                    item['caMedia'] = '[{"?????????":4}]'
                elif value.strip() == 'TVC':
                    item['caMedia'] = '[{"TVC":5}]'
                elif value.strip() == '??????':
                    item['caMedia'] = '[{"??????":6}]'
                elif value.strip() == '??????':
                    item['caMedia'] = '[{"??????":7}]'
                elif value.strip() == '??????':
                    item['caMedia'] = '[{"??????":8}]'
                elif value.strip() == '??????':
                    item['caMedia'] = '[{"??????":9}]'
                elif value.strip() == '??????':
                    item['caMedia'] = '[{"??????":10}]'
                elif value.strip() == '??????':
                    item['caMedia'] = '[{"??????":12}]'
                elif value.strip() == '??????':
                    item['caMedia'] = '[{"??????":13}]'
                elif value.strip() == 'H5':
                    item['caMedia'] = '[{"H5":14}]'
                elif value.strip() == 'APP':
                    item['caMedia'] = '[{"APP":15}]'
                elif value.strip() == '?????????':
                    item['caMedia'] = '[{"?????????":16}]'
                elif value.strip() == '??????':
                    item['caMedia'] = '[{"??????":17}]'
                else:
                    item['caMedia'] = '[{"' + value + '":-1}]'
            elif key == '????????????':
                item['caAgency'] = '[{"' + value + '":-1}]'
            elif key == '????????????':
                item['caMade'] = '[{"' + value + '":-1}]'
            elif key == '????????????':
                item['caDesc'] = value
            elif key == '???????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role1.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role2.append('"' + value + '"')
            elif key == '??????????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role3.append('"' + value + '"')
            elif key == '??????????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role4.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role5.append('"' + value + '"')
            elif key == '?????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role6.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role7.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role8.append('"' + value + '"')
            elif key == '???????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role9.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role10.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role11.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role12.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role13.append('"' + value + '"')
            elif key == '??????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role14.append('"' + value + '"')
            elif key == '??????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role15.append('"' + value + '"')
            elif key == '??????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role16.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role17.append('"' + value + '"')
            elif key == '?????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role18.append('"' + value + '"')
            elif key == '?????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role19.append('"' + value + '"')
            elif key == '?????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role20.append('"' + value + '"')
            elif key == '?????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role22.append('"' + value + '"')
            elif key == '?????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role23.append('"' + value + '"')
            elif key == '?????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role24.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role25.append('"' + value + '"')
            elif key == '?????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role37.append('"' + value + '"')
            elif key == '?????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role38.append('"' + value + '"')
            elif key == '????????????':
                while len(value) >= 60:
                    if i >= len(infos):
                        break
                    i += 1
                role48.append('"' + value + '"')
            else:
                referList.append('{"' + key + '":"' + value + '"}')
            i += 1
        countries = response.xpath("//ul[@class='list-unstyled featured_video__list']/li").extract()
        if countries is not None:
            for country in countries:
                country = Selector(text=country)
                key = country.xpath("//strong/text()").extract_first()
                value = country.xpath("//*[not(name()='strong')]/text()").extract_first()
                if key is not None and key == '??????:':
                    referList.append('{"??????":"' + value.strip() + '"}')
        if len(referList) > 0:
            item['caRefer'] = '[' + ','.join(referList) + ']'
        # desc = response.xpath("//tr/td[@itemprop='description']//text()").extract()
        # if desc is not None and len(desc) > 0:
        #     desc = ''.join(desc)
        #     desc = re.sub(r"([\r\n\s+])", ' ', desc)
        #     item['caDesc'] = desc
        # else:
        #     item['caDesc'] = ''
        if len(role1) > 0:
            role1 = ','.join(role1)
            role1 = re.sub('","', ',', role1)
            parter += '{"???????????????":' + role1 + '},'
        if len(role2) > 0:
            role2 = ','.join(role2)
            role2 = re.sub('","', ',', role2)
            parter += '{"????????????":' + role2 + '},'
        if len(role3) > 0:
            role3 = ','.join(role3)
            role3 = re.sub('","', ',', role3)
            parter += '{"??????????????????":' + role3 + '},'
        if len(role4) > 0:
            role4 = ','.join(role4)
            role4 = re.sub('","', ',', role4)
            parter += '{"??????????????????":' + role4 + '},'
        if len(role5) > 0:
            role5 = ','.join(role5)
            role5 = re.sub('","', ',', role5)
            parter += '{"????????????":' + role5 + '},'
        if len(role6) > 0:
            role6 = ','.join(role6)
            role6 = re.sub('","', ',', role6)
            parter += '{"?????????":' + role6 + '},'
        if len(role7) > 0:
            role7 = ','.join(role7)
            role7 = re.sub('","', ',', role7)
            parter += '{"????????????":' + role7 + '},'
        if len(role8) > 0:
            role8 = ','.join(role8)
            role8 = re.sub('","', ',', role8)
            parter += '{"????????????":' + role8 + '},'
        if len(role9) > 0:
            role9 = ','.join(role9)
            role9 = re.sub('","', ',', role9)
            parter += '{"???????????????":' + role9 + '},'
        if len(role10) > 0:
            role10 = ','.join(role10)
            role10 = re.sub('","', ',', role10)
            parter += '{"????????????":' + role10 + '},'
        if len(role11) > 0:
            role11 = ','.join(role11)
            role11 = re.sub('","', ',', role11)
            parter += '{"????????????":' + role11 + '},'
        if len(role12) > 0:
            role12 = ','.join(role12)
            role12 = re.sub('","', ',', role12)
            parter += '{"????????????":' + role12 + '},'
        if len(role13) > 0:
            role13 = ','.join(role13)
            role13 = re.sub('","', ',', role13)
            parter += '{"????????????":' + role13 + '},'
        if len(role14) > 0:
            role14 = ','.join(role14)
            role14 = re.sub('","', ',', role14)
            parter += '{"??????":' + role14 + '},'
        if len(role15) > 0:
            role15 = ','.join(role15)
            role15 = re.sub('","', ',', role15)
            parter += '{"??????":' + role15 + '},'
        if len(role16) > 0:
            role16 = ','.join(role16)
            role16 = re.sub('","', ',', role16)
            parter += '{"??????":' + role16 + '},'
        if len(role17) > 0:
            role17 = ','.join(role17)
            role17 = re.sub('","', ',', role17)
            parter += '{"????????????":' + role17 + '},'
        if len(role18) > 0:
            role18 = ','.join(role18)
            role18 = re.sub('","', ',', role18)
            parter += '{"?????????":' + role18 + '},'
        if len(role19) > 0:
            role19 = ','.join(role19)
            role19 = re.sub('","', ',', role19)
            parter += '{"?????????":' + role19 + '},'
        if len(role20) > 0:
            role20 = ','.join(role20)
            role20 = re.sub('","', ',', role20)
            parter += '{"?????????":' + role20 + '},'
        if len(role22) > 0:
            role22 = ','.join(role22)
            role22 = re.sub('","', ',', role22)
            parter += '{"?????????":' + role22 + '},'
        if len(role23) > 0:
            role23 = ','.join(role23)
            role23 = re.sub('","', ',', role23)
            parter += '{"?????????":' + role23 + '},'
        if len(role24) > 0:
            role24 = ','.join(role24)
            role24 = re.sub('","', ',', role24)
            parter += '{"?????????":' + role24 + '},'
        if len(role25) > 0:
            role25 = ','.join(role25)
            role25 = re.sub('","', ',', role25)
            parter += '{"????????????":' + role25 + '},'
        if len(role37) > 0:
            role37 = ','.join(role37)
            role37 = re.sub('","', ',', role37)
            parter += '{"?????????":' + role37 + '},'
        if len(role38) > 0:
            role38 = ','.join(role38)
            role38 = re.sub('","', ',', role38)
            parter += '{"?????????":' + role38 + '},'
        if len(role48) > 0:
            role48 = ','.join(role48)
            role48 = re.sub('","', ',', role48)
            parter += '{"????????????":' + role48 + '},'
        parter = parter.strip(',')
        parter += ']'
        item['caParters'] = parter
        languageInfos = response.xpath("//div[@class='featured_video__footer']//li/text()").extract()
        languageStr = ''
        # if languageInfos is not None:
        #     for language in languageInfos:
        #         language = language.strip()
        #         if language == '??????':
        #             languageStr = '[{"??????":1}]'
        #         if language == '??????':
        #             languageStr = '[{"??????":2}]'
        #         if language == '??????':
        #             languageStr = '[{"??????":3}]'
        #         if language == '?????????':
        #             languageStr = '[{"??????":4}]'
        #         if language == '??????':
        #             languageStr = '[{"??????":5}]'
        #         if language == '??????':
        #             languageStr = '[{"??????":6}]'
        #         if language == '?????????':
        #             languageStr = '[{"????????????":7}]'
        #         if language == '??????':
        #             languageStr = '[{"?????????":8}]'
        # if languageStr == '':
        #     languageStr = '[{"??????":2}]'
        item['caLanguage'] = languageStr
        item['caPlatform'] = '[{"??????":18}]'
        item['caLabel'] = ''
        item['caUID'] = str(uuid.uuid1())
        detail = response.xpath("//div[@class='featured_video__content']").extract_first()
        item['images'] = response.xpath("//img[@itemprop='contentUrl']/@src | //video/@poster").extract()
        item['file_urls'] = response.xpath("//video/source/@src").extract()
        if detail is not None:
            if item['images'] is not None and item['images'] != '':
                for image in item['images']:
                    count = re.findall(image, detail)
                    if len(count) > 0:
                        detail = re.sub(image,
                                        '77code_space_editor_place77/codespace/product/{currentdate}/pic/' +
                                        image.split('/')[-1], detail)
            if item['file_urls'] is not None and item['file_urls'] != '':
                for file_url in item['file_urls']:
                    count = re.findall(file_url, detail)
                    if len(count) > 0:
                        detail = re.sub(file_url, '77code_space_editor_place77/codespace/product/{currentdate}/video/' +
                                        file_url.split('/')[-1], detail)
            detail = re.sub('{currentdate}', str(current_time), detail)
            item['caDetail'] = detail
        else:
            item['caDetail'] = ''
        awardUrl = response.xpath("//li[contains(@id,'_awards')]/a/@data-par").extract_first()
        if awardUrl is not None:
            yield scrapy.Request('https://cn.adforum.com' + str(awardUrl), meta={"item": item},
                                 callback=self.awardparse)
        # yield scrapy.Request('https://cn.adforum.com/public/afup_render/tab/awards/34544953', meta={"item": item},
        #                      callback=self.awardparse)

    def awardparse(self, response):
        item = response.meta['item']
        prizeInfos = response.xpath("//div[@class='afup-tab-award p-b-sm']").extract()
        prizeList = []
        if prizeInfos is not None and len(prizeInfos) > 0:
            for prizeInfo in prizeInfos:
                prizeInfo = Selector(text=prizeInfo)
                str = '{"_aprTitle":"'
                awardName = prizeInfo.xpath("//div[@class='award_name']/a/text()").extract_first()
                str += awardName + '","_bperiod":"'
                awardKeys = prizeInfo.xpath("//div[@class='media-body small']//strong/text()").extract()
                awardValue = prizeInfo.xpath("//div[@class='media-body small']//span/text()").extract()
                awardValue = ';'.join(awardValue)
                awardValue = re.sub(r"([\r\n+])", '', awardValue)
                awardValue = re.sub(r"([\r\n\s]{2,})", '', awardValue)
                awardValue = re.sub(r"(;{2,})", ';', awardValue)
                awardValue = awardValue.strip(";")
                awardValue = awardValue.split(";")
                n = 0
                for awardKey in awardKeys:
                    if awardKey == '??????:':
                        str += awardValue[n] + '","_choner":"'
                    if awardKey == '??????:':
                        str += awardValue[n] + '"}'
                    n += 1
                prizeList.append(str)
        prizeSet = set(prizeList)
        prizeList = list(prizeSet)
        if len(prizeList) > 0:
            item['caPrize'] = '[' + ','.join(prizeList) + ']'
        yield item
