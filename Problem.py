import numpy as np
from pymoo.core.problem import ElementwiseProblem

from Bot import *
from Strategy import *


  

class VotingProblem(ElementwiseProblem):
    def __init__(self,df):
        super().__init__(n_var=8,
                         n_obj=1,
                         xl=np.array([-15, -15, -15, -15,1,1,1,1]),
                         xu=np.array([15, 15, 15, 15,5,5,3,5]),
                         vtype=int)
        self.df=df

    def _evaluate(self, x, out, *args, **kwargs):
        startingaud=100
        Votingstrategy=VotingStrategy(mfi_buy_threshold_divergence=x[0],mfi_sell_threshold_divergence=x[1],d_buy_threshold_divergence=x[2],d_sell_threshold_divergence=x[3],d_w=x[4],kd_w=x[5],ema_w=x[6],mfi_w=x[7])
        VotingBot=Bot("Voting Strategy",Votingstrategy, startingaud)
        VotingBot.execute_trade(self.df) 

        f1=VotingBot.getaud()*-1

      
        #print(np.array((f1,f2)))
        out["F"] =[f1]
        #print(out["F"])
     