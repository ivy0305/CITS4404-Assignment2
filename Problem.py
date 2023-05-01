import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.optimize import minimize
from pymoo.operators.repair.rounding import RoundingRepair
from Bot import *
from Strategy import *
import ccxt
from ta.trend import MACD
from ta.momentum import RSIIndicator
class MACDRSIProblem(ElementwiseProblem):
    def __init__(self,df):
        super().__init__(n_var=7,
                         n_obj=1,
                         n_ieq_constr=2,
                         xl=np.array([1, 1, 1, 1,1, 0,-100]),
                         xu=np.array([50, 50, 50, 100, 100, 99,100]),
                         vtype=int)
        self.df=df

    def _evaluate(self, x, out, *args, **kwargs):
        startingbtc=0
        startingaud=100
        MACDRSIstrategy=MACDRSIStrategy(slow=x[0],fast=x[1],sign=x[2],rsiwindow=x[3],buyrsithreshold=x[4],sellrsithreshold=x[5],macdthreshold=x[6])
        MACDRSIBot=Bot("MACD RSI Strategy",MACDRSIstrategy, startingbtc, startingaud)
        MACDRSIBot.execute_trade( self.df) 
        out["F"] = MACDRSIBot.getaud()*-1
        g1=x[1] - x[0]-1
        g2=len(MACDRSIBot.gettradingrecord())-30
        out["G"] =[ g1,g2]
  
        
class BollingerBandRSIProblem(ElementwiseProblem):
    def __init__(self,df):
        super().__init__(n_var=5,
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=np.array([1, 1, 1, 1,1]),
                         xu=np.array([50, 50, 9, 100, 100]),
                         vtype=int
                         )
        self.df=df

    def _evaluate(self, x, out, *args, **kwargs):
        startingbtc=0
        startingaud=100
        BBRSIstrategy=BollingerBandRSIStrategy(rsiwindow=x[0],window=x[1],window_dev_square=x[2],buyrsithreshold=x[3],sellrsithreshold=x[4])
        BBRSIBot=Bot("Bollinger Band RSIStrategy",BBRSIstrategy, startingbtc, startingaud)
        BBRSIBot.execute_trade( self.df) 
        out["F"] = BBRSIBot.getaud()*-1

        out["G"] = len(BBRSIBot.gettradingrecord())-30
   
# *** Simulations *** #

class RSIProblem(ElementwiseProblem):
    def __init__(self,df):
        super().__init__(n_var=3,
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=np.array([1, 1, 1]),
                         xu=np.array([50, 100, 100 ]),
                         vtype=int
                         )
        self.df=df

    def _evaluate(self, x, out, *args, **kwargs):
        startingbtc=0
        startingaud=100
        RSIstrategy=RSIStrategy(rsiwindow=x[0],buyrsithreshold=x[1],sellrsithreshold=x[2])
        RSIBot=Bot("RSI Strategy",RSIstrategy, startingbtc, startingaud)
        RSIBot.execute_trade( self.df) 
        out["F"] = RSIBot.getaud()*-1

        out["G"] = len(RSIBot.gettradingrecord())-100
        
class MACDProblem(ElementwiseProblem):
    def __init__(self,df):
        super().__init__(n_var=4,
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=np.array([1, 1, 1, -100]),
                         xu=np.array([50, 50, 50, 100]),
                         vtype=int)
        self.df=df

    def _evaluate(self, x, out, *args, **kwargs):
        startingbtc=0
        startingaud=100
        MACDstrategy=MACDStrategy(slow=x[0],fast=x[1],sign=x[2],macdthreshold=x[3])
        MACDBot=Bot("MACD RSI Strategy",MACDstrategy, startingbtc, startingaud)
        MACDBot.execute_trade( self.df) 
        out["F"] = MACDBot.getaud()*-1
        g1=x[1] - x[0]-1
        g2=len(MACDBot.gettradingrecord())-30
        out["G"] =[ g1,g2]