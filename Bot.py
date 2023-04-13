class Bot:
    def __init__(self, name, bitcion, audbudget):
        self.name = name
        self.bitcion = bitcion
        self.audbudget = audbudget
        self.tradingrecord=[]
    def read_OHLCV_data(data):
        return
    def buy(self,timestamp, bidprice):
        action="buy"
        self.tradingrecord.append((timestamp,action,bidprice))
        return
    def sell(self,timestamp, askprice):
        action="sell"
        self.tradingrecord.append((timestamp,action,askprice))
        return
    
    def score(self):
        valid = True
        balance = 0
        return balance   