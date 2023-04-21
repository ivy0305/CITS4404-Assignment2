import ta
import ccxt
import pandas as pd
from ta.volatility import BollingerBands, AverageTrueRange


from datetime import datetime

kraken=ccxt.kraken()
kraken.load_markets()
# Create a session

print("*"*50,"get_ohlc_data","*"*50)


ohlcdata=kraken.fetch_ohlcv("BTC/AUD",limit=72120)

df=pd.DataFrame(ohlcdata,columns=["timestamp","open","high","low","close","volume"])
print(df)
print(df["close"])
bb_indicator=BollingerBands(df["close"])
upperband=bb_indicator.bollinger_hband()
print(upperband[19:])
lowerband=bb_indicator.bollinger_lband()
print(lowerband[19:])
moving_average=bb_indicator.bollinger_mavg()
print(moving_average[19:])

'''
dayohlc=kr.get_ohlc_data(tradepair,interval=1440)

dayohlc[0]["time"] = [datetime.fromtimestamp(x) for x in dayohlc[0]["time"]]
print(dayohlc[0])
print("*"*50,"get_recent_spreads","*"*50)

recenttrade=kr.get_recent_spreads(tradepair)
recenttrade[0]["time"] = [datetime.fromtimestamp(x) for x in recenttrade[0]["time"]]
print(recenttrade)

# Check the Kraken API system status
print("Kraken API system status:",kr.get_system_status())
'''

