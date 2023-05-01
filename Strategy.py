import pandas as pd
import datetime
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import MACD,SMAIndicator
from ta.momentum import RSIIndicator
import math
class Strategy:

    def __init__(self):
        pass
    def decide(self, data,t):
        pass
  
        #done
'''  
class PPStrategy(Strategy):
    def __init__(self):
        pass
    def decide(self, data,t):
        
        action="hold"
        if(pd.isna(data["previouspivot"]) ):
                return action

        if(data["close"]<data["S2"] and data["isuptrend"]):
            action="buy"
                
        if(data["close"]>data["R2"] and not data["isuptrend"]):
            action="sell"      
        return action
        #done
'''  
class BuyandholdStrategy(Strategy):
    def __init__(self):
        pass
    def decide(self, data,t):
        action="hold"
        if(t==1):
            action="buy"
        return action
        #done

     
class BollingerBandRSIStrategy(Strategy):
    #https://www.youtube.com/watch?v=pCmJ8wsAS_w
    def __init__(self,rsiwindow,window, window_dev_square,buyrsithreshold,sellrsithreshold):
        self.rsiwindow=rsiwindow
        self.BBwindow=window
        self.window_dev=math.sqrt( window_dev_square)
        self.buyrsithreshold=buyrsithreshold
        self.sellrsithreshold=sellrsithreshold
        self.minimumworkingday=max(rsiwindow,window)
        
        pass
    def decide(self, data,t):
        action="hold"
        if(t<self.minimumworkingday):
            return action
        closevalue=data["close"][t-1]
        bb_indicator=BollingerBands(data["close"],self.BBwindow,self.window_dev)
        upperband=bb_indicator.bollinger_hband()[t-1]
        lowerband=bb_indicator.bollinger_lband()[t-1]
        
        RSI_indicator=RSIIndicator(data["close"],window=self.rsiwindow)
        rsi=RSI_indicator.rsi()[t-1]
       
        #skip if no rsi data
    
        if(closevalue<lowerband and rsi<self.buyrsithreshold):
            action="buy"
    
        if(closevalue>upperband and rsi<self.sellrsithreshold):
            action="sell"
       
        #print("Date:",datetime.datetime.fromtimestamp(row["timestamp"]/1000.0),row["close"] ,action)
        return action

class RSIStrategy(Strategy):
    def __init__(self,rsiwindow,buyrsithreshold,sellrsithreshold):
        self.rsiwindow=rsiwindow
        self.buyrsithreshold=buyrsithreshold
        self.sellrsithreshold=sellrsithreshold
        self.minimumworkingday=rsiwindow
        self.signal="hold"
        pass
    def decide(self, data,t):
        action="hold"
        if(t<self.minimumworkingday):
            return action
        RSI_indicator=RSIIndicator(data["close"],window=self.rsiwindow)
        rsi=RSI_indicator.rsi()[t-1]    
        
        if(self.signal=="buy" and rsi>self.buyrsithreshold):
            self.signal="hold"
            action="buy"  
        if(self.signal=="sell" and rsi<self.sellrsithreshold):
            self.signal="hold"
            action="sell"
        if(rsi>70):
            self.signal="sell"
        if(rsi<30):
            self.signal="buy"
        return action
    '''      
class MACDStrategy(Strategy):
    #https://www.youtube.com/watch?v=rf_EQvubKlk
    def __init__(self):
        self.signal="hold"
        pass
    def decide(self, data,t):
        action="hold"
        if(pd.isna(data["macd_diff"]) ):
                return action
        if(self.signal=="buy" and data["macd"]>data["macd_signal"] and data["macd"]< 0):
            action="buy"
            self.signal="hold"
    
        if(self.signal=="sell" and data["macd"]<row["macd_signal"] and row["macd"]>0 ):
            action="sell"
            self.signal="hold"
            
        if(row["macd"]<row["macd_signal"]):
            self.signal="buy"
        else:
            self.signal="sell"
        return action
         '''  
class MACDRSIStrategy(Strategy):
    #https://www.youtube.com/watch?v=rf_EQvubKlk
    def __init__(self,slow,fast,sign,rsiwindow,buyrsithreshold,sellrsithreshold,macdthreshold):
        self.signal="hold"
        self.slow=slow
        self.fast=fast
        self.sign=sign
        self.rsiwindow=rsiwindow
        self.buyrsithreshold=buyrsithreshold
        self.sellrsithreshold=sellrsithreshold
        self.minimumworkingday=slow+sign-2 
        self.macdthreshold=macdthreshold
        pass
    def decide(self, data,t):
        action="hold"
        if(t<=self.minimumworkingday):
            return action
        macd_indicator=MACD(data["close"],window_slow=self.slow,window_fast=self.fast,window_sign=self.sign)
        macd_signal=macd_indicator.macd_signal()[t-1]
        macd=macd_indicator.macd()[t-1]
        #macd_diff=macd_indicator.macd_diff()[-1]
  
        RSI_indicator=RSIIndicator(data["close"],window=self.rsiwindow)
        rsi=RSI_indicator.rsi()[t-1]
        if(macd>macd_signal and macd< self.macdthreshold and rsi<self.buyrsithreshold):
            action="buy"
        if( macd<macd_signal and macd>self.macdthreshold and rsi>self.sellrsithreshold):
            action="sell"
          
        '''
         if(self.signal=="buy" and macd>macd_signal and macd< self.macdthreshold and rsi<self.buythreshold):
            action="buy"
            self.signal="hold"
    
        if(self.signal=="sell" and macd<macd_signal and macd>self.macdthreshold and rsi>self.sellthreshold):
            action="sell"
            self.signal="hold"
           
        if(macd<macd_signal):
            self.signal="buy"
        else:
            self.signal="sell"
        ''' 
        return action

class MACDStrategy(Strategy):
    #https://www.youtube.com/watch?v=rf_EQvubKlk
    def __init__(self,slow,fast,sign,macdthreshold):
        self.signal="hold"
        self.slow=slow
        self.fast=fast
        self.sign=sign
        self.minimumworkingday=slow+sign-2 
        self.macdthreshold=macdthreshold
        pass
    def decide(self, data,t):
        action="hold"
        if(t<=self.minimumworkingday):
            return action
        macd_indicator=MACD(data["close"],window_slow=self.slow,window_fast=self.fast,window_sign=self.sign)
        macd_signal=macd_indicator.macd_signal()[t-1]
        macd=macd_indicator.macd()[t-1]
        #macd_diff=macd_indicator.macd_diff()[-1]
    
        if(self.signal=="buy" and macd>macd_signal and macd< self.macdthreshold ):
            action="buy"
       
    
        if(self.signal=="sell" and macd<macd_signal and macd> self.macdthreshold ):
            action="sell"
           
           
        if(macd<macd_signal and self.signal!="buy"):
            self.signal="buy"
        if(macd>macd_signal and self.signal!="sell"):
            self.signal="sell"
        
 
        
           
       

'''
class VotingStrategy(Strategy):
    def __init__(self,strategyList):
        self.StrategyList=strategyList
    def decide(self, data,t):
        decisionlist=[]
        for strategy in self.StrategyList:
           decisionlist.append(strategy.decide(data))
        #print(decisionlist)
        return max(set(decisionlist), key = decisionlist.count)
'''  