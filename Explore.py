# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc

quot_x = quot[(quot['fut'] == 'SR') & (quot['main'] == 1)][['open', 'high', 'low', 'close']]
quot_x.reset_index(inplace=True)
quot_x = quot_x[quot_x['trad_date'] >= pd.to_datetime('2015-07-01')]
quot_x.trad_date = mdates.date2num(quot_x.trad_date.dt.to_pydatetime())
quot_x_ohlc = zip(quot_x['trad_date'], quot_x['open'], quot_x['high'], quot_x['low'], quot_x['close'])

weekday_quot = [tuple([i]+list(quote[1:])) for i,quote in enumerate(quot_x_ohlc)]

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)

candlestick_ohlc(ax, weekday_quot, width=0.6, colorup='r', colordown='g')
ax.set_xticks(range(0,len(weekday_quot),5))
ax.set_xticklabels([mdates.num2date(quot_x_ohlc[index][0]).strftime('%b-%d')
                    for index in ax.get_xticks()])
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.show()




