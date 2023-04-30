from Strategy import *
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import MACD,SMAIndicator
from ta.momentum import RSIIndicator
class Bot:
    def __init__(self, name,strategy, btc, aud):
        self.btc = btc
        self.aud = aud
        self.profit =0
        self.tradingrecord=[]
        self.strategy=strategy
        self.startingaud=aud
        self.name =name
        
    def getaud(self):
        return self.aud
    def getname(self):
        return self.name
    def getbtc(self):
        return self.btc
    def getprofit(self):
        return self.profit
    def gettradingrecord(self):
        return self.tradingrecord 
    def addIndicators(df):
        bb_indicator=BollingerBands(df["close"],30,2)
        df["upperband"]=bb_indicator.bollinger_hband()
        df["lowerband"]=bb_indicator.bollinger_lband()
        df["moving_average"]=bb_indicator.bollinger_mavg()
        atr_indicator=AverageTrueRange(df["high"],df["low"],df["close"])
        df["atr"]=atr_indicator.average_true_range()
        
        RSI_indicator=RSIIndicator(df["close"],12)
        df["rsi"]=RSI_indicator.rsi()

        df['previouspivot'] = (df['high'] + df['low'] + df['close'])/3
        df['R1'] = (2*df['previouspivot']) - df['low']
        df['S1'] = (2*df['previouspivot']) - df['high']
        df['R2'] = (df['previouspivot']) + (df['high'] - df['low'])
        df['S2'] = (df['previouspivot']) - (df['high'] - df['low'])
        df['previouspivot']=df['previouspivot'].shift(1)
        df['R1']=df['R1'].shift(1)
        df['S1']=df['S1'].shift(1)
        df['R2']=df['R2'].shift(1)
        df['S2']=df['S2'].shift(1)
        df["isuptrend"]=df["open"]>df["previouspivot"]
        return df 
    def addMACDIndicator(df,slow,fast,sign):  
        macd_indicator=MACD(df["close"],window_slow=slow,window_fast=fast,window_sign=sign)
        df["macd_signal"]=macd_indicator.macd_signal()
        df["macd"]=macd_indicator.macd()
        df["macd_diff"]=macd_indicator.macd_diff()  
        return df
    def addRSIIndicator(df,window):
        RSI_indicator=RSIIndicator(df["close"],window)
        df["rsi"]=RSI_indicator.rsi()
        return df
        
    def buy_trigger(self,t, data):
        action=self.strategy.decide(data,t)
        if(action=="buy"):
            return True
        else:
            return False
       
    def sell_trigger(self,t, data):
        action=self.strategy.decide(data,t)
        if(action=="sell"):
            return True
        else:
            return False
    
    
    
    def execute_trade(self,data):
        bought = False
       
        for t in range(1, len(data)):
            if not bought and self.buy_trigger(t, data) and not self.buy_trigger(t - 1, data) and not (self.sell_trigger(t, data) and not self.sell_trigger(t - 1, data)):
                #print(f"Buy signal at t={data.loc[t, 'timestamp']}, price={data.loc[t, 'close']}")
                #commission=0
                commission=self.aud*0.02
                self.aud-=commission
                self.buy(data.loc[t, 'timestamp'],data.loc[t, 'close'],self.aud/data.loc[t, 'close'],commission)
                bought = True
            elif bought and self.sell_trigger(t, data) and not self.sell_trigger(t - 1, data) and not (self.buy_trigger(t, data) and not self.buy_trigger(t - 1, data)):
                commission=self.btc*0.02
                #commission=0
                self.btc-=commission
                #print(f"Sell signal at t={data.loc[t, 'timestamp']}, price={data.loc[t, 'close']}")
                self.sell(data.loc[t, 'timestamp'],data.loc[t, 'close'],self.btc,commission)
                bought = False
            
            # Sell at the close of the last day if the asset has been bought
            if bought and t == len(data) - 1:
                #commission=0
                commission=self.btc*0.02
                self.btc-=commission
                self.sell(data.loc[t, 'timestamp'],data.loc[t, 'close'],self.btc,commission)
                bought = False
            
            
        
   
    def buy(self,timestamp, price,btcamount,commission):
        action="buy"
        self.aud-=price*btcamount
        self.btc+=btcamount
        self.profit-=price*btcamount+commission
        self.tradingrecord.append((timestamp,action,price,btcamount,commission))

    def sell(self,timestamp, price,btcamount,commission):
        action="sell"
        self.aud+=price*btcamount
        self.btc-=btcamount
        self.profit+=price*btcamount+commission
        
        self.tradingrecord.append((timestamp,action,price,btcamount,commission*price,self.profit))

    def score(self):
        print("AUD:",self.aud,"BTC:",self.btc)
       
        return self.getaud()-self.startingaud/self.startingaud*100  