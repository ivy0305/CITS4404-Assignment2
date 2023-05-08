import ccxt
from Problem import *
from Bot import *
from Strategy import *

import pandas as pd

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.optimize import minimize
from pymoo.operators.repair.rounding import RoundingRepair
import datetime 
from GA import *
from FATRLS import *
def printrecord(bot):
    print("Trade Record: ")
    for i in bot.gettradingrecord():
        if(i[1]=="sell"):
            print("Date:",datetime.datetime.fromtimestamp(i[0]/1000.0),"\tAction:",i[1],"\tPrice:",i[2],"\tAmount(BTC):",i[3],"\tCommission(AUD):",i[4],"\tNet Profit(AUD):",i[5])
            write2file(filename,f'\tDate:{datetime.datetime.fromtimestamp(i[0]/1000.0)}\tAction:{i[1]}\tPrice:{i[2]}\tAmount(BTC){i[3]}\tCommission(AUD):{i[4]}\tNet Profit(AUD):{i[5]}\n')
        else:
            print("Date:",datetime.datetime.fromtimestamp(i[0]/1000.0),"\tAction:",i[1],"\tPrice:",i[2],"\tAmount(BTC):",i[3],"\tCommission(AUD):",i[4])
            write2file(filename,f'\tDate:{datetime.datetime.fromtimestamp(i[0]/1000.0)}\tAction:{i[1]}\tPrice:{i[2]}\tAmount(BTC){i[3]}\tCommission(AUD):{i[4]}\n')
        




def get_BTCAUDdata(startingbased,nday):
    ohlcdata=kraken.fetch_ohlcv("BTC/AUD",since=startingbased,timeframe="1d",limit=nday) 
    df=pd.DataFrame(ohlcdata,columns=["timestamp","open","high","low","close","volume"])
    return df


def trainPSOVotingProblem(train_data):
    write2file(filename,f'Particle Swarm Optimization:\n')
    Problem=VotingProblem(train_data)
    #algorithm=GA(pop_size=100,sampling=IntegerRandomSampling())
    algorithm = PSO(adaptive=True, pop_size=100, sampling=IntegerRandomSampling(),repair=RoundingRepair(),  pertube_best=False)
    res = minimize(Problem,
                algorithm,
                seed=1,
                verbose=True)
    print("Best solution found: \nX = %s\nF = $%s\n" % (res.X, -1 * res.F[0]))
    
    return res.X,res.F[0]
def trainGAVotingProblem(train_data):
    write2file(filename,f'Genetic Algorithm Optimization:\n')
    x,fitness=trainGA(train_data, parameter_size = 8,n_individuals = 100,cross_rate = 0.5,mutation_rate = 0.2,n_generation= 50)
    print("Best solution found: \nX = %s\nF = $%s\n" % (x,  -1*fitness))
    return x, fitness

def trainFATRLSVotingProblem(train_data):
    write2file(filename,f'FATRLS Algorithm Optimization:\n')
    x,fitness=trainFATRLS(train_data,max_iterations=50,beta=1.2,id=train_data.shape[0]//2,tabu_size=train_data.shape[0])
    print("Best solution found: \nX = %s\nF = $%s\n" % (x, fitness))
    return x, fitness

def testbot(bot,test_data):
    print("*"*50,f'{bot.getname():^30}',"*"*50)
    write2file(filename,f'{"="*50} {bot.getname()+" Performance with Testing Data":^80} {"="*50} \n')
    bot.execute_trade(test_data) 
  
    print("Result:",round(bot.score(),3),"%")
    print("Total Trade Made:",len(bot.gettradingrecord())/2," times")
    print("Win Trade Made:",bot.getwintime(),"times")
    
    write2file(filename,f'Profit Percentage: \t {round(bot.score(),3)}% \n')
    write2file(filename,f'Total Trade Made (Buy+Sell):\t {int(len(bot.gettradingrecord())/2)} times \n')
    write2file(filename,f'Win Rate:\t {bot.getwintime()}/{int(len(bot.gettradingrecord())/2)} \n\n')
    write2file(filename,f'Transaction Record:\n')
    printrecord(bot)
    
    return bot.getaud()

def write2file(exp_name,text):
    with open(r'Output/{}.txt'.format(exp_name),'a') as file:
        file.write(text)   
        
if __name__ == "__main__": 
  # Retrieve the historical data
    kraken=ccxt.kraken()
    kraken.load_markets()
    
    BASE=1623456000000 #Bullish market
    #BASE=1623456000000+4*MONTH #Bearish market
    #BASE=1623456000000+7*MONTH #Mix market
    DAY=86400000
    MONTH=DAY*30
    predaynumber=14
    trainingdatasize=30
    datasize=30
    

    botname="Voting Strategy"
    optimizer="GA"
    filename=datetime.datetime.today().strftime('%Y%m%d_%H%M%S')+"_"+botname
    tradingMarket="BTC/AUD"
    testmonthnumber=12
    
    Algorithmtotalprofit=0
    BuyandHoldtotalprofit=0
    startingaud=100
    bhstartingaud=100
    wincount=0
    write2file(filename,f"\nTesting Date:\t {datetime.datetime.today().strftime('%Y/%m/%d %H:%M:%S')}\nStrategy:\t {botname}\nTrading pair:\t{tradingMarket}\nStarting AUD:\t{startingaud}\nNumber of Iteration:\t{testmonthnumber}\n\n\n")
    write2file(filename,f'\n\n{"*"*180}\n\n')
    for i in range(testmonthnumber):
        print("="*160)
        print(i+1,"/",testmonthnumber)
        print("="*160)
        write2file(filename,f"Iteration:\t {i+1} / {testmonthnumber}\n\n")
        train_data=get_BTCAUDdata(BASE+MONTH*i-predaynumber*DAY,trainingdatasize+predaynumber)
        test_data=get_BTCAUDdata(BASE+(MONTH*(i+1))-predaynumber*DAY,datasize+predaynumber)
        
        write2file(filename,f'Training Data:\n\tFrom:\t { datetime.datetime.fromtimestamp(train_data.loc[0,"timestamp"]/1000.0)}\tTo:\t { datetime.datetime.fromtimestamp(train_data.loc[train_data.shape[0]-1,"timestamp"]/1000.0)}\t Size:\t{train_data.shape} \n')
        write2file(filename,f'Testing Data:\n\tFrom:\t { datetime.datetime.fromtimestamp(test_data.loc[0,"timestamp"]/1000.0)}\tTo:\t { datetime.datetime.fromtimestamp(test_data.loc[test_data.shape[0]-1,"timestamp"]/1000.0)}\t Size:\t{test_data.shape} \n\n')
        #print(train_data)
      
        #print(test_data)
        if(optimizer=="PSO"):
            best_param,train_fitness=trainPSOVotingProblem(train_data)
        elif(optimizer=="GA"):
            best_param,train_fitness=trainGAVotingProblem(train_data)
        elif(optimizer=="FATRLS"):
            best_param,train_fitness=trainFATRLSVotingProblem(train_data)
            train_fitness=train_fitness*-1
            
   
        write2file(filename,f'Best Parameter:\n\tmfi_buy_threshold_divergence=\t{best_param[0]}\n\tmfi_sell_threshold_divergence=\t{best_param[1]}\n\td_buy_threshold_divergence=\t{best_param[2]}\n\td_sell_threshold_divergence=\t{best_param[3]}\n\td_w=\t{best_param[4]}\n\tkd_w=\t{best_param[5]}\n\tema_w=\t{best_param[6]}\n\tmfi_w=\t{best_param[7]}\n')
        write2file(filename,f'Training_Fitness:{-1*train_fitness}\n\n')
     
        votingstrategy=VotingStrategy(mfi_buy_threshold_divergence=best_param[0],mfi_sell_threshold_divergence=best_param[1],d_buy_threshold_divergence=best_param[2],d_sell_threshold_divergence=best_param[3],d_w=best_param[4],kd_w=best_param[5],ema_w=best_param[6],mfi_w=best_param[7])
        votingbot=Bot(botname,votingstrategy, startingaud)
        Algorithmtotalprofit+= testbot(votingbot,test_data)
        
        write2file(filename,f'\n')
        BHStrategy= BuyandholdStrategy()
        BHBot=Bot("Buy and Hold Strategy",BHStrategy, bhstartingaud)
        BuyandHoldtotalprofit+=testbot(BHBot,test_data)
        if(votingbot.score()>BHBot.score()):
            wincount+=1
        write2file(filename,f'\n\n{"*"*180}\n\n')

     
    print("="*160)
    print(""*60)
    print("="*160)
    write2file(filename,f'\n\n\n{"="*180}\n{"Final Report":^180}\n{"="*180}\n\n')
 
    print(f'Win Rate:{wincount}/{testmonthnumber}')
    print(f'Total Profit:{Algorithmtotalprofit-startingaud*testmonthnumber}')
    print(f'Buy and Hold Total Profit:{BuyandHoldtotalprofit-startingaud*testmonthnumber}')
    
    
    write2file(filename,f'Total Win Rate:\t{wincount}/{testmonthnumber}\n')
    write2file(filename,f'Total Net Profit:\t{Algorithmtotalprofit-startingaud*testmonthnumber} AUD\n')
    write2file(filename,f'Buy and Hold Total Profit:\t{BuyandHoldtotalprofit-bhstartingaud*testmonthnumber} AUD\n')
    #testBollingerBandRSIProblem(df,startingbtc, startingaud,train_data,test_data)
    #testMACDRSIProblem(df,startingbtc, startingaud,train_data,test_data)
    #testRSIProblem(df,startingbtc, startingaud,train_data,test_data)
    #testMACDProblem(df,startingbtc, startingaud,train_data,test_data)

 

    
    
   
    

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
