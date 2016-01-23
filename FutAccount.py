# -*- coding: utf-8 -*-
import pandas as pd


class Account:
    def __init__(self, quot, tick_info, fut_info):
        self.avl_fund = 0           # 当前可用资金
        self.quot = quot            # 行情数据
        self.tick_info = tick_info  # 合约数据
        self.fut_info = fut_info    # 期货品种数据

        # 资金状况
        self.clear_his = pd.DataFrame(columns=[
            'date',         # 日期
            'ydy_bal',      # 上日结存
            'deps_witd',    # 出入金
            'fee',          # 手续费
            'cl_pl',        # 逐笔平仓盈亏
            'mtm_pl',       # 盯市平仓盈亏
            'bal',          # 当日权益
            'flt_pl',       # 浮动盈亏
            'used_mrg',     # 保证金占用
            'hld_pl',       # 持仓盯市盈亏
            'tot_pl',       # 总盈亏
            'tot_mtm_pl'    # 总盯市盈亏
            'avl_fund'      # 可用资金
            'rsk_rate'      # 风险度
            'mrg_call'      # 应追加保证金
        ])



        # 出入金记录
        self.trans_his = pd.DataFrame(columns=[
            'date',     # 日期
            'direc',    # 转入转出
            'amt'       # 金额
        ])

        # 成交记录
        self.trad_his = pd.DataFrame(columns=[
            'date',     # 日期
            'exc',      # 交易所
            'fut',      # 品种
            'tick',     # 合约
            'bs',       # 买卖
            'oc',       # 开平
            'price',    # 成交价
            'vol',      # 手数
            'amt',      # 成交额
            'fee',      # 手续费
            'cl_pl'     # 平仓盈亏
        ])

        # 平仓明细
        self.close_his = pd.DataFrame(columns=[
            'date',             # 日期
            'exc',              # 交易所
            'fut',              # 品种
            'tick',             # 合约
            'bs',               # 买卖
            'price',            # 成交价
            'vol',              # 手数
            'op_date',          # 开仓日期
            'op_price',         # 开仓价
            'ydy_set_price',    # 昨日结算价
            'fee',              # 手续费
            'cl_pl'             # 平仓盈亏
        ])

        # 持仓明细
        self.hold_detail_his = pd.DataFrame(columns=[
            'date',             # 日期
            'exc',              # 交易所
            'fut',              # 品种
            'tick',             # 合约
            'op_date',          # 开仓日期
            'bs',               # 买卖
            'vol',              # 持仓量
            'op_price',         # 开仓价
            'ydy_set_price',    # 昨日结算价
            'set_price',        # 结算价
            'flt_pl',           # 浮动盈亏
            'mtm_pl'            # 盯市盈亏
            'used_mrg'          # 保证金占用
        ])

        # 持仓汇总
        self.hold_detail_his = pd.DataFrame(columns=[
            'date',             # 日期
            'exc',              # 交易所
            'fut',              # 品种
            'tick',             # 合约
            'vol',              # 持仓量
            'avg_price',        # 买均价
            'ydy_set_price',    # 昨日结算价
            'set_price',        # 结算价
            'flt_pl',           # 浮动盈亏
            'mtm_pl',           # 盯市盈亏
            'used_mrg'          # 保证金占用
        ])

    def funds_trans(self, date, direc, amt):
        if amt <= 0:
            raise Exception('金额参数错误')
        if direc == 1:
            self.avl_fund += amt
        elif direc == -1:
            if self.avl_fund >= amt:
                self.avl_fund -= amt
            else:
                raise Exception('转出资金 %.2f 超过可用资金 %.2f' % (amt, self.avl_fund))
        else:
            raise Exception('资金转入/转出参数错误：1：转入，-1：转出')

        self.trans_his = self.trans_his.append({
            'date': date,
            'direc': direc,
            'amt': amt
        }, ignore_index=True)

    def open(self, date, tick, bs, price, vol):
        if bs not in ('b', 's'):
            raise Exception('开仓方向参数错误：b：买，s：卖')
        if price <= 0:
            raise Exception('开仓价格参数错误')
        if vol <= 0:
            raise Exception('开仓手数参数错误')

        tick_x = self.tick_info[(self.tick_info['tick'] == tick) &
                                 (self.tick_info['lst_date'] <= date) &
                                 (self.tick_info['lst_trad_date'] >= date)]
        if len(tick_x) == 0:
            raise Exception('查无此合约 %s' % tick)
        tick_id = tick_x.index.values[0]

        fut_x = self.fut_info.ix[tick_x['fut']]
        quot_x = self.quot.ix[['date', 'tick_id']]

        quot_x = self.quot.ix[[tick_id, date]]




    def close(self, date, tick, bs, price, vol):
        pass

    def daily_clear(self, date):
        pass

