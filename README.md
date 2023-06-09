# CITS4404-Assignment2
## Assumption
#### 1.The bot starts with one hundred Australian dollars (AUD).
#### 2.The bot swaps all of its AUD for BTC when it receives the first buy trigger, then sells it all when it gets the subsequent sell trigger (any intermediate buy triggers after
#### 3.Purchasing and before selling are ignored. It then buys again on the next buy trigger, and so on.
#### 4.Each buy or sell event costs 2% of current holdings.
#### 5.At the end of the test period the holding is sold (if currently in BTC) at the close price and evaluated in AUD.
## Setup
1. Clone this project
```
git clone https://github.com/ivy0305/CITS4404-Assignment2.git
```
2. Install the required packages
```
pipenv install
```
3. Run the pipenv script in pipenv
```
pipenv run start
```

## Code File Description
#### Bot.py : 
1.	Calculate and Record data related to Transaction (e.g. Profit, Trading record)
2.	Implement the language of the assignment
3.	Act according to the assign strategy
#### Strategy.py :
Strategies Used - Particle Swarm Optimisation, Fast Local Search Optimisation
1.	Calculate TA Indicators
2.	Implement the trading logic
3.	Return an action from [hold, buy, sell]
#### Problem.py:
1.	Define objective function and constrains
2.	Define training Parameters
#### Run_test.py:
1.	The Main file on this application
2.	Initalization
3.	Handle the process of the test
4.	Evaluate preformance
5.	Output a txt file to Output folder
#### FATRLS.py:
1.  Implement FATRLS algorithm
#### GA.py:
1.  Implement GA algorithm
