import ccxt
from Bot import *
from Strategy import *
import pandas as pd
import ta
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import MACD,SMAIndicator
from ta.momentum import RSIIndicator
def printrecord(bot):
    print("Trade Record: ")
    for i in bot.gettradingrecord():
        print(i)
        
def addIndicators(df):
    bb_indicator=BollingerBands(df["close"],30)
    df["upperband"]=bb_indicator.bollinger_hband()
    df["lowerband"]=bb_indicator.bollinger_lband()
    df["moving_average"]=bb_indicator.bollinger_mavg()
    atr_indicator=AverageTrueRange(df["high"],df["low"],df["close"])
    df["atr"]=atr_indicator.average_true_range()

    macd_indicator=MACD(df["close"])
    df["macd_diff"]=macd_indicator.macd_diff()

    RSI_indicator=RSIIndicator(df["close"])
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

DATANUMBER=720
kraken=ccxt.kraken()
kraken.load_markets()

ohlcdata=kraken.fetch_ohlcv("BTC/AUD",timeframe="1d",limit=DATANUMBER)

df=pd.DataFrame(ohlcdata,columns=["timestamp","open","high","low","close","volume"])
df=addIndicators(df)

print("*"*50,"Pivot Point","*"*50)
startingbtc=0
startingaud=100
ppstrategy= PPStrategy(0.01)
ppbot=Bot(ppstrategy, startingbtc, startingaud)


for index, row in df.iterrows(): 
    action=ppbot.read_OHLCV_data(row) 
    ppbot.runaction(action,row['timestamp'],row['close'])
    
#print("AUD:",ppbot.getaud(),"BTC:",ppbot.getbtc())
ppbot.finalisetrade(df["timestamp"].iloc[-1], df["close"].iloc[-1])
print("Result:",round(ppbot.score(),3),"%")
#printrecord(ppbot)

print("*"*50,"BuyandholdStrategy","*"*50)
BHStrategy= BuyandholdStrategy(1)
BHBot=Bot(BHStrategy, startingbtc, startingaud)
for index, row in df.iterrows(): 
    action=BHBot.read_OHLCV_data(row) 
    BHBot.runaction(action,row['timestamp'],row['close'])
    
#print("AUD:",BHBot.getaud(),"BTC:",BHBot.getbtc())
BHBot.finalisetrade(df["timestamp"].iloc[-1], df["close"].iloc[-1])
print("Result:",round(BHBot.score(),3),"%")
#printrecord(BHBot)

