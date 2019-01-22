# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GgpiaoItem(scrapy.Item):
    name = scrapy.Field()  # 名称
    code = scrapy.Field()  # 代码
    open = scrapy.Field()  # 开盘
    high = scrapy.Field()  # 最高
    low = scrapy.Field()  # 最低
    close = scrapy.Field()  # 收盘
    volume = scrapy.Field()  # 成交量
    preClose = scrapy.Field()  # 昨收
    netChangeRatio = scrapy.Field()  # 涨幅

    pass
