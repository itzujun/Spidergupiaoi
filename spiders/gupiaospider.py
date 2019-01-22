#  _*_  coding:utf-8_*_
"""
scrapy
"""

__author__ = "liuzujun"
__time__ = "2019.01.21 "

import scrapy

from ggpiao.items import GgpiaoItem
import json
import time


class GupiaoSpider(scrapy.Spider):
    #
    name = "gupiao"
    host = "http://quote.eastmoney.com/"
    start_urls = ["http://quote.eastmoney.com/stocklist.html"]

    def parse(self, response):
        for p in response.xpath("//div[@id='quotesearch']//a[@target='_blank']//text()").extract():
            name = p.split("(")[0]
            code = p.split("(")[1].split(")")[0]
            if not code.startswith("300") and not code.startswith("300000"):
                continue
            print("name:", name, "code:", code)
            url = "https://gupiao.baidu.com/api/stocks/stockdaybar?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code=" + \
                  "sz" + code + "&step=3&start=&count=160&fq_type=no&timestamp=" + str(int(time.time()))
            headers = {
                "Referer": "https://gupiao.baidu.com/stock/sz" + code + ".html",
                'Host': 'gupiao.baidu.com',
                'Origin': 'https://gupiao.baidu.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                "Cookie": "BAIDUID=343A7589AC95C6D6B68D1F76FE45C876:FG=1; BIDUPSID=343A7589AC95C6D6B68D1F76FE45C876; PSTM=1533821763; locale=zh; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; Hm_lvt_35d1e71f4c913c126b8703586f1d2307=1545643486,1546248867,1548122715; Hm_lpvt_35d1e71f4c913c126b8703586f1d2307=1548122715; PMS_JT=%28%7B%22s%22%3A1548122724560%2C%22r%22%3A%22https%3A//gupiao.baidu.com/%22%7D%29"
            }
            yield scrapy.Request(url=url, callback=self.parse_item, meta={"code": code, "name": name}, headers=headers)

    def parse_item(self, response):
        item = GgpiaoItem()
        if response.text is None:
            return
        js = json.loads(response.text)
        name = response.meta['name']
        code = response.meta['code']
        lis = js.get("mashData", "-")
        msg = lis[0].get("kline")
        item["name"] = name
        item["code"] = code
        item["netChangeRatio"] = str(format(float(msg.get("netChangeRatio", "-")), ".2f")) + "%"
        item["open"] = msg.get("open", "-")
        item["high"] = msg.get("high", "-")
        item["low"] = msg.get("low", "-")
        item["close"] = msg.get("close", "-")
        item["volume"] = msg.get("volume", "-")
        item["preClose"] = msg.get("preClose", "-")
        item["close"] = msg.get("close", "-")
        print("完成:", name, "  ", code)
        yield item
