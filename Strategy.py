import numpy as np
import random
import pandas as pd
class Strategy:

    def __init__(self):
        pass

    def decide(self, row):
        action="hold"
        if(pd.isna(row["upperband"]) ):
                return action
        if(row["close"]<row["S1"] and row["isuptrend"]):
            action="sell"
        if(row["close"]>row["R1"] and not row["isuptrend"]):
            action="buy"
        return action
        #done
