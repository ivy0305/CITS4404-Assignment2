import ta
from krakipy import KrakenAPI
from datetime import datetime
# Create a session
kr = KrakenAPI()
tradepair="XBTAUD"
df= kr.get_tradable_asset_pairs()
#print(df.to_string())
# Get Ticker for Bitcoin/EUR
print("*"*50,"get_ticker_information","*"*50)
print(kr.get_ticker_information(tradepair))
print("*"*50,"get_ohlc_data","*"*50)

dayohlc=kr.get_ohlc_data(tradepair,interval=1440)

dayohlc[0]["time"] = [datetime.fromtimestamp(x) for x in dayohlc[0]["time"]]
print(dayohlc[0])
print("*"*50,"get_recent_spreads","*"*50)

recenttrade=kr.get_recent_spreads(tradepair)
recenttrade[0]["time"] = [datetime.fromtimestamp(x) for x in recenttrade[0]["time"]]
print(recenttrade)

# Check the Kraken API system status
print("Kraken API system status:",kr.get_system_status())
