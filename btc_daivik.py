import ccxt
import ta
import csv
import pandas as pd
from pymoo.operators.repair.rounding import RoundingRepair
from ta.trend import MACD
from ta.momentum import RSIIndicator

import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.optimize import minimize

# Reads data into a pandas dataframe.
data = pd.read_csv('btc_data.csv', sep=',')


class BTCProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=7,
                         n_obj=1,
                         n_ieq_constr=1,
                         xl=np.array([1, 2, 1, 0, 1, 1, 0]),
                         xu=np.array([719, 720, 720, 2, 720, 100, 99]),
                         vtype=int)

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = simulate_trades(days=len(data), parameters=[x[0], x[1], x[2], x[3], x[4], x[5], x[6]], start_cash=1000, unit=1, verbose=False) * -1

        out["G"] = x[0] - x[1]
        if x[0] == x[1]:
            out["G"] = 1


# Gets data from the Kraken exchange (BTC/AUD) for 720 data points within a specified timeframe.
def get_data(timeframe='1d'):
    # [date, open, high, low, close, volume] * 720
    # timeframe ('1d') denotes the time between each datapoint
    with open('btc_data.csv', mode='w', newline='') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['date', 'open', 'high', 'low', 'close', 'volume'])
        csv_writer.writerows(ccxt.kraken().fetch_ohlcv('BTC/AUD', timeframe))

# get_data()

# *** Triggers *** #
# Check for three MACD signals:
# 1. Signal line crossovers, when MACD histogram is positive or negative.
# 2. Centerline crossovers, when MACD line is positive or negative.
# 3. Divergences, when a new lowest price happens, check if the MACD line is also at its lowest.
#    If it isn't, there's an uptrend possible, etc. (maybe have a divergence threshold parameter for triggers?)


# Determines whether a buy trigger occurs.
def buy_trigger(macd_line, macd_hist, rsi, day, parameters):
    # If day is under 25, MACD indicators can't really do anything.
    if day < parameters[1] - 1:
        return False

    # As we are buying/selling at the open prices, we must use the previous day's MACD values - as MACD indicators
    # use closing prices only (while we are acting at the start of the day).
    day = day - 1

    # As 33 is the first valid day for using the MACD signal line, anything under only considers the MACD line.
    # TODO: change if required.
    if day < parameters[2] + parameters[1] - 2:
        if parameters[3] >= 1:
            return macd_line[day] > 0 and rsi[day] < parameters[5]
        return macd_line[day] > 0

    if parameters[3] >= 1:
        return macd_hist[day] > 0 and rsi[day] < parameters[5]
    return macd_hist[day] > 0


# Determines whether a sell trigger occurs.
def sell_trigger(macd_line, macd_hist, rsi, day, parameters):
    # If day is under 25, MACD indicators can't really do anything.
    if day < parameters[1] - 1:
        return False

    # As we are buying/selling at the open prices, we must use the previous day's MACD values - as MACD indicators
    # use closing prices only (while we are acting at the start of the day).
    day = day - 1

    # As 33 is the first valid day for using the MACD signal line, anything under only considers the MACD line.
    # TODO: change if required.
    if day < parameters[2] + parameters[1] - 2:
        if parameters[3] >= 1:
            return macd_line[day] < 0 and rsi[day] > parameters[6]
        return macd_line[day] < 0

    if parameters[3] >= 1:
        return macd_hist[day] < 0 and rsi[day] > parameters[6]
    return macd_hist[day] < 0


# *** Simulations *** #


# Simulates a defined number of days of trade simulations with given parameters and starting cash.
def simulate_trades(days=len(data), parameters=[12, 26, 9, 1, 14, 30, 70], start_cash=100, unit=1, verbose=True):
    # Defines variables. (initially set to sell trigger so the bot purchases first)
    btc = 0
    is_buy = False
    is_sell = True

    # Defines statistical variables.
    # The cash highs/lows are only updated after sell triggers.
    cash = start_cash
    cash_high = cash
    cash_low = cash

    # Defines the gross profit and gross loss, alongside previous cash to calculate these.
    gross_profit = 0
    gross_loss = 0
    previous_cash = cash

    # Creates a TA indicator for MACD.
    ind_macd = MACD(close=data["close"], window_fast=parameters[0], window_slow=parameters[1], window_sign=parameters[2])
    ind_rsi = RSIIndicator(data["close"], window=parameters[4])
    macd_line = ind_macd.macd()
    macd_hist = ind_macd.macd_diff()
    rsi = ind_rsi.rsi()

    # TODO: add graphing, etc.
    # Iterates through every requested day from the first day onwards.
    for day in range(days):
        if verbose:
            print(f"**Day {(day + 1) * unit}**\nCash: ${cash}\nBTC: {btc}\nOpen: ${data['open'][day]}\nClose: ${data['close'][day]}\n")

        # If a trigger is not in place already, a buy or sell trigger is initiated if necessary.
        # A trigger results in the negation of the buy/sell states, indicating that a change has occurred.
        # The 0.98 multiplier effectively acts as the 2% holding deduction on an action.
        if not is_buy and buy_trigger(macd_line, macd_hist, rsi, day, parameters):
            is_buy, is_sell = not is_buy, not is_sell
            btc = (cash/data['open'][day]) * 0.98
            cash = 0

        elif not is_sell and sell_trigger(macd_line, macd_hist, rsi, day, parameters):
            is_sell, is_buy = not is_sell, not is_buy
            cash = (btc*data['open'][day]) * 0.98
            btc = 0

            if cash - previous_cash > 0:
                gross_profit += cash - previous_cash
            else:
                gross_loss += abs(cash - previous_cash)
            previous_cash = cash

            cash_high = max(cash, cash_high)
            cash_low = min(cash, cash_low)

        if cash == 0 and btc == 0:
            if verbose:
                print("\033[91m" + "You are broke lol" + "\033[0m")
            break

    # Sells all BTC on the final day at the closing price, if currently on a buy trigger.
    if is_buy:
        cash = btc * data['close'][days - 1]
        cash_high = max(cash, cash_high)
        cash_low = min(cash, cash_low)

    # Random filler code to make the output profit colours print more nicely.
    profit = cash - start_cash
    header = "\033[92m" if profit > 0 else "\033[91m" if profit < 0 else "\033[93m"

    # Calculates profit factor.
    if gross_loss > 0:
        pf = gross_profit/gross_loss
    else:
        pf = 92349242

    # Prints the final simulation results.
    if verbose:
        print("**Simulation Results**\nCash: ${:0.2f}\nProfit: {:}${:0.2f}\n\033[0m".format(cash, header, profit, pf))
        print("Min: ${:0.2f}\nMax: ${:0.2f}".format(cash_low, cash_high))

    return profit


# simulate_trades(start_cash=1000, unit=7)
problem = BTCProblem()
algorithm = PSO(adaptive=True, pop_size=100, sampling=IntegerRandomSampling(), repair=RoundingRepair(), pertube_best=False)

res = minimize(problem,
               algorithm,
               seed=1,
               verbose=True)
print("Best solution found: \nX = %s\nF = $%s\nCV = %s" % (res.X, -1 * res.F[0], res.CV[0]))

simulate_trades(parameters=list(res.X), start_cash=1000)
