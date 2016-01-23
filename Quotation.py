# -*- coding: utf-8 -*-
import pandas as pd
import talib

#数据文件存储路径
QUOT_FILE_PATH = 'data/'

#获取行情
def get_quot(comb):
    quot = pd.DataFrame()
    for i, row in comb.iterrows():
        # df = pd.read_csv(QUOT_FILE_PATH + row.code + '.csv',
        #                  parse_dates=['date'],
        #                  date_parser=lambda x: pd.datetime.strptime(x, '%Y/%m/%d'))
        df = pd.read_csv(QUOT_FILE_PATH + row.code + '.csv', parse_dates=['date'])

        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        df[['open', 'high', 'low', 'close']] /= row.price_div
        df['code'] = row.code

        quot = quot.append(df, ignore_index=True)

    quot.set_index(['code', 'date'], inplace=True)
    quot.sort_index(inplace=True)
    return quot


# quot.to_csv('e:/tmp.csv')