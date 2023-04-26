import numpy as np
import random
import pandas as pd
class Strategy:

    def __init__(self,tradingpercentage):
        self.tradingpercentage=tradingpercentage

    def decide(self, row):
        pass
    def gettradingvolumepercentage(self):
        return self.tradingpercentage
        #done
class PPStrategy(Strategy):
    def __init__(self,tradingpercentage):
        self.tradingpercentage=tradingpercentage
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["previouspivot"]) ):
                return action
        if(row["close"]<row["S1"] and row["isuptrend"]):
            action="sell"
        if(row["close"]>row["R1"] and not row["isuptrend"]):
            action="buy"
        return action
        #done
class BuyandholdStrategy(Strategy):
    def __init__(self,tradingpercentage):
        self.tradingpercentage=tradingpercentage
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
    def __init__(self,tradingpercentage):
        self.tradingpercentage=tradingpercentage
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["rsi"]) ):
                return action
        if(row["low"]<row["lowerband"] and row["rsi"]<30):
            action="buy"
        if(row["high"]>row["upperband"] and row["rsi"]>70):
            action="sell"
        return action
    
class RSIStrategy(Strategy):
    def __init__(self,tradingpercentage):
        self.tradingpercentage=tradingpercentage
        pass
    def decide(self, row):
        action="hold"
        if(pd.isna(row["macd_diff"]) ):
                return action
        if(row["rsi"]<30):
            action="buy"
        if(row["rsi"]>70):
            action="sell"
        return action
    
class MACDStrategy(Strategy):
    def __init__(self,tradingpercentage):
        self.tradingpercentage=tradingpercentage
        pass
    def decide(self, row):
        action="hold"
        signal=""
        if(pd.isna(row["macd_diff"]) ):
                return action
        if(row["macd"]>row["macd_signal"]):
            if(signal!="buy" and row["macd"]<0):
                action="buy"
            signal="buy"
        if(row["macd"]<row["macd_signal"]):
            if(signal!="sell"and row["macd"]>0):
                action="sell"
            signal="sell"
            
            
        return action