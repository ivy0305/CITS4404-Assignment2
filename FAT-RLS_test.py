import random
import ccxt
from Bot import *
from Strategy import *
def gettrainingdata():
    kraken=ccxt.kraken()
    kraken.load_markets()   
    ohlcdata=kraken.fetch_ohlcv("BTC/AUD",since=1620864000000,timeframe="1d",limit=60) #Since 1620864000000 to 1629417600000 earlist data
    df=pd.DataFrame(ohlcdata,columns=["timestamp","open","high","low","close","volume"])
    return df
def objective_function(df,x):
    startingbtc=0
    startingaud=100
    AIVotingstrategy=AIVotingStrategy(k_buy_threshold=x[0],k_sell_threshold=x[1],d_buy_threshold=x[2],d_sell_threshold=x[3],rsi_buy_threshold=x[4],rsi_sell_threshold=x[5])
    bot=Bot("AI Voting Strategy",AIVotingstrategy, startingbtc, startingaud)
    bot.execute_trade(df) 
    return bot.getaud()

def generate_initial_solution():
    # Generate an initial solution randomly
    list_length = 6

    # Initialize an empty list
    random_numbers = []

    # Generate random numbers and add them to the list
    for i in range(list_length):
        random_number = random.uniform(1, 100)
        random_numbers.append(int(random_number))
     
    print(random_numbers)
    return random_numbers

def perturb_solution(x, strength):
    # Perturb the solution by adding or subtracting a random value
    newsolution=[]  
    for xi in x:
      
        y = strength * random.uniform(-1, 1)
        while(xi+y<=1):
            y = strength * random.uniform(-1, 1)
        newsolution.append(int(xi+y))
    
    return newsolution

def run_tabu_search(max_iterations, tabu_size):
    # Initialize variables
    df=gettrainingdata()
    current_solution = generate_initial_solution()
    best_solution = current_solution
    best_fitness = objective_function(df,current_solution)
    tabu_list = []
    
    for i in range(max_iterations):
        # Perturb the current solution
      
        strength = 1 / (i + 1)  
        new_solution = perturb_solution(current_solution, strength)
        
        # Check if new solution is in the tabu list
        if new_solution in tabu_list:
            continue
        
        # Evaluate the new solution
        new_fitness = objective_function(df,new_solution)
        
        # Update best solution if necessary
        if new_fitness < best_fitness:
            best_fitness = new_fitness
            best_solution = new_solution
        
        # Add new solution to the tabu list
        tabu_list.append(new_solution)
        
        # Remove old solutions from the tabu list
        if len(tabu_list) > tabu_size:
            del tabu_list[0]
       
        # Move to the new solution with some probability based on fitness difference
        delta_fitness = new_fitness - objective_function(df,current_solution)
        
        acceptance_probability = min(1, 2.71828 ** (-delta_fitness / strength))
        if random.uniform(0, 1) < acceptance_probability:
            current_solution = new_solution
    
    return best_solution, best_fitness
for i in range(100):
    print( run_tabu_search(400,5))