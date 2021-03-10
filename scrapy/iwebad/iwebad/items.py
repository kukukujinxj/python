# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IwebadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    caTitle = scrapy.Field()
    caDesc = scrapy.Field()
    caPostDate = scrapy.Field()
    caDetail = scrapy.Field()
    caResources = scrapy.Field()
    caOriginalUrl = scrapy.Field()
    caLanguage = scrapy.Field()
    caPlatform = scrapy.Field()
    caAgency = scrapy.Field()
    caMade = scrapy.Field()
    caParters = scrapy.Field()
    caLabel = scrapy.Field()
    caUID = scrapy.Field()
    caCampaign = scrapy.Field()
    caCategory = scrapy.Field()
    caMedia = scrapy.Field()
    caPrize = scrapy.Field()
    images = scrapy.Field()
    imageSmall = scrapy.Field()
