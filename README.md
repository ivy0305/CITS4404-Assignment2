# CITS4404-Assignment2
## Assumption
#### 1.The bot starts with one hundred Australian dollars (AUD).
#### 2.The bot swaps all of its AUD for BTC when it receives the first buy trigger, then sells it all when it gets the subsequent sell trigger (any intermediate buy triggers after #### 3.purchasing and before selling are ignored). It then buys again on the next buy trigger, and so on.
#### 4.Each buy or sell event costs 2% of current holdings.
#### 5.At the end of the test period the holding is sold (if currently in BTC) at the close price and evaluated in AUD.
## Setup
1. Clone this project
```
git clone https://github.com/ivy0305/CITS4404-Assignment2.git
```
2. Switch to kc_bot branch
```
git checkout kc_bot
```
3. Install the required packages
```
pipenv install
```
4. Activate the virtual environment 
```
pipenv shell
```
5. Run the bot
```
python run_test.py
```
## Code File
#### run_test.py
1. Read data
2. Initalise indicators for the data
3. Initalise strategy and bot
4. Evaluate preformance
#### Bot.py
1. Calculate profit of the trades
2. Execute trades according to assigned strategy's decision
#### Strategy.py
1. Trading logic
2. Decide action for bot
