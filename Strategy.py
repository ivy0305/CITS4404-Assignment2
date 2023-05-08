import pandas as pd
from ta.volume import MFIIndicator
from ta.trend import EMAIndicator
from ta.momentum import StochasticOscillator

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
        if(t<14):
            return action
        if(t==14):
            action="buy"
        return action
        #done

              
class VotingStrategy(Strategy):
    def __init__(self, mfi_buy_threshold_divergence,mfi_sell_threshold_divergence,d_buy_threshold_divergence,d_sell_threshold_divergence,d_w,kd_w,ema_w,mfi_w):
        self.signal="hold"
        self.mfi_buy_threshold_divergence=mfi_buy_threshold_divergence
        self.mfi_sell_threshold_divergence=mfi_sell_threshold_divergence
        self.d_buy_threshold_divergence=d_buy_threshold_divergence
        self.d_sell_threshold_divergence=d_sell_threshold_divergence
        self.d_w=d_w
        self.kd_w=kd_w
        self.ema_w=ema_w
        self.mfi_w=mfi_w
    def decide(self, data,t):
        action={"hold":0,"buy":0,"sell":0}
       
        mfind=MFIIndicator(data['high'],data['low'],data['close'],data['volume'],window=14)
        mfi=mfind.money_flow_index()
        stochasticOscillator=StochasticOscillator(data['high'],data['low'],data['close'],window=14)
        k=stochasticOscillator.stoch()
        d=stochasticOscillator.stoch_signal()
       
        EMA_indicator=EMAIndicator(data['low'],window=14)
        ema=EMA_indicator.ema_indicator()[t]
        if(pd.isna(k[t]) or pd.isna(d[t]) or pd.isna(mfi[t]) or pd.isna(ema)):
            return action
 
        if k[t] > d[t]:
            action["buy"]+=self.kd_w
        else:
            action["sell"]+=self.kd_w 
     
        if( d[t]>30+self.d_buy_threshold_divergence and d[t-1]<30+self.d_buy_threshold_divergence):
            action["buy"]+=self.d_w
        elif(d[t]<70+self.d_sell_threshold_divergence and d[t-1]>70+self.d_sell_threshold_divergence):
            action["sell"]+=self.d_w
        else:
            action["hold"]+=self.d_w
            
        if( mfi[t-1]<20+self.mfi_buy_threshold_divergence and mfi[t]>20+self.mfi_buy_threshold_divergence):
            action["buy"]+=self.mfi_w
        elif(mfi[t-1]>80+self.mfi_sell_threshold_divergence and mfi[t]<80+self.mfi_sell_threshold_divergence):
            action["sell"]+=self.mfi_w
        else:
            action["hold"]+=self.mfi_w
        
        if(data.loc[t, 'close']<ema):
            action["sell"]+=self.ema_w
        else:
            action["buy"]+=self.ema_w
        
        if(t==len(data)-1):
            action["hold"]+=20
        
        votedAction = max(action, key=lambda k: action[k])
        return votedAction