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
class BTCProblem(ElementwiseProblem):
    def __init__(self,df):
        super().__init__(n_var=7,
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=np.array([1, 1, 1, 1,1, 0,-100]),
                         xu=np.array([50, 50, 50, 100, 100, 99,100]),
                         vtype=int)
        self.df=df

    def _evaluate(self, x, out, *args, **kwargs):
        startingbtc=0
        startingaud=100
        MACDRSIstrategy=MACDRSIStrategy(slow=x[0],fast=x[1],sign=x[2],rsiwindow=x[3],buythreshold=x[4],sellthreshold=x[5],macdthreshold=x[6])
        MACDRSIBot=Bot("MACD RSI Strategy",MACDRSIstrategy, startingbtc, startingaud)
        MACDRSIBot.execute_trade( self.df) 
        out["F"] = MACDRSIBot.getaud()*-1

        out["G"] = x[1] - x[0]-1
   
# *** Simulations *** #

