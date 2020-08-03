# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviepanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    types = scrapy.Field()  # 类型
    name = scrapy.Field() #标题
    link_pan = scrapy.Field() #链接
    link = scrapy.Field()  # 链接
    disk_pan = scrapy.Field()  # 网盘
    pan_m = scrapy.Field()
    pan_list = scrapy.Field()
    magnet_list = scrapy.Field()