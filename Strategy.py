import pandas as pd
import datetime
class Strategy:

    def __init__(self):
        pass
    def decide(self, row):
        pass
  
        #done
class PPStrategy(Strategy):
    def __init__(self):
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["previouspivot"]) ):
                return action

        if(row["close"]<row["S2"] and row["isuptrend"]):
            action="buy"
                
        if(row["close"]>row["R2"] and not row["isuptrend"]):
            action="sell"      
        return action
        #done
class BuyandholdStrategy(Strategy):
    def __init__(self):
        self.i=0
    def decide(self, row):
        action="hold"
        if(self.i==0):
            action="buy"
        self.i+=1

        return action
        #done
        
class BollingerBandRSIStrategy(Strategy):
    #https://www.youtube.com/watch?v=pCmJ8wsAS_w
    def __init__(self):
        pass
    def decide(self, row):
        action="hold"
        #skip if no rsi data
        if(pd.isna(row["rsi"]) ):
                return action
    
        if(row["close"]<row["lowerband"] and row["rsi"]<=30):
            action="buy"
    
        if(row["high"]>row["moving_average"]):
            action="sell"
       
        #print("Date:",datetime.datetime.fromtimestamp(row["timestamp"]/1000.0),row["close"] ,action)
        return action
    
class RSIStrategy(Strategy):
    def __init__(self):
  
        self.signal="hold"
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["macd_diff"]) ):
                return action
     
        if(self.signal=="buy" and row["rsi"]>30):
            self.signal="hold"
            action="buy"  
        if(self.signal=="sell" and row["rsi"]<70):
            self.signal="hold"
            action="sell"
        if(row["rsi"]>70):
            self.signal="sell"
        if(row["rsi"]<30):
            self.signal="buy"
        return action
    
class MACDStrategy(Strategy):
    #https://www.youtube.com/watch?v=rf_EQvubKlk
    def __init__(self):
        self.signal="hold"
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["macd_diff"]) ):
                return action
        if(self.signal=="buy" and row["macd"]>row["macd_signal"] and row["macd"]< 0):
            action="buy"
            self.signal="hold"
    
        if(self.signal=="sell" and row["macd"]<row["macd_signal"] and row["macd"]>0 ):
            action="sell"
            self.signal="hold"
            
        if(row["macd"]<row["macd_signal"]):
            self.signal="buy"
        else:
            self.signal="sell"
        return action
class MACDRSIStrategy(Strategy):
    #https://www.youtube.com/watch?v=rf_EQvubKlk
    def __init__(self):
        self.signal="hold"
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["macd_diff"]) ):
                return action
        if(self.signal=="buy" and row["macd"]>row["macd_signal"] and row["macd"]< 0 and row["rsi"]<50):
            action="buy"
            self.signal="hold"
    
        if(self.signal=="sell" and row["macd"]<row["macd_signal"] and row["macd"]>0  and row["rsi"]>50):
            action="sell"
            self.signal="hold"
            
        if(row["macd"]<row["macd_signal"]):
            self.signal="buy"
        else:
            self.signal="sell"
        return action
class VotingStrategy(Strategy):
    def __init__(self,strategyList):
        self.StrategyList=strategyList
    def decide(self, row):
        decisionlist=[]
        for strategy in self.StrategyList:
           decisionlist.append(strategy.decide(row))
        #print(decisionlist)
        return max(set(decisionlist), key = decisionlist.count)