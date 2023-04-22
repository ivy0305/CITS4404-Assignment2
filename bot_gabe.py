import ccxt
import talib
import pandas as pd
import numpy as np

exchange = ccxt.kraken()
symbol = 'BTC/AUD'
budget = 100
max_amount = 0.001
holding = 'AUD'

ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1d')

df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

sma9 = talib.SMA(df['close'], timeperiod=9)
sma21 = talib.SMA(df['close'], timeperiod=21)

if np.logical_and(sma9.shift(1) > sma21.shift(1), sma9 < sma21).iloc[-1]:
    # SMA9 just crossed below SMA21, trigger a buy order
    if holding == 'AUD':
        amount = min(max_amount, budget / ohlcv[-1][4])
        order = exchange.create_order(symbol, type='market', side='buy', amount=amount)
        print(f"Buy order placed: {order}")
        budget -= amount * ohlcv[-1][4] * 1.02
        holding = 'BTC'
elif np.logical_and(sma9.shift(1) < sma21.shift(1), sma9 > sma21).iloc[-1]:
    # SMA9 just crossed above SMA21, trigger a sell order
    if holding == 'BTC':
        amount = min(max_amount, exchange.fetch_balance()[symbol.split('/')[0]]['free'])
        order = exchange.create_order(symbol, type='market', side='sell', amount=amount)
        print(f"Sell order placed: {order}")
        budget += amount * ohlcv[-1][4] * 0.98
        holding = 'AUD'

if holding == 'BTC':
    close_price = exchange.fetch_ticker(symbol)['close']
    budget += amount * close_price * 0.98

print(f"Final budget: {budget:.2f} AUD")
