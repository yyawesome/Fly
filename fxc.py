#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from datetime import datetime
import tushare as ts
import math

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
        if (max-min)/min > 0.2:
            is_mad = True
            days = data[idx_max:].shape[0]

    return is_mad, days

maxn = None
minn = None

def rmq(arr):
    global maxn, minn

    n = len(arr)
    k = int(math.log(n * 1.0) / math.log(2.0))
    maxn = np.zeros((10000, 32))
    minn = np.zeros((10000, 32))
    for i in xrange(n):
        maxn[i][0] = arr[i]
        minn[i][0] = arr[i]
    for j in xrange(1, k+1, 1):
        for i in xrange(n):
            if (i + (1 << (j-1)) < n):
                maxn[i][j] = max(maxn[i][j - 1], maxn[i + (1 << (j - 1))][j - 1])
                minn[i][j] = min(minn[i][j - 1], minn[i + (1 << (j - 1))][j - 1])

def get_mad_bull_idx(arr, start, end):
    rmq(arr)

    k = int(math.log(end - start + 1.0) / math.log(2.0))
    v_max = max(maxn[start][k], maxn[end - (1 << k) + 1][k])
    v_min = min(minn[start][k], minn[end - (1 << k) + 1][k])

    return v_max, v_min

def compute_mad_bull_factor(df, days):
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D').strftime('%Y-%m-%d')
    df = pd.DataFrame(data=df, index=dates)  # 获取半年内数据
    df = df.dropna()  # 剔除非开盘日

    df['mad_bull'] = -1
    df['price_back'] = -1
    df['volume_pct'] = -1

    data = df['close']
    rmq(data)

    for i in xrange(df.shape[0] - 15):
        sub_data = data[i:i + 15]
        max = sub_data.max()
        idx_max = sub_data.idxmax()
        min = sub_data[:idx_max].min()  # 最小值应该在最大值前面
        if (max - min) / min > 0.5:
            days = df[idx_max:].shape[0]
            df.iloc[[i]]


    print df

if __name__ == '__main__':
    # print is_mad_bull('603393')
    # stock = ts.get_hist_data(code='603393')
    # result = compute_mad_bull_factor(stock, 180)
    # print result
    a = np.array([3,2,4,5,6,8,1,2,9,7])

    print get_mad_bull_idx(a, 0, 5)


