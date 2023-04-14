class Bot:
    def __init__(self, name, btc, aud):
        self.name = name
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
    def buy(self,timestamp, bidprice,amount):
        action="buy"
        self.profit-=bidprice*amount
        self.tradingrecord.append((timestamp,action,bidprice,amount))

    def sell(self,timestamp, askprice,amount):
        action="sell"
        self.profit+=askprice*amount
        self.tradingrecord.append((timestamp,action,askprice,amount))

    def score(self):
        if(self.btc!=0):
            print("Please sold all BTC")
            return 0
        return self.profit   