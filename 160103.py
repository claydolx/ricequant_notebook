#简单的卡尔曼滤波和pair trading

import talib
import numpy as np
import math
import pandas as pd

def init(context):
    #中信证券 x
    #天房发展 y
    context.s1 = "600030.XSHG"
    context.s2 = "600322.XSHG"
    context.Q = 2.5143591211526362 #需要确定
    context.R = 0.44338752801584308 #同上y的标准差
    context.KfBeta = 0.29027465784393242 #同上
    context.P = 0
    context.mean = -0.25681462928009235 #同上 s2[-1]-s1[-1] * s2.mean()/s1.mean()

def handle_bar(context, bar_dict):
    x = history(1,'1m','close')[context.s1][0]
    y = history(1,'1m','close')[context.s2][0]
    #x = history(1,'1d','close')[context.s1][0]
    #y = history(1,'1d','close')[context.s2][0]
    
    #滤波部分，获得beta
    if x != 'NaN' and y != 'NaN' :
        yHat = x * context.KfBeta
        v = y - yHat
        F = context.P * (x**2) + context.R
        context.KfBeta = context.KfBeta + context.P * x * v / F
        context.P = context.P - (context.P * x)**2 / F + context.Q
    #以上通过测试 12/23

    betShare = context.portfolio.cash*0.6/y
    buyShare = context.KfBeta*betShare
    #价差、zScore、仓位
    spread = y - x * context.KfBeta
    zScore = (spread-context.mean) / context.R
    shareStock1 = context.portfolio.positions[context.s1]
    shareStock2 = context.portfolio.positions[context.s2]
    
    
    
    #底下信号好好琢磨怎么写
    #print('start')
    #print(betShare)
    #print(buyShare)
    print(zScore)
    #入场信号
    if zScore > 0.5:
        order_shares(context.s2, -betShare)
        order_shares(context.s1, buyShare)

    if zScore <-0.5:
        order_shares(context.s1, -buyShare)
        order_shares(context.s2, betShare)

    #离场信号
    if zScore < 0.5 and zScore >-0.5: #and (shareStock1 !=0 or shareStock2 !=0):
        order_target_value(context.s1, 0)
        order_target_value(context.s2, 0)


