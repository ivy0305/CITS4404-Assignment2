# CITS4404-Assignment2
## Assumption
### 1. This trading bot can sell short(Can sell BTC when you do not own any)
### 2. In the finalisation stage, the bot will sell or buy BTC untill the balance is zero
### 3. This bot can only see one candle stick data at a time 

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
