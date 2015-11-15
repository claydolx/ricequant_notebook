# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import talib
import numpy as np
import math
import pandas as pd

def choose(stocks):
    pe = get_fundamentals(query(fundamentals.eod_derivative_indicator.pe_ratio).filter(fundamentals.eod_derivative_indicator.stockcode.in_(stocks)))
    pb = get_fundamentals(query(fundamentals.eod_derivative_indicator.pb_ratio).filter(fundamentals.eod_derivative_indicator.stockcode.in_(stocks)))
    ps = get_fundamentals(query(fundamentals.eod_derivative_indicator.ps_ratio).filter(fundamentals.eod_derivative_indicator.stockcode.in_(stocks)))
    scores = pe.rank(axis=1).ix[0]+pb.rank(axis=1).ix[0]+ps.rank(axis=1).ix[0]
    #print(scores)
    #print(type(scores))
    #scores = pd.Series(scores)
    best_stocks=[]
    n=3
    for i in range(n):
        x = scores.argmin()
        #print(x)
        best_stocks.append(x)
        scores.pop(x)
    #ss = s.idxmax(axis=1).ix[0,0]
    return best_stocks #一个列表

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    #context.s = choose(['600571.XSHG', '600570.XSHG', '002657.XSHE', '600588.XSHG', '300348.XSHE', '300380.XSHE'])
    context.s = choose(['601328.XSHG', '600050.XSHG', '600583.XSHG', '601601.XSHG', '601857.XSHG', '600893.XSHG', '600036.XSHG', '600000.XSHG', '600111.XSHG', '600018.XSHG', '600519.XSHG', '601390.XSHG', '600016.XSHG', '601288.XSHG', '601668.XSHG', '601818.XSHG', '601006.XSHG', '601088.XSHG', '600585.XSHG', '600089.XSHG', '600256.XSHG', '600406.XSHG', '601998.XSHG', '601166.XSHG', '600048.XSHG', '600104.XSHG', '601800.XSHG', '601688.XSHG', '600015.XSHG', '600690.XSHG', '600028.XSHG', '600010.XSHG', '600637.XSHG', '600999.XSHG', '600109.XSHG', '601989.XSHG', '600518.XSHG', '601628.XSHG', '600887.XSHG', '600837.XSHG', '601766.XSHG', '601169.XSHG', '601988.XSHG', '601398.XSHG', '600030.XSHG', '600150.XSHG', '601186.XSHG', '601318.XSHG'])
    #scheduler.run_monthly(choose, monthday=1)
    #context.s1 = "000001.XSHE"
    context.fired = False

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单
    #print(context.s)
    # TODO: 开始编写你的算法吧！
    if not context.fired:
        #
	    # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
	    p = 1/len(context.s)
	    for q in context.s:
	        order_percent(q, p)
    context.fired = True

