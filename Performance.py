# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fig = plt.figure()
for i, row in comb.iterrows():
    quot_code = quot.ix[row.code]
    quot_code.set_index('date', inplace=True)
    ax1 = fig.add_subplot(len_comb, 1, i + 1)
    x_date = pd.Series(np.intersect1d(act.value.index.values, quot_code.index.values))
    ax1.plot(x_date, act.value.ix[x_date].net_value, 'r-', linewidth=3)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Net Value', color='red')
    ax1.set_ylim([0, act.value.ix[x_date].net_value.max() * 1.1])
    ax2 = ax1.twinx()
    ax2.plot(x_date, quot_code.ix[x_date].close * row.price_div, 'b-')
    ax2.plot(x_date, quot_code.ix[x_date].MA_short * row.price_div, 'g--')
    ax2.plot(x_date, quot_code.ix[x_date].MA_long * row.price_div, 'k--')
    ax2.set_ylabel(row.code, color='blue')
    ax2.set_ylim([0, quot_code.ix[x_date].close.max() * row.price_div * 1.1])
plt.show()


def max_dd(series):
    max2here = pd.expanding_max(series)
    dd2here = max2here - series
    return dd2here.max()

print 'Current net value %.3f' % act.value.net_value[-1]
print 'Max net value: %.3f' % act.value.net_value.max()
print 'Min net value: %.3f' % act.value.net_value.min()
print 'Max drawn down: %.3f' % max_dd(act.value.net_value)

act.value['ret'] = act.value.net_value / act.value.net_value.shift(1) - 1
sharpe = (act.value.ret.mean() - 0.06/365) / (act.value.ret.std()) * np.sqrt(365)
print 'Sharpe ratio: %.2f' % sharpe
