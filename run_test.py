import ccxt
from Problem import *
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
        

# Retrieve the historical data
DATANUMBER=720
kraken=ccxt.kraken()
kraken.load_markets()

ohlcdata=kraken.fetch_ohlcv("BTC/AUD",since=1620403200000,timeframe="1d",limit=DATANUMBER) #Since 1620403200000 8 May 2021 (+ 720days = 28 Apr 2023)

df=pd.DataFrame(ohlcdata,columns=["timestamp","open","high","low","close","volume"])

startingbtc=0
startingaud=100
#df=addIndicators(df)
#print(df)
# *** Simulations *** #
def testBollingerBandRSIProblem():
    Problem=BollingerBandRSIProblem(df)
    algorithm = PSO(adaptive=True, pop_size=100, sampling=IntegerRandomSampling(), repair=RoundingRepair(), pertube_best=False)
    res = minimize(Problem,
                algorithm,
                seed=1,
                verbose=True)
    print("Best solution found: \nX = %s\nF = $%s\nCV = %s\nG=%s\n" % (res.X, -1 * res.F[0], res.CV[0],res.G[0]))

    BBRSIstrategy=BollingerBandRSIStrategy(rsiwindow=res.X[0],window=res.X[1],window_dev_square=res.X[2],buyrsithreshold=res.X[3],sellrsithreshold=res.X[4])
    BBRSIBot=Bot("PSO MACD RSI Strategy",BBRSIstrategy, startingbtc, startingaud)
    executebot(BBRSIBot)
    
def testMACDRSIProblem():
    Problem=MACDRSIProblem(df)
    algorithm = PSO(adaptive=True, pop_size=100, sampling=IntegerRandomSampling(), repair=RoundingRepair(), pertube_best=False)
    res = minimize(Problem,
                algorithm,
                seed=1,
                verbose=True)
    print("Best solution found: \nX = %s\nF = $%s\nCV = %s\nG=%s\n" % (res.X, -1 * res.F[0], res.CV[0],res.G[0]))
    MACDRSIstrategy=MACDRSIStrategy(slow=res.X[0],fast=res.X[1],sign=res.X[2],rsiwindow=res.X[3],buyrsithreshold=res.X[4],sellrsithreshold=res.X[5],macdthreshold=res.X[6])
    MACDRSIBot=Bot("PSO MACD RSI Strategy",MACDRSIstrategy, startingbtc, startingaud)
    executebot(MACDRSIBot)
    
def testRSIProblem():
    Problem=RSIProblem(df)
    algorithm = PSO(adaptive=True, pop_size=100, sampling=IntegerRandomSampling(), repair=RoundingRepair(), pertube_best=False)
    res = minimize(Problem,
                algorithm,
                seed=1,
                verbose=True)
    print("Best solution found: \nX = %s\nF = $%s\nCV = %s\nG=%s\n" % (res.X, -1 * res.F[0], res.CV[0],res.G[0]))
    RSIstrategy=RSIStrategy(rsiwindow=res.X[0],buyrsithreshold=res.X[1],sellrsithreshold=res.X[2])
    RSIBot=Bot("PSO RSI Strategy",RSIstrategy, startingbtc, startingaud)
    executebot(RSIBot)
 
def testMACDProblem():
    Problem=MACDProblem(df)
    algorithm = PSO(adaptive=True, pop_size=100, sampling=IntegerRandomSampling(), repair=RoundingRepair(), pertube_best=False)
    res = minimize(Problem,
                algorithm,
                seed=1,
                verbose=True)
    print("Best solution found: \nX = %s\nF = $%s\nCV = %s\nG=%s\n" % (res.X, -1 * res.F[0], res.CV[0],res.G[0]))
    MACDstrategy=MACDStrategy(slow=res.X[0],fast=res.X[1],sign=res.X[2],macdthreshold=res.X[3])
    MACDBot=Bot("PSO MACD RSI Strategy",MACDstrategy, startingbtc, startingaud)
    executebot(MACDBot) 
    
def executebot(bot):
    print("*"*50,f'{bot.getname():^30}',"*"*50)
    bot.execute_trade(df) 
  
    print("Result:",round(bot.score(),3),"%")
    print("Total Trade Made:",len(bot.gettradingrecord())," times")
    printrecord(bot)
BHStrategy= BuyandholdStrategy()
BHBot=Bot("Buy and hold Strategy",BHStrategy, startingbtc, startingaud)
TestBots=[BHBot]

if __name__ == "__main__": 
    #testBollingerBandRSIProblem()
    #testMACDRSIProblem()
    #testRSIProblem()
    testMACDProblem()
    BHStrategy= BuyandholdStrategy()
    BHBot=Bot("Buy and hold Strategy",BHStrategy, startingbtc, startingaud)
    executebot(BHBot)
   
    

'''
# Simulates a defined number of days of trade simulations with given parameters and starting cash.
startingbtc=0
startingaud=100

BHStrategy= BuyandholdStrategy()
#PPstrategy= PPStrategy()
#BRSIstrategy= BollingerBandRSIStrategy()
#RSIstrategy= RSIStrategy()
#MACDstrategy= MACDStrategy()
MACDRSIstrategy=MACDRSIStrategy(slow=26,fast=12,sign=8,rsiwindow=14,buythreshold=40,sellthreshold=60)
#Votestrategy= VotingStrategy([MACDstrategy,RSIstrategy,PPstrategy])
BHBot=Bot("Buy and hold Strategy",BHStrategy, startingbtc, startingaud)
#PPBot=Bot("PP Support and Resistance Strategy",PPstrategy, startingbtc, startingaud)
#BRSIBot=Bot("BollingerBand RSI Strategy",BRSIstrategy, startingbtc, startingaud)
#RSIBot=Bot("RSI Strategy",RSIstrategy, startingbtc, startingaud)
#VoteBot=Bot("Voting Strategy",Votestrategy, startingbtc, startingaud)
#MACDBot=Bot("MACD Strategy",MACDstrategy, startingbtc, startingaud)
MACDRSIBot=Bot("MACD RSI Strategy",MACDRSIstrategy, startingbtc, startingaud)
TestBots=[BHBot,MACDRSIBot]
for bot in TestBots:
    print("*"*50,f'{bot.getname():^30}',"*"*50)
    bot.execute_trade(df) 
  
    print("Result:",round(bot.score(),3),"%")
    print("Total Trade Made:",len(bot.gettradingrecord())," times")
    printrecord(bot)


'''
