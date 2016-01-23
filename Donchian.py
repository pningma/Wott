# -*- coding: utf-8 -*-
import pandas as pd
from Account import Account
from Quotation import get_quot
# from timeit import default_timer as timer

# 初始资金
INIT_CAP = 1000000

# N（ATR）的计算周期
ATR_PERD = 20

# 是否需要均线过滤器
REQUIRE_MA_FILTER = True
# 均线过滤器中短期均线天数
MA_LINES_SHORT = 25
# 均线过滤器中长期均线天数
MA_LINES_LONG = 350
# 向上突破前期n日高点进入
PREV_HIGH_PERD = 20
# 每次建仓一个N（ATR）相当于账户资金的比例
OPEN_CAP_RATIO = 0.01
# 逐步建仓次数
OPEN_POS_STEP = 4
# 每次建仓间隔的N（ATR）
OPEN_POS_RATIO = 0.5

# 是否需要止损
REQUIRE_STOP_LOSS = True
# 止损点位间隔的N(ATR)
STOP_LOSS_RATIO = 2

# 向下突破前期n日低点退出
PREV_LOW_PERD = 10

# 回测起始期
S_BT_DATE = '2014-01-01'
# 回测结束期
E_BT_DATE = '2015-05-31'

# 两个浮点数近似相等的判别
EPS = 0.00001


#记录投资组合的表
comb = pd.DataFrame({'code': ['cyb', 'hs300', 'sz50', 'zxb', 'zz500'], #代码
                     'price_div': [1000, 1000, 1000, 1000, 1000], #价格除数，股指为1000，个股为1
                     'unit': [100, 100, 100, 100, 100], #最小购买单位
                     'limit_ratio': [0.1, 0.1, 0.1, 0.1, 0.1] #涨跌停板
                     })

# comb = pd.DataFrame({'code': ['hs300'],
#                      'price_div': [1000],
#                      'unit': [100],
#                      'limit_ratio': [0.1]
#                      })
len_comb = len(comb)

quot = get_quot(comb)

df['MA_short'] = talib.MA(df.close.shift(1).values, MA_LINES_SHORT)
df['MA_long'] = talib.MA(df.close.shift(1).values, MA_LINES_LONG)
df['ATR'] = talib.ATR(df.high.shift(1).values,
                      df.low.shift(1).values,
                      df.close.shift(1).values,
                      ATR_PERD)
df['prev_high'] = pd.rolling_max(df.high.shift(1), PREV_HIGH_PERD)
df['prev_low'] = pd.rolling_min(df.low.shift(1), PREV_LOW_PERD)



act = Account(INIT_CAP, quot)

#记录每次策略的执行
rec = pd.DataFrame(columns=['code', #代码
                            's_date', #开始日期
                            'e_date', #结束日期
                            'open_cnt', #开仓次数
                            'quit_type', #退出原因（向下突破n日低点 / 向下突破止损点）
                            'prof_loss' #盈亏金额
                            ])

#记录每次策略执行的中间变量表
status = pd.DataFrame({'s_date': [None] * len_comb, #起始日期
                       'e_date': [None] * len_comb, #终止日期
                       'open_cnt': [0] * len_comb, #当前开仓次数
                       'hold': [0] * len_comb, #当前持仓量
                       'next_open_price': [None] * len_comb, #下一开仓点位
                       'stop_loss_price': [None] * len_comb #止损点位
                       }, index=[comb.code])


for i in pd.date_range(S_BT_DATE, E_BT_DATE):
    for j, row in comb.iterrows():
        quot_code = quot.ix[row.code]
        quot_code.set_index('date', inplace=True)

        if i in quot_code.index:
            quot_date = quot_code.ix[i]
            quot_date_prev = quot_code.shift(1).ix[i]

            #首次开仓
            if status.ix[row.code].open_cnt == 0 \
                    and quot_date.high > quot_date.prev_high \
                    and abs(quot_date.low - quot_date_prev.close * (1 + row.limit_ratio)) >= EPS \
                    and (not REQUIRE_MA_FILTER or quot_date.MA_short > quot_date.MA_long):
                price = max(quot_date.open, quot_date.prev_high)
                vol = int(act.cap * OPEN_CAP_RATIO / (quot_date.ATR * row.unit)) * row.unit
                act.buy(i, row.code, price, vol)
                status.set_value(row.code, 'hold', vol)
                status.set_value(row.code, 'open_cnt', 1)
                status.set_value(row.code, 'next_open_price', price + OPEN_POS_RATIO * quot_date.ATR)
                status.set_value(row.code, 'stop_loss_price', price - STOP_LOSS_RATIO * quot_date.ATR)
                status.set_value(row.code, 's_date', i)

            #中途加仓
            elif 0 < status.ix[row.code].open_cnt < OPEN_POS_STEP \
                    and quot_date.high > status.ix[row.code].next_open_price \
                    and abs(quot_date.low - quot_date_prev.close * (1 + row.limit_ratio)) >= EPS \
                    and (not REQUIRE_MA_FILTER or quot_date.MA_short > quot_date.MA_long):
                price = max(quot_date.open, status.ix[row.code].next_open_price)
                vol = int(act.cap * OPEN_CAP_RATIO / (quot_date.ATR * row.unit)) * row.unit
                act.buy(i, row.code, price, vol)

                status.set_value(row.code, 'hold', status.ix[row.code].hold + vol)
                status.set_value(row.code, 'open_cnt', status.ix[row.code].open_cnt + 1)
                status.set_value(row.code, 'next_open_price', price + OPEN_POS_RATIO * quot_date.ATR)
                status.set_value(row.code, 'stop_loss_price', price - STOP_LOSS_RATIO * quot_date.ATR)

            #突破前期低点退出
            elif status.ix[row.code].open_cnt > 0 \
                    and quot_date.low < quot_date.prev_low \
                    and abs(quot_date.high - quot_date_prev.close * (1 - row.limit_ratio)) >= EPS:
                price = min(quot_date.open, quot_date.prev_low)
                act.sell(i, row.code, price, status.ix[row.code].hold)
                status.set_value(row.code, 'e_date', i)
                prof_loss = act.prof_loss(status.ix[row.code].s_date, status.ix[row.code].e_date, row.code)
                rec = rec.append({'code': row.code,
                                  's_date': status.ix[row.code].s_date,
                                  'e_date': status.ix[row.code].e_date,
                                  'open_cnt': status.ix[row.code].open_cnt,
                                  'quit_type': 'Min(' + str(PREV_LOW_PERD) + ')',
                                  'prof_loss': prof_loss},
                                 ignore_index=True)

                status.set_value(row.code, 'hold', 0)
                status.set_value(row.code, 'open_cnt', 0)
                status.set_value(row.code, 'next_open_price', None)
                status.set_value(row.code, 'stop_loss_price', None)
                status.set_value(row.code, 's_date', None)
                status.set_value(row.code, 'e_date', None)

            #突破止损点退出
            elif REQUIRE_STOP_LOSS \
                    and status.ix[row.code].open_cnt > 0 \
                    and quot_date.low < status.ix[row.code].stop_loss_price \
                    and abs(quot_date.high - quot_date_prev.close * (1 - row.limit_ratio)) >= EPS:
                price = min(quot_date.open, status.ix[row.code].stop_loss_price)
                act.sell(i, row.code, price, status.ix[row.code].hold)
                status.set_value(row.code, 'e_date', i)
                prof_loss = act.prof_loss(status.ix[row.code].s_date, status.ix[row.code].e_date, row.code)
                rec = rec.append({'code': row.code,
                                  's_date': status.ix[row.code].s_date,
                                  'e_date': status.ix[row.code].e_date,
                                  'open_cnt': status.ix[row.code].open_cnt,
                                  'quit_type': 'SLP',
                                  'prof_loss': prof_loss},
                                 ignore_index=True)

                status.set_value(row.code, 'hold', 0)
                status.set_value(row.code, 'open_cnt', 0)
                status.set_value(row.code, 'next_open_price', None)
                status.set_value(row.code, 'stop_loss_price', None)
                status.set_value(row.code, 's_date', None)
                status.set_value(row.code, 'e_date', None)

    #每天更新净值
    act.update_value(i)
act.value.set_index('date', inplace=True)

# end_time = timer()

# print end_time - start_time

