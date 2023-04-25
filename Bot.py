
import pandas as pd
from Strategy import *
class Bot:
    def __init__(self, model, btc, aud):
        self.model = model
        self.btc = btc
        self.aud = aud
        self.profit =0
        self.tradingrecord=[]
    def read_OHLCV_data(self,row):
        strategy= Strategy()
        action=strategy.decide(row)
        
        if(action=="sell"):
            print("sell:",row["timestamp"],row["close"],0.001)
            self.sell(row["timestamp"],row["close"],0.001)
        if(action=="buy"):
            print("buy:",row["timestamp"],row["close"],0.001)
            self.buy(row["timestamp"],row["close"],0.001)
        return
    
    def getaud(self):
        return self.aud
    def getbtc(self):
        return self.btc
    def getprofit(self):
        return self.profit
    def gettradingrecord(self):
        return self.tradingrecord 
    def buy(self,timestamp, bidprice,amount):
        action="buy"
        self.aud-=bidprice*amount
        self.btc+=amount
        self.profit-=bidprice*amount
        self.tradingrecord.append((timestamp,action,bidprice,amount))

    def sell(self,timestamp, askprice,amount):
        action="sell"
        self.aud+=askprice*amount
        self.btc-=amount
        self.profit+=askprice*amount
        self.tradingrecord.append((timestamp,action,askprice,amount))

    def score(self):
        print("AUD:",self.aud,"BTC:",self.btc)
        return self.profit   