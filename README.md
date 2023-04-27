# CITS4404-Assignment2
## Assumption
#### 1. This trading bot has the ability to sell short, which means it can sell BTC even if the user does not own any.
#### 2. In the finalisation stage, the bot will sell or buy BTC untill the balance is zero
#### 3. This bot is designed to process one candlestick data point at a time during runtime.

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
