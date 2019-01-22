# -*- coding: utf-8 -*-

"""
数据保存结果处理
"""

import pandas as pd
import time
import os


class GgpiaoPipeline(object):
    def __init__(self):
        self.recore_d = []
        self.Date = time.strftime('%Y%m%d')
        self.Recordpath = '.\\save\\'
        self.filename = 'Data' + self.Date
        if not os.path.exists(self.Recordpath):
            os.makedirs(self.Recordpath)

    def process_item(self, item, spider):
        recores = {}
        recores["名称"] = item["name"]
        recores["代码"] = item["code"]
        recores["涨幅"] = item["netChangeRatio"]
        recores["开盘"] = item["open"]
        recores["最高"] = item["high"]
        recores["最低"] = item["low"]
        recores["昨收"] = item["preClose"]
        recores["成交量"] = item["volume"]
        recores["收盘"] = item["close"]
        self.recore_d.append(recores)
        return item

    def open_spider(self, spider):
        print("open_spider...")
        pass

    def close_spider(self, spider):
        print("res>>>>>>>>>>>>>111: ", len(self.recore_d))
        df = pd.DataFrame(self.recore_d)
        df.to_excel(self.Recordpath + self.filename + '.xls', index=False)  # 未排名
        df["涨幅"] = df["涨幅"].apply(lambda x: float(str(x).replace("%", "")))
        df = df.sort_values(by=["涨幅"], ascending=[False])
        df["涨幅"] = df["涨幅"].apply(lambda x: str(x) + "%")
        df.to_excel(self.Recordpath + self.filename + '排名.xls', index=False)
        print("保存文件成功：", self.Recordpath)

        pass
