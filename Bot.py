from Strategy import *
class Bot:
    def __init__(self, strategy, btc, aud):
        self.btc = btc
        self.aud = aud
        self.profit =0
        self.tradingrecord=[]
        self.strategy=strategy
        self.startingaud=aud
    def read_OHLCV_data(self,row):
        action=self.strategy.decide(row)
        return action
    def runaction(self,action,timestamp,close):
        if(action=="sell"):
            tradingamount=self.strategy.gettradingvolumepercentage()*self.startingaud/close
            self.sell(timestamp,close,tradingamount)
        if(action=="buy"):
            tradingamount=self.strategy.gettradingvolumepercentage()*self.startingaud/close
            self.buy(timestamp,close,tradingamount)
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

    def finalisetrade(self,timestamp,close):
        if(self.getbtc()!=0):
            self.sell( timestamp, close,self.getbtc()) 
        if(self.getbtc()<0):
            self.buy( timestamp, close,abs(self.getbtc())) 
    def score(self):
        print("AUD:",self.aud,"BTC:",self.btc)
        return self.profit/self.startingaud*100  