#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from datetime import datetime
import tushare as ts

def is_mad_bull(code):
    stock = ts.get_hist_data(code=code) #获取全部数据
    dates = pd.date_range(end=datetime.now(), periods=180, freq='D').strftime('%Y-%m-%d')
    data = pd.DataFrame(data=stock, index=dates) #获取半年内数据
    data = data.dropna() #剔除非开盘日

    is_mad = False #是否有疯牛
    days = -1 #距离结束的天数
    for i in xrange(data.shape[0]-15):
        sub_data = data['close'][i:i+15]
        max = sub_data.max()
        idx_max = sub_data.idxmax()
        min = sub_data[:idx_max].min() #最小值应该在最大值前面
        if (max-min)/min > 0.5:
            is_mad = True
            days = data[idx_max:].shape[0]

    return is_mad, days


if __name__ == '__main__':
    print is_mad_bull('603393')

