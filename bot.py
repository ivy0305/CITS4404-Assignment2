import ccxt
import ta
import pandas as pd

# Retrieve the historical data
exchange = ccxt.kraken()

# ticker = exchange.fetch_ticker('BTC/AUD')
# print(ticker)

def fetch_data():
    ohlcv = exchange.fetchOHLCV('BTC/AUD', timeframe = '1m')
    data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    return data 

def apply_ta(data):
    # SMA Indicator
    data['sma_short'] = ta.trend.SMAIndicator(data['close'], window=50).sma_indicator()
    data['sma_long'] = ta.trend.SMAIndicator(data['close'], window=200).sma_indicator()

    # EMA Indicator
    # data['ema_short'] = ta.trend.EMAIndicator(data['close'], window=50).ema_indicator()
    # data['ema_long'] = ta.trend.EMAIndicator(data['close'], window=200).ema_indicator()

    return data

def buy_trigger(t, data):
    return data.loc[t, 'sma_short'] > data.loc[t, 'sma_long']
    # return data.loc[t, 'ema_short'] > data.loc[t, 'ema_long']     # EMA Indicator

def sell_trigger(t, data):
    return data.loc[t, 'sma_short'] < data.loc[t, 'sma_long']
    # return data.loc[t, 'ema_short'] < data.loc[t, 'ema_long']     # EMA Indicator

def execute_trade(data):
    bought = False
    for t in range(1, len(data)):
        if not bought and buy_trigger(t, data) and not buy_trigger(t - 1, data) and not (sell_trigger(t, data) and not sell_trigger(t - 1, data)):
            print(f"Buy signal at t={t}, price={data.loc[t, 'close']}")
            bought = True
        elif bought and sell_trigger(t, data) and not sell_trigger(t - 1, data) and not (buy_trigger(t, data) and not buy_trigger(t - 1, data)):
            print(f"Sell signal at t={t}, price={data.loc[t, 'close']}")
            bought = False
        
        # Sell at the close of the last day if the asset has been bought
        if bought and t == len(data) - 1:
            print(f"Sell signal at t={t} (close of last day), price={data.loc[t, 'close']}")
            bought = False

def evaluate_bot(data, initial_capital=100, fee_percentage=0.02):
    capital = initial_capital
    btc_holding = 0
    bought = False

    for t in range(1, len(data)):
        if not bought and buy_trigger(t, data) and not buy_trigger(t - 1, data) and not (sell_trigger(t, data) and not sell_trigger(t - 1, data)):
            btc_purchase = capital * (1 - fee_percentage)
            btc_holding = btc_purchase / data.loc[t, 'close']
            capital = 0
            bought = True
        elif bought and sell_trigger(t, data) and not sell_trigger(t - 1, data) and not (buy_trigger(t, data) and not buy_trigger(t - 1, data)):
            capital = btc_holding * data.loc[t, 'close'] * (1 - fee_percentage)
            btc_holding = 0
            bought = False

    # Sell the remaining BTC holding at the close of the last day
    if bought:
        capital = btc_holding * data.loc[len(data) - 1, 'close'] * (1 - fee_percentage)

    return capital

def main():
    data = fetch_data()
    data = apply_ta(data)
    execute_trade(data)
    final_capital = evaluate_bot(data)
    print('---------')
    print(f"Final capital: AUD {final_capital:.2f}\n")


if __name__ == '__main__':
    main()