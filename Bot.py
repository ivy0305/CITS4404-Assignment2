from ta.volatility import BollingerBands, AverageTrueRange
import pandas as pd
class Bot:
    def __init__(self, model, btc, aud):
        self.model = model
        self.btc = btc
        self.aud = aud
        self.profit =0
        self.tradingrecord=[]
    def read_OHLCV_data(data):
        return
    def getaud(self):
        return self.aud
    def getbtc(self):
        return self.btc
    def getprofit(self):
        return self.profit
    def gettradingrecord(self):
        return self.tradingrecord
    
    def run(self,df):
        bb_indicator=BollingerBands(df["close"])
        df["upperband"]=bb_indicator.bollinger_hband()
        df["lowerband"]=bb_indicator.bollinger_lband()
        df["moving_average"]=bb_indicator.bollinger_mavg()
        atr_indicator=AverageTrueRange(df["high"],df["low"],df["close"])
        df["atr"]=atr_indicator.average_true_range()

        
        for index, row in df.iterrows():
            if(pd.isna(row["upperband"]) ):
                continue
            #print("no:",index,"close:",row["close"],"upperband:",row["upperband"],"lowerband:",row["lowerband"])
            if(row["close"]>row["upperband"]):
                print("sell:",row["timestamp"],row["close"],0.001)
                self.sell(row["timestamp"],row["close"],0.001)
            if(row["close"]<row["lowerband"]):
                print("buy:",row["timestamp"],row["close"],0.001)
                self.buy(row["timestamp"],row["close"],0.001)
        print("final AUD:",self.aud,"BTC:",self.btc)
        if(self.btc!=0):
            self.sell( df["timestamp"].iloc[-1], df["close"].iloc[-1],self.btc) 
        return
        
        
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