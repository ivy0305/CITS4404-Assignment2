import ccxt
from Bot import *
import pandas as pd
kraken=ccxt.kraken()
kraken.load_markets()

ohlcdata=kraken.fetch_ohlcv("BTC/AUD",timeframe="30m",limit=700)

df=pd.DataFrame(ohlcdata,columns=["timestamp","open","high","low","close","volume"])

model="base"
startingbtc=0
startingaud=100
basebot=Bot(model, startingbtc, startingaud)
basebot.run(df)
print("Score:",basebot.score())
