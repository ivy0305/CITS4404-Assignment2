import ccxt
from Bot import *
import pandas as pd
import ta
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import MACD,SMAIndicator
from ta.momentum import RSIIndicator
kraken=ccxt.kraken()
kraken.load_markets()

ohlcdata=kraken.fetch_ohlcv("BTC/AUD",timeframe="15m",limit=720)

df=pd.DataFrame(ohlcdata,columns=["timestamp","open","high","low","close","volume"])
bb_indicator=BollingerBands(df["close"])
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
model="base"
startingbtc=0
startingaud=100
basebot=Bot(model, startingbtc, startingaud)

for index, row in df.iterrows(): 
    basebot.read_OHLCV_data(row) 
    
print("AUD:",basebot.getaud(),"BTC:",basebot.getbtc())
if(basebot.getbtc()!=0):
    basebot.sell( df["timestamp"].iloc[-1], df["close"].iloc[-1],basebot.getbtc()) 
print("Score:",basebot.score())
