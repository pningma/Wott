# -*- coding: utf-8 -*-
import pandas as pd
# import numpy as np
# from sqlalchemy import create_engine

# engine = create_engine('mysql://ningma:1q2w3e4r@192.168.1.100/pth?charset=utf8')
# con = engine.connect()
#
# tick_info = pd.DataFrame(con.execute(
#     'SELECT exchangeCD, secID, secShortName, ticker,'
#     '       contractObject, listDate, lastTradeDate, lastDeliDate '
#     'From pt.tick_info '
#     'INNER JOIN pt.fut_info '
#     'ON contractObject = FUT_CD'
# ).fetchall(), columns=['exc', 'tick_id', 'sht_name', 'tick', 'fut',
#                        'lst_date', 'lst_trad_date', 'lst_deli_date'])
# tick_info['lst_date'] = tick_info['lst_date'].astype('datetime64')
# tick_info['lst_trad_date'] = tick_info['lst_trad_date'].astype('datetime64')
# tick_info['lst_deli_date'] = tick_info['lst_deli_date'].astype('datetime64')
# tick_info.set_index('tick_id', inplace=True)
# tick_info.sort_index(inplace=True)
# tick_info.to_csv('data\\tick_info.csv', encoding='utf-8')
#
# quot = pd.DataFrame(con.execute(
#     'SELECT exchangeCD, secID, ticker, tradeDate, contractObject, preSettlePrice, '
#     '       openPrice, highestPrice, lowestPrice, closePrice, settlePrice, turnoverVol, '
#     '       mainCon, smainCon '
#     'FROM pt.fut_quot2006a '
#     'INNER JOIN pt.fut_info '
#     'ON contractObject = FUT_CD '
#     'WHERE mainCon + smainCon = 1'
# ).fetchall(), columns=['exc', 'tick_id', 'tick', 'trad_date', 'fut', 'ydy_sett',
#                        'open', 'high', 'low', 'close', 'sett', 'vol', 'main', 'sub_main'])
# quot['trad_date'] = quot['trad_date'].astype('datetime64')
# quot.set_index(['tick_id', 'trad_date'], inplace=True)
# quot.sort_index(inplace=True)
# quot.fillna(method='ffill', inplace=True)
# quot.to_csv('data\\quot.csv', encoding='utf-8')
#
# quot_2016jan = pd.DataFrame(con.execute(
#     'SELECT exchangeCD, secID, ticker, tradeDate, contractObject, preSettlePrice, '
#     '       openPrice, highestPrice, lowestPrice, closePrice, settlePrice, turnoverVol, '
#     '       mainCon, smainCon '
#     'FROM pt.fut_quot2016jan '
#     'INNER JOIN pt.fut_info '
#     'ON contractObject = FUT_CD '
#     'WHERE mainCon + smainCon = 1'
# ).fetchall(), columns=['exc', 'tick_id', 'tick', 'trad_date', 'fut', 'ydy_sett',
#                        'open', 'high', 'low', 'close', 'sett', 'vol', 'main', 'sub_main'])
# quot_2016jan['trad_date'] = quot_2016jan['trad_date'].astype('datetime64')
# quot_2016jan.set_index(['tick_id', 'trad_date'], inplace=True)
# quot_2016jan.sort_index(inplace=True)
# quot_2016jan.fillna(method='ffill', inplace=True)
# quot_2016jan.to_csv('data\\quot_2016jan.csv', encoding='utf-8')

fut_info = pd.read_csv(r'd:\Proj\Home\Wott\data\fut_info.csv', encoding='utf-8')
fut_info.set_index('fut', inplace=True)


tick_info = pd.read_csv('data\\tick_info.csv', encoding='utf-8')
tick_info['lst_date'] = tick_info['lst_date'].astype('datetime64')
tick_info['lst_trad_date'] = tick_info['lst_trad_date'].astype('datetime64')
tick_info['lst_deli_date'] = tick_info['lst_deli_date'].astype('datetime64')
tick_info.set_index('tick_id', inplace=True)
tick_info.sort_index(inplace=True)

quot = pd.read_csv('data\\quot.csv', encoding='utf-8')
quot['trad_date'] = quot['trad_date'].astype('datetime64')
quot.set_index(['tick_id', 'trad_date'], inplace=True)
quot.sort_index(inplace=True)

quot_2016jan = pd.read_csv('data\\quot_2016jan.csv', encoding='utf-8')
quot_2016jan['trad_date'] = quot_2016jan['trad_date'].astype('datetime64')
quot_2016jan.set_index(['tick_id', 'trad_date'], inplace=True)
quot_2016jan.sort_index(inplace=True)

# 主力指数
# quot1.sort_values(['fut','trad_date'], inplace=True)
#
# def weighted_mean(x):
#     if sum(quot1.loc[x.index, 'vol'] == 0):
#         return np.nan
#     else:
#         return np.average(x, weights=quot1.loc[x.index, 'vol'])
#
# dom_idx = quot1.groupby(['fut', 'trad_date'])['open', 'high', 'low', 'close', 'sett'].agg(weighted_mean)
# dom_idx.fillna(method='ffill', inplace=True)
# dom_idx.to_csv('data\\dom_idx.csv', encoding='utf-8')

dom_idx = pd.read_csv('data\\dom_idx.csv', encoding='utf-8')
dom_idx.set_index(['fut', 'trad_date'], inplace=True)
dom_idx.sort_index(inplace=True)
