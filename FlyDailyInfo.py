#!/usr/bin/python
import tushare as ts
import numpy as np

DAILY_LIMIT_P = 9.8  # 涨幅，实际上涨停应大于此数值
DAY_COL_KEY_HIGH = 'high'
DAY_COL_KEY_LOW = 'low'
DAY_COL_KEY_P = 'p_change'


def get_daily_limit_along_number(date=None):
    _day_all_df = ts.get_day_all(date)
    _number = _day_all_df[np.logical_and(_day_all_df[DAY_COL_KEY_HIGH] == _day_all_df[DAY_COL_KEY_LOW],
                                         _day_all_df[DAY_COL_KEY_P] > DAILY_LIMIT_P)].shape[0]
    return _number


if __name__ == '__main__':
    daily_limit_along_number = get_daily_limit_along_number()
    print(daily_limit_along_number)
