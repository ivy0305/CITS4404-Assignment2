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
        self.nextaction="buy"
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["previouspivot"]) ):
                return action
        if(self.nextaction=="buy"):  
           if(row["close"]<row["S2"] and row["isuptrend"]):
                action="buy"
                self.nextaction="sell"
        else:
            if(row["close"]>row["R2"] and not row["isuptrend"]):
                action="sell"
                self.nextaction="buy"
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
        self.nextaction="buy"
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["rsi"]) ):
                return action
        if( self.nextaction=="buy"):
            if(row["close"]<row["lowerband"] and row["rsi"]<=30):
                action="buy"
                self.nextaction="sell"
        if( self.nextaction=="sell"):
            if(row["high"]>row["moving_average"]):
                action="sell"
                self.nextaction="buy"   
        #print("Date:",datetime.datetime.fromtimestamp(row["timestamp"]/1000.0),row["close"] ,action)
        return action
    
class RSIStrategy(Strategy):
    def __init__(self):
        self.nextaction="buy"
        self.signal="hold"
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["macd_diff"]) ):
                return action
        if(self.nextaction=="buy"):
            if(self.signal=="buy" and row["rsi"]>30):
                self.signal="hold"
                action="buy" 
                self.nextaction="sell"
            if(row["rsi"]<30):
                self.signal="buy"
        else:
            if(self.signal=="sell" and row["rsi"]<70):
                self.nextaction="buy"
                self.signal="hold"
                action="sell"
            if(row["rsi"]>70):
                self.signal="sell"
        return action
    
class MACDStrategy(Strategy):
    #https://www.youtube.com/watch?v=rf_EQvubKlk
    def __init__(self):
        self.nextaction="buy"
        self.signal="hold"
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["macd_diff"]) ):
                return action
        if(self.nextaction=="buy"):    
            if(self.signal=="buy" and row["macd"]>row["macd_signal"] and row["macd"]<0):
                action="buy"
                self.nextaction="sell"
        else:
            if(self.signal=="sell" and row["macd"]<row["macd_signal"] and row["macd"]>0):
                action="sell"
                self.nextaction="buy"
            
        if(row["macd"]<row["macd_signal"]):
            self.signal="buy"
        else:
            self.signal="sell"
        return action