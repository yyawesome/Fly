#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from datetime import datetime
import tushare as ts
import math

maxn = None
minn = None
maxidx = None
minidx = None

def st(arr):
    global maxn, minn, maxidx, minidx

    n = len(arr)
    k = int(math.log(n * 1.0) / math.log(2.0))
    maxn = np.zeros((n, 32))
    minn = np.zeros((n, 32))
    maxidx = np.zeros((n, 32), dtype=np.uint64)
    minidx = np.zeros((n, 32), dtype=np.uint64)

    for i in xrange(n):
        maxn[i][0] = arr[i]
        minn[i][0] = arr[i]
        maxidx[i][0] = i
        minidx[i][0] = i

    for j in xrange(1, k+1, 1):
        for i in xrange(n):
            if (i + (1 << (j-1)) < n):
                deta_i = (1 << (j - 1))

                max_values = [maxn[i][j - 1], maxn[i+deta_i][j - 1]]
                max_idxs = [maxidx[i][j - 1], maxidx[i+deta_i][j - 1]]
                maxn[i][j] = max(max_values)
                maxidx[i][j] = max_idxs[max_values.index(maxn[i][j])]

                min_values = [minn[i][j - 1], minn[i+deta_i][j - 1]]
                min_idxs = [minidx[i][j - 1], minidx[i+deta_i][j - 1]]
                minn[i][j] = min(min_values)
                minidx[i][j] = min_idxs[min_values.index(minn[i][j])]

#获取最大值及其位置
def get_mad_bull_max(start, end):

    k = int(math.log(end - start + 1.0) / math.log(2.0))

    v = int(end - (1 << k) + 1)
    max_values = [maxn[start][k], maxn[v][k]]
    max_idxs = [maxidx[start][k], maxidx[v][k]]
    v_max = max(max_values)
    idx_max = max_idxs[max_values.index(v_max)]

    return v_max, idx_max

#获取最小值及其位置
def get_mad_bull_min(start, end):

    k = int(math.log(end - start + 1.0) / math.log(2.0))

    v = int(end - (1 << k) + 1)
    min_values = [minn[start][k], minn[v][k]]
    min_idxs = [minidx[start][k], minidx[v][k]]
    v_min = min(min_values)
    idx_min = min_idxs[min_values.index(v_min)]

    return v_min, idx_min

def compute_mad_bull_factor(df, days):
    df_result = []

    for code in df['code'].drop_duplicates():
        df_code = df[df.code == code]
        start_date = (datetime.now() + pd.DateOffset(days=-180)).strftime('%Y-%m-%d')
        df_code = df_code[df_code.date > start_date]  # 获取半年内数据

        df_code['mad_bull'] = -1
        df_code['price_back'] = -1.0
        df_code['volume_pct'] = -1.0

        data = df_code['close'].values
        st(data)

        for i in xrange(data.shape[0] - 14):
            vmax, idxmax = get_mad_bull_max(i, i+14)
            vmin, idxmin = get_mad_bull_min(i, idxmax)

            if (vmax - vmin) / vmin > 0.5:
                df_code.at[idxmax, 'mad_bull'] = 0
                df_code.at[idxmax, 'price_back'] = 0.0
                df_code.at[idxmax, 'volume_pct'] = 1.0

        offset = -1
        volume = -1
        price = -1
        for i in xrange(data.shape[0]):
            if df_code.at[i, 'mad_bull'] == 0:
                offset = 0
                volume = df_code.at[i, 'volume']
                price = df_code.at[i, 'close']
                continue

            if offset == -1:
                continue
            else:
                offset += 1
                df_code.at[i, 'mad_bull'] = offset
                df_code.at[i, 'price_back'] = (price - df_code.at[i, 'close'])/price
                df_code.at[i, 'volume_pct'] = df_code.at[i, 'volume']/volume
        df_result.append(df_code)
    return pd.concat(df_result)

if __name__ == '__main__':
    # codes = ts.get_stock_basics().index
    # stocks = [ts.get_hist_data(code=code) for code in codes]

    df = ts.get_hist_data('603393').reset_index()
    df['code'] = '603393'
    df2 = ts.get_hist_data('300059').reset_index()
    df2['code'] = '603394'
    df3 = ts.get_hist_data('600340').reset_index()
    df3['code'] = '600340'

    dfa = pd.concat([df, df2, df3])

    result = compute_mad_bull_factor(dfa, 180)
    print result

    # a = np.array([3,2,4,5,6,8,1,2,9,7])
    #
    # print get_mad_bull_idx(a, 1, 8)


