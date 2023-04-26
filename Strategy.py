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