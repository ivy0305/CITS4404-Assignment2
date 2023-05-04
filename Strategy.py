import pandas as pd
import datetime
from ta.volume import VolumeWeightedAveragePrice,MFIIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import MACD,SMAIndicator
from ta.momentum import RSIIndicator,StochasticOscillator
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
         
class AIMACDRSIStrategy(Strategy):
    #https://www.youtube.com/watch?v=rf_EQvubKlk
    def __init__(self,macd_buy_threshold,macd_sell_threshold,macdsignal_buy_threshold,macdsignal_sell_threshold,macd_diff_threshold,buyrsithreshold,sellrsithreshold):
        self.signal="hold"
        self.macd_buy_threshold=macd_buy_threshold
        self.macd_sell_threshold=macd_sell_threshold
        self.macdsignal_buy_threshold=macdsignal_buy_threshold
        self.macdsignal_sell_threshold=macdsignal_sell_threshold
        self.macd_diff_threshold=macd_diff_threshold
        self.buyrsithreshold=buyrsithreshold
        self.sellrsithreshold=sellrsithreshold
        pass
    def decide(self, data,t):
        action="hold"
        macd_indicator=MACD(data["close"])
        macd_signal=macd_indicator.macd_signal()[t-1]   
        macd=macd_indicator.macd()[t-1]   
        macd_diff=macd_indicator.macd_diff()[t-1]   
        RSI_indicator=RSIIndicator(data["close"])
        rsi=RSI_indicator.rsi()[t-1]
        if(pd.isna(macd_signal) or pd.isna(macd) or pd.isna(macd_diff) or pd.isna(rsi)):
            return action
     
        if( macd < self.macd_buy_threshold  and macd_signal< self.macdsignal_buy_threshold and macd_diff> self.macd_diff_threshold and rsi<self.buyrsithreshold):
            action="buy"
        if( macd > self.macd_sell_threshold  and macd_signal> self.macdsignal_sell_threshold and macd_diff< self.macd_diff_threshold and rsi>self.sellrsithreshold):
            action="sell" 
        return action
       
        '''
        if( macd[t-1] > macd_signal[t-1]and macd[t-2] < macd_signal[t-2]  and macd[t-1]< self.macdthreshold and rsi<self.buyrsithreshold):
            action="buy"
        if( macd[t-1] < macd_signal[t-1] and macd[t-2] > macd_signal[t-2] and macd[t-1]>self.macdthreshold and rsi>self.sellrsithreshold):
            action="sell"
        '''
class AIStrategy(Strategy):
    def __init__(self, k_threshold,d_threshold,rsi_buy_threshold,rsi_sell_threshold):
        self.signal="hold"
        self.k_threshold=k_threshold
        self.d_threshold=d_threshold
        self.rsi_buy_threshold=rsi_buy_threshold
        self.rsi_sell_threshold=rsi_sell_threshold
        pass
    def decide(self, data,t):
        action="hold"
        mfind=MFIIndicator(data['high'],data['low'],data['close'],data['volume'])
        mfi=mfind.money_flow_index()[t-1]
        stochasticOscillator=StochasticOscillator(data['high'],data['low'],data['close'])
        k=stochasticOscillator.stoch()[t-1]
        d=stochasticOscillator.stoch()[t-1]
        RSI_indicator=RSIIndicator(data["close"])
        rsi=RSI_indicator.rsi()[t-1]
        if(pd.isna(k) or pd.isna(d) or pd.isna(mfi) or pd.isna(rsi)):
            return action
        
        if( k > self.k_threshold  and d> self.d_threshold and mfi< 20 and rsi<self.rsi_buy_threshold):
            action="buy"
        if( k < self.k_threshold  and d<self.d_threshold and mfi> 80 and rsi>self.rsi_sell_threshold):
            action="sell" 
        return action
              
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
            
        votedAction = max(action, key=lambda k: action[k])
        return votedAction       
             
class MACDRSIStrategy(Strategy):
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
        macd_signal=macd_indicator.macd_signal()
        macd=macd_indicator.macd()
        #macd_diff=macd_indicator.macd_diff()[-1]
  
        RSI_indicator=RSIIndicator(data["close"],window=self.rsiwindow)
        rsi=RSI_indicator.rsi()[t-1]
        '''
        if( macd[t-1] > macd_signal[t-1]and macd[t-2] < macd_signal[t-2]  and macd[t-1]< self.macdthreshold and rsi<self.buyrsithreshold):
            action="buy"
        if( macd[t-1] < macd_signal[t-1] and macd[t-2] > macd_signal[t-2] and macd[t-1]>self.macdthreshold and rsi>self.sellrsithreshold):
            action="sell"
        '''
        
        if( macd[t-1] > macd_signal[t-1]  and macd[t-1]< self.macdthreshold and rsi<self.buyrsithreshold):
            action="buy"
        if( macd[t-1] < macd_signal[t-1] and macd[t-1]>self.macdthreshold and rsi>self.sellrsithreshold):
            action="sell" 
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
        macd_signal=macd_indicator.macd_signal()
        macd=macd_indicator.macd()
        #macd_diff=macd_indicator.macd_diff()[-1]
    
        if macd[t-1] > macd_signal[t-1]and macd[t-2] < macd_signal[t-2] and macd[t-1] <self.macdthreshold:
            # MACD crossed above signal line - buy signal
            action='buy'
        if macd[t-1] < macd_signal[t-1] and macd[t-2] > macd_signal[t-2] and macd[t-1] >self.macdthreshold:
            # MACD crossed below signal line - sell signal
            action='sell'
        return action
 
        
           
       

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