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

    macd_indicator=MACD(df["close"],26,12,9)
    df["macd_signal"]=macd_indicator.macd_signal()
    df["macd"]=macd_indicator.macd()
    df["macd_diff"]=macd_indicator.macd_diff()

    
    RSI_indicator=RSIIndicator(df["close"],13)
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

ohlcdata=kraken.fetch_ohlcv("BTC/AUD",timeframe="1w",limit=DATANUMBER)

df=pd.DataFrame(ohlcdata,columns=["timestamp","open","high","low","close","volume"])
df=addIndicators(df)
startingbtc=0
startingaud=100

print("*"*50,f'{"Buy and hold Strategy":^30}',"*"*50)
BHStrategy= BuyandholdStrategy(1)
BHBot=Bot(BHStrategy, startingbtc, startingaud)
for index, row in df.iterrows(): 
    action=BHBot.read_OHLCV_data(row) 
    BHBot.runaction(action,row['timestamp'],row['close'])
    
#print("AUD:",BHBot.getaud(),"BTC:",BHBot.getbtc())
BHBot.finalisetrade(df["timestamp"].iloc[-1], df["close"].iloc[-1])
print("Result:",round(BHBot.score(),3),"%")
print("Total Trade Made:",len(BHBot.gettradingrecord())," times")
#printrecord(BHBot)




print("*"*50,f'{"Pivot Point":^30}',"*"*50)
ppstrategy= PPStrategy(0.01)
PPBot=Bot(ppstrategy, startingbtc, startingaud)


for index, row in df.iterrows(): 
    action=PPBot.read_OHLCV_data(row) 
    PPBot.runaction(action,row['timestamp'],row['close'])
    
#print("AUD:",ppbot.getaud(),"BTC:",ppbot.getbtc())
PPBot.finalisetrade(df["timestamp"].iloc[-1], df["close"].iloc[-1])
print("Result:",round(PPBot.score(),3),"%")
print("Total Trade Made:",len(PPBot.gettradingrecord())," times")
#printrecord(ppbot)

print("*"*50,f'{"BollingerBand RSI Strategy":^30}',"*"*50)
BRSIstrategy= BollingerBandRSIStrategy(0.1)
BRSIBot=Bot(BRSIstrategy, startingbtc, startingaud)
for index, row in df.iterrows(): 
    action=BRSIBot.read_OHLCV_data(row) 
    BRSIBot.runaction(action,row['timestamp'],row['close'])
    
#print("AUD:",BHBot.getaud(),"BTC:",BHBot.getbtc())
BRSIBot.finalisetrade(df["timestamp"].iloc[-1], df["close"].iloc[-1])
print("Result:",round(BRSIBot.score(),3),"%")
print("Total Trade Made:",len(BRSIBot.gettradingrecord())," times")
#printrecord(BHBot)

print("*"*50,f'{"RSI Strategy":^30}',"*"*50)
RSIstrategy= RSIStrategy(0.1)
RSIBot=Bot(RSIstrategy, startingbtc, startingaud)
for index, row in df.iterrows(): 
    action=RSIBot.read_OHLCV_data(row) 
    RSIBot.runaction(action,row['timestamp'],row['close'])
    
#print("AUD:",BHBot.getaud(),"BTC:",BHBot.getbtc())
RSIBot.finalisetrade(df["timestamp"].iloc[-1], df["close"].iloc[-1])
print("Result:",round(RSIBot.score(),3),"%")
print("Total Trade Made:",len(RSIBot.gettradingrecord())," times")
#printrecord(BHBot)

print("*"*50,f'{"MACD Strategy":^30}',"*"*50)
MACDstrategy= MACDStrategy(0.1)
MACDBot=Bot(MACDstrategy, startingbtc, startingaud)
for index, row in df.iterrows(): 
    action=MACDBot.read_OHLCV_data(row) 
    MACDBot.runaction(action,row['timestamp'],row['close'])
    
#print("AUD:",BHBot.getaud(),"BTC:",BHBot.getbtc())
MACDBot.finalisetrade(df["timestamp"].iloc[-1], df["close"].iloc[-1])
print("Result:",round(MACDBot.score(),3),"%")
print("Total Trade Made:",len(MACDBot.gettradingrecord())," times")