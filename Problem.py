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

  

class AIVotingProblem(ElementwiseProblem):
    def __init__(self,df):
        super().__init__(n_var=10,
                         n_obj=1,
                         n_ieq_constr=3,
                         xl=np.array([5, 5, 5, 5, 5, 5,0,0,0,0]),
                         xu=np.array([95, 95, 95, 95, 95, 95,2,2,2,2]),
                         vtype=int)
        self.df=df

    def _evaluate(self, x, out, *args, **kwargs):
        startingaud=100
   
        AIMACDRSIstrategy=AIVotingStrategy(mfi_buy_threshold=x[0],mfi_sell_threshold=x[1],k_buy_threshold=x[2],k_sell_threshold=x[3],rsi_buy_threshold=x[4],rsi_sell_threshold=x[5],kd_w=x[6],k_w=x[7],rsi_w=x[8],mfi_w=x[9])
        AIMACDRSIBot=Bot("AI Voting Strategy",AIMACDRSIstrategy, startingaud)
        AIMACDRSIBot.execute_trade(self.df) 

        f1=AIMACDRSIBot.getaud()*-1

      
        #print(np.array((f1,f2)))
        out["F"] =[f1]
        #print(out["F"])
        g1=x[0]-x[1]-1
        g2=x[2]-x[3]-1
        g3=x[4]-x[5]-1
        out["G"] =[g1,g2,g3]