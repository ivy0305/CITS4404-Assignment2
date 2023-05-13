from Strategy import *

class Bot:
    def __init__(self, name,strategy, aud):
        self.btc = 0
        self.aud = aud
        self.profit =0
        self.tradingrecord=[]
        self.strategy=strategy
        self.startingaud=aud
        self.name =name
        self.wintrade_time=0
        
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
    def getwintime(self):
        return self.wintrade_time
        
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
        self.profit=0
        self.aud-=price*btcamount
        self.btc+=btcamount
        self.profit-=price*btcamount+commission
        self.tradingrecord.append((timestamp,action,price,btcamount,commission))

    def sell(self,timestamp, price,btcamount,commission):
        action="sell"
        self.aud+=price*btcamount
        self.btc-=btcamount
        self.profit+=price*btcamount-commission
        if(self.profit>0):
            self.wintrade_time+=1
        self.tradingrecord.append((timestamp,action,price,btcamount,commission*price,self.profit))
        
    def score(self):
        print("AUD:",self.aud,"BTC:",self.btc)
        return ((self.aud-self.startingaud)/self.startingaud*100)  
