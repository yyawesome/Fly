#!/usr/bin/python
import tushare as ts
import numpy as np
import pandas as pd
from pandas import Series, DataFrame


# 统计非一字板的个数 一字板判定（涨停并且开盘涨幅大于8%）
# 根据一字板涨停条件抽取出一个df[date] 生成series 然后进行count，在将series根据date count 添加到原df
def get_daily_limit_along_factor(df):
    limit_df = df[np.logical_and(df['open'] >= 8,
                                 df['p_change'] > 9.8)]
    rest_df = df.drop(limit_df)['date']
    date_series = Series(rest_df)
    # 这个series包含了每个date中的非一字板个数
    date_num_series = date_series.value_counts()
    date_num_df = DataFrame({'date': date_num_series.index,
                             'daily_limit_along_factor': date_num_series.values})
    print(date_num_df)
    # 默认根据date作为两个表的key值进行连接合并
    return pd.merge(df, date_num_df)


if __name__ == '__main__':
    print("hello")
    # df = ts.get_hist_data('603283').reset_index()
    # df2 = ts.get_hist_data('002907').reset_index()
    # df3 = ts.get_hist_data('300664').reset_index()
    # df4 = ts.get_hist_data('603655').reset_index()
    # df5 = ts.get_hist_data('300433').reset_index()
    # df6 = ts.get_hist_data('600903').reset_index()
    # dfa = pd.concat([df, df2, df3, df4, df5, df6])
    # f = get_daily_limit_along_factor(dfa)
