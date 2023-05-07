import random
import ccxt
import numpy as np
from Bot import *
from Strategy import *
def gettrainingdata():
    kraken=ccxt.kraken()
    kraken.load_markets()   
    ohlcdata=kraken.fetch_ohlcv("BTC/AUD",since=1620864000000,timeframe="1d",limit=60) #Since 1620864000000 to 1629417600000 earlist data
    df=pd.DataFrame(ohlcdata,columns=["timestamp","open","high","low","close","volume"])
    return df
def objective_function(df,x):
    startingaud=100
    Votingstrategy=VotingStrategy(mfi_buy_threshold=x[0],mfi_sell_threshold=x[1],k_buy_threshold=x[2],k_sell_threshold=x[3],rsi_buy_threshold=x[4],rsi_sell_threshold=x[5],kd_w=x[6],k_w=x[7],rsi_w=x[8],mfi_w=x[9])
    bot=Bot("AI Voting Strategy",Votingstrategy, startingaud)
    bot.execute_trade(df) 
    return bot.getaud()

def generate_initial_solution():
    # Generate an initial solution randomly
    list_length = 10
    # Initialize an empty list
    random_numbers = []

    # Generate random numbers and add them to the list
    for i in range(list_length):
        
        if(i>5):
            random_number = random.uniform(0, 2)
            random_numbers.append(round(random_number,2))
        else:
            random_number = random.uniform(5, 95)
            random_numbers.append(int(random_number))
     

    return random_numbers

def perturb_solution(x, strength):
    # Perturb the solution by adding or subtracting a random value
    newsolution=[]  
    for i in range(len(x)):
        if(i>5):
            y = strength * 0.1 *random.uniform(-1, 1)
            if(x[i]+y<1):
                y = strength * 0.1 *random.uniform(0, 1)
            if(x[i]+y>2):
                y = strength * 0.1 *random.uniform(-1, 0)
            newsolution.append(round(x[i]+y,2))
        else:
            y = strength * random.uniform(-1, 1)
            if(x[i]+y<5):
                y = strength *random.uniform(0, 1)
            if(x[i]+y>95):
                y = strength *random.uniform(-1, 0)
                
            newsolution.append(int(x[i]+y))
    
    return newsolution

def run_tabu_search(df,max_iterations,beta,id, tabu_size):
    s_shaped_function = lambda x: 1 / ( 1 + (x/(1-x))**(-beta) )
    
    current_solution = generate_initial_solution()
    best_solution = current_solution
    best_fitness = objective_function(df,current_solution)
    tabu_list = []
    
    for nfev in range(2,max_iterations+1):
        # Perturb the current solution
        
        norm_nfev = np.clip(nfev/max_iterations, 0.01, 0.99)
        d = int(np.round(id*(1-s_shaped_function(norm_nfev))))
        if d<1: 
            d = 1
        new_solution = perturb_solution(current_solution, d)
        
        # Check if new solution is in the tabu list
        while new_solution in tabu_list:
            new_solution = perturb_solution(current_solution, d)
        
        # Evaluate the new solution
        new_fitness = objective_function(df,new_solution)
        
        # Update best solution if necessary
        if new_fitness > best_fitness:
            best_fitness = new_fitness
            best_solution = new_solution
        
        # Add new solution to the tabu list
        tabu_list.append(new_solution)
        
        # Remove old solutions from the tabu list
        if len(tabu_list) > tabu_size:
            del tabu_list[0]
       

    return best_solution, best_fitness

def trainFATRLS(df,max_iterations,beta,id,tabu_size):
    random.seed(23)
    best_fitness=0
    best_solution=[]
  
    for i in range(20):
        solution, fitness= run_tabu_search(df,max_iterations,beta,id, tabu_size)
        if(fitness>best_fitness):
            best_fitness=fitness
            best_solution=solution
        print(f"Iterations  {(i+1)}:\t Solution: {solution}\t Fitness: {fitness}")
    return best_solution, best_fitness
         