import ccxt
from Bot import *
from Strategy import *
import pandas as pd
import datetime
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import MACD,SMAIndicator
from ta.momentum import RSIIndicator
def printrecord(bot):
    print("Trade Record: ")
    for i in bot.gettradingrecord():
        if(i[1]=="sell"):
            print("Date:",datetime.datetime.fromtimestamp(i[0]/1000.0),"\tAction:",i[1],"\tPrice:",i[2],"\tAmount(BTC):",i[3],"\tCommission(AUD):",i[4],"\tNet Profit(AUD):",i[5])
        else:
            print("Date:",datetime.datetime.fromtimestamp(i[0]/1000.0),"\tAction:",i[1],"\tPrice:",i[2],"\tAmount(BTC):",i[3],"\tCommission(AUD):",i[4])
        
def addIndicators(df):
    bb_indicator=BollingerBands(df["close"],30,2)
    df["upperband"]=bb_indicator.bollinger_hband()
    df["lowerband"]=bb_indicator.bollinger_lband()
    df["moving_average"]=bb_indicator.bollinger_mavg()
    atr_indicator=AverageTrueRange(df["high"],df["low"],df["close"])
    df["atr"]=atr_indicator.average_true_range()

    macd_indicator=MACD(df["close"],26,12,9)
    df["macd_signal"]=macd_indicator.macd_signal()
    df["macd"]=macd_indicator.macd()
    df["macd_diff"]=macd_indicator.macd_diff()

    
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
# Retrieve the historical data
DATANUMBER=720
kraken=ccxt.kraken()
kraken.load_markets()

ohlcdata=kraken.fetch_ohlcv("BTC/AUD",since=1620403200000,timeframe="4h",limit=DATANUMBER) #Since 1620403200000 8 May 2021 (+ 720days = 28 Apr 2023)

df=pd.DataFrame(ohlcdata,columns=["timestamp","open","high","low","close","volume"])

df=addIndicators(df)
print(df)
# *** Simulations *** #


# Simulates a defined number of days of trade simulations with given parameters and starting cash.
startingbtc=0
startingaud=100

BHStrategy= BuyandholdStrategy()
PPstrategy= PPStrategy()
BRSIstrategy= BollingerBandRSIStrategy()
RSIstrategy= RSIStrategy()
MACDstrategy= MACDStrategy()
MACDRSIstrategy=MACDRSIStrategy()
Votestrategy= VotingStrategy([MACDstrategy,RSIstrategy,PPstrategy])
BHBot=Bot("Buy and hold Strategy",BHStrategy, startingbtc, startingaud)
PPBot=Bot("PP Support and Resistance Strategy",PPstrategy, startingbtc, startingaud)
BRSIBot=Bot("BollingerBand RSI Strategy",BRSIstrategy, startingbtc, startingaud)
RSIBot=Bot("RSI Strategy",RSIstrategy, startingbtc, startingaud)
VoteBot=Bot("Voting Strategy",Votestrategy, startingbtc, startingaud)
MACDBot=Bot("MACD Strategy",MACDstrategy, startingbtc, startingaud)
MACDRSIstrategy=Bot("MACD RSI Strategy",MACDRSIstrategy, startingbtc, startingaud)
TestBots=[BHBot,PPBot,RSIBot,BRSIBot,MACDBot,MACDRSIstrategy,VoteBot]
for bot in TestBots:
    print("*"*50,f'{bot.getname():^30}',"*"*50)
    bot.execute_trade(df) 
  
    print("Result:",round(bot.score(),3),"%")
    print("Total Trade Made:",len(bot.gettradingrecord())," times")
    #printrecord(bot)
