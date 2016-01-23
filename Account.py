# -*- coding: utf-8 -*-
import pandas as pd


class Account:
    max_e_date = pd.to_datetime('2199-12-31')

    def __init__(self, cap, quot):
        self.cap = cap
        self.init_cap = cap
        self.quot = quot

        self.trad = pd.DataFrame(columns=['date', 'code', 'direct', 'price', 'vol', 'amt'])
        self.hold = pd.DataFrame(columns=['s_date', 'e_date', 'code', 'vol'])
        self.value = pd.DataFrame(columns=['date', 'cap', 'mkt_value', 'total_fund', 'net_value'])

    def buy(self, date, code, price, vol):
        if self.cap < vol * price:
            print 'No enough money to buy %d units of %s at price %.3f in ' \
                  + date.strftime('%Y-%m-%d') % (vol, code, price)
            return
        if code not in self.quot.index:
            raise Exception('No quotation data of ' + code)

        quot_code = self.quot.ix[code]
        quot_code.set_index('date', inplace=True)

        if date not in quot_code.index:
            raise Exception('No quotation data of ' + code + ' on ' + date.strftime('%Y-%m-%d'))
        if (price > quot_code.ix[date].high) or (price < quot_code.ix[date].low):
            raise Exception('Invalid price of ' + code + ' on ' + date.strftime('%Y-%m-%d') +
                            ' [' + str(quot_code.ix[date].low) + ', ' + str(quot_code.ix[date].high) + ']')

        self.trad = self.trad.append({'date': date,
                                      'code': code,
                                      'direct': 'B',
                                      'price': price,
                                      'vol': vol,
                                      'amt': price * vol},
                                     ignore_index=True)

        self.cap -= price * vol
        hold_idx = self.hold[(self.hold.code == code) &
                             (self.hold.e_date == Account.max_e_date)].index
        if len(hold_idx) == 0:
            self.hold = self.hold.append({'s_date': date,
                                          'e_date': Account.max_e_date,
                                          'code': code,
                                          'vol': vol},
                                         ignore_index=True)
        else:
            self.hold.set_value(hold_idx[0], 'e_date', date)
            self.hold = self.hold.append({'s_date': date,
                                          'e_date': Account.max_e_date,
                                          'code': code,
                                          'vol': self.hold.ix[hold_idx[0]].vol + vol},
                                         ignore_index=True, )
            self.hold = self.hold[self.hold.s_date != self.hold.e_date].reset_index(drop=True)

    def sell(self, date, code, price, vol):
        if code not in self.quot.index:
            raise Exception('No quotation data of ' + code)

        quot_code = self.quot.ix[code]
        quot_code.set_index('date', inplace=True)

        if date not in quot_code.index:
            raise Exception('No quotation data of ' + code + ' on ' + date.strftime('%Y-%m-%d'))
        if (price > quot_code.ix[date].high) or (price < quot_code.ix[date].low):
            raise Exception('Invalid price of ' + code + ' on ' + date.strftime('%Y-%m-%d') +
                            ' [' + str(quot_code.ix[date].low) + ', ' + str(quot_code.ix[date].high) + ']')

        hold_idx = self.hold[(self.hold.code == code) &
                             (self.hold.e_date == Account.max_e_date)].index
        if len(hold_idx) == 0 or self.hold.ix[hold_idx[0]].vol < vol:
            raise Exception('No enough holding')

        self.trad = self.trad.append({'date': date,
                                      'code': code,
                                      'direct': 'S',
                                      'price': price,
                                      'vol': vol,
                                      'amt': price * vol},
                                     ignore_index=True)
        self.cap += price * vol
        self.hold.set_value(hold_idx[0], 'e_date', date)
        if self.hold.ix[hold_idx[0]].vol > vol:
            self.hold = self.hold.append({'s_date': date,
                                          'e_date': Account.max_e_date,
                                          'code': code,
                                          'vol': self.hold.ix[hold_idx[0]].vol - vol},
                                         ignore_index=True)
        self.hold = self.hold[self.hold.s_date != self.hold.e_date].reset_index(drop=True)

    def update_value(self, date):
        self.value = self.value[self.value.date != date].reset_index(drop=True)
        cur_hold = self.hold[(self.hold.e_date == Account.max_e_date) &
                             (self.hold.s_date <= date)][['code', 'vol']]

        mkt_value = 0
        if len(cur_hold) > 0:
            for idx, row in cur_hold.iterrows():
                if row.code not in self.quot.index:
                    raise Exception('No quotation data of ' + row.code)
                quot_code = self.quot.ix[row.code]
                quot_code.set_index('date', inplace=True)

                last_quot_date = quot_code.index[quot_code.index <= date].max()
                if last_quot_date:
                    mkt_value += row.vol * quot_code.ix[last_quot_date].close
                else:
                    raise Exception('No quotation data of ' + row.code + ' before ' +
                                    date.strftime('%Y-%m-%d'))

        self.value = self.value.append({'date': date,
                                        'cap': self.cap,
                                        'mkt_value': mkt_value,
                                        'total_fund': self.cap + mkt_value,
                                        'net_value': (self.cap + mkt_value) / float(self.init_cap)},
                                       ignore_index=True)

    def prof_loss(self, s_date, e_date, code):
        if code not in self.quot.index:
            raise Exception('No quotation data of ' + code)

        quot_code = self.quot.ix[code]
        quot_code.set_index('date', inplace=True)

        s_hold_vol = self.hold[(self.hold.s_date < s_date) &
                               (self.hold.e_date >= s_date) &
                               (self.hold.code == code)].vol
        if len(s_hold_vol) == 0:
            s_hold_value = 0
        else:
            last_quot_date = quot_code.index[quot_code.index <= s_date].max()
            if last_quot_date:
                s_hold_value = s_hold_vol * quot_code.ix[last_quot_date].close
                s_hold_value = s_hold_value.values[0]
            else:
                raise Exception('No quotation data of ' + code + ' before ' +
                                s_date.strftime('%Y-%m-%d'))

        e_hold_vol = self.hold[(self.hold.s_date <= e_date) &
                               (self.hold.e_date > e_date) &
                               (self.hold.code == code)].vol
        if len(e_hold_vol) == 0:
            e_hold_value = 0
        else:
            last_quot_date = quot_code.index[quot_code.index <= e_date].max()
            if last_quot_date:
                e_hold_value = e_hold_vol * quot_code.ix[last_quot_date].close
                e_hold_value = e_hold_value.values[0]
            else:
                raise Exception('No quotation data of ' + code + ' before ' +
                                e_date.strftime('%Y-%m-%d'))

        flt_trad = self.trad[(self.trad.date >= s_date) &
                             (self.trad.date <= e_date) &
                             (self.trad.code == code)]
        if len(flt_trad) == 0:
            tot_buy_amt = tot_sell_amt = 0
        else:
            tot_buy_amt = flt_trad[flt_trad.direct == 'B'].amt.sum()
            tot_sell_amt = flt_trad[flt_trad.direct == 'S'].amt.sum()
        return e_hold_value - s_hold_value + tot_sell_amt - tot_buy_amt