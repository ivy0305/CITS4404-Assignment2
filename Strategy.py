import pandas as pd
import datetime
from ta.volume import VolumeWeightedAveragePrice,MFIIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import MACD,SMAIndicator,EMAIndicator
from ta.momentum import RSIIndicator,StochasticOscillator
import math
class Strategy:

    def __init__(self):
        pass
    def decide(self, data,t):
        pass
  
        #done

class BuyandholdStrategy(Strategy):
    def __init__(self):
        pass
    def decide(self, data,t):
        action="hold"
        if(t==1):
            action="buy"
        return action
        #done

              
class AIVotingStrategy(Strategy):
    def __init__(self, mfi_buy_threshold,mfi_sell_threshold,k_buy_threshold,k_sell_threshold,rsi_buy_threshold,rsi_sell_threshold,kd_w,k_w,rsi_w,mfi_w):
        self.signal="hold"
        self.mfi_buy_threshold=mfi_buy_threshold
        self.mfi_sell_threshold=mfi_sell_threshold
        self.k_buy_threshold=k_buy_threshold
        self.k_sell_threshold=k_sell_threshold
        self.rsi_buy_threshold=rsi_buy_threshold
        self.rsi_sell_threshold=rsi_sell_threshold
        self.kd_w=kd_w
        self.k_w=k_w
        self.rsi_w=rsi_w
        self.mfi_w=mfi_w
    def decide(self, data,t):
        action={"hold":0,"buy":0,"sell":0}
       
        mfind=MFIIndicator(data['high'],data['low'],data['close'],data['volume'])
        mfi=mfind.money_flow_index()[t-1]
        stochasticOscillator=StochasticOscillator(data['high'],data['low'],data['close'],window=9)
        k=stochasticOscillator.stoch()
        d=stochasticOscillator.stoch_signal()
        RSI_indicator=RSIIndicator(data["close"],window=6)
        rsi=RSI_indicator.rsi()[t-1]
        EMA_indicator=EMAIndicator(data['close'],window=5)
        ema=EMA_indicator.ema_indicator()[t-1]
        if(pd.isna(k[t-1]) or pd.isna(d[t-1]) or pd.isna(mfi) or pd.isna(rsi)):
            return action
        
        if k[t-1] > d[t-1]and k[t-2] < d[t-2] and k[t-1] <30:
            # kd crossed above signal line - buy signal
            action["buy"]+=self.kd_w
        if k[t-1] < d[t-1] and k[t-2] > d[t-2] and k[t-1] >70:
            # kd crossed below signal line - sell signal
            action["sell"]+=self.kd_w
            
        if( k[t-1]<self.k_buy_threshold ):
            action["buy"]+=self.k_w
        elif(k[t-1]>self.k_sell_threshold ):
            action["sell"]+=self.k_w
        else:
            action["hold"]+=self.k_w
        
        if( rsi<self.rsi_buy_threshold ):
            action["buy"]+=self.rsi_w
        elif(rsi>self.rsi_sell_threshold ):
            action["sell"]+=self.rsi_w
        else:
            action["hold"]+=self.rsi_w
            
        if( mfi<self.mfi_buy_threshold ):
            action["buy"]+=self.mfi_w
        elif(mfi>self.mfi_sell_threshold ):
            action["sell"]+=self.mfi_w
        else:
            action["hold"]+=self.mfi_w
        '''
        if(data.loc[t-1, 'close']<ema):
            action["buy"]+=0.5
        else:
            action["sell"]+=0.5
        '''    
        
        votedAction = max(action, key=lambda k: action[k])
        return votedAction