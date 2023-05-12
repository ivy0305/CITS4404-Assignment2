import random
import numpy as np
from Bot import *
from Strategy import *

def objective_function(df,x):
    startingaud=100
    Votingstrategy=VotingStrategy(mfi_buy_threshold_divergence=x[0],mfi_sell_threshold_divergence=x[1],d_buy_threshold_divergence=x[2],d_sell_threshold_divergence=x[3],d_w=x[4],kd_w=x[5],ema_w=x[6],mfi_w=x[7])
    bot=Bot("AI Voting Strategy",Votingstrategy, startingaud)
    bot.execute_trade(df) 
    return bot.getaud()

def generate_initial_solution():
    # Generate an initial solution randomly
    list_length = 8
    # Initialize an empty list
    random_numbers = []

    # Generate random numbers and add them to the list
    for i in range(list_length):
      
        if(i<4):
            random_number = random.uniform(-15,15)
            random_numbers.append(int(random_number))
        elif(i==6):
            random_number = random.uniform(1,3)
            random_numbers.append(int(random_number))
        else:
            random_number = random.uniform(1,5)
            random_numbers.append(int(random_number))
     

    return random_numbers

def perturb_solution(x, strength):
    # Perturb the solution by adding or subtracting a random value
    newsolution=[]  
    for i in range(len(x)):
        if(i>3):
            y = strength * 0.1 *random.uniform(-1, 1)
            if(x[i]+y<0):
                y = strength * 0.1 *random.uniform(0, 1)
            if(x[i]+y>5):
                y = strength * 0.1 *random.uniform(-1, 0)
            newsolution.append(round(x[i]+y,2))
        elif(i==6):
            y = strength * 0.1 *random.uniform(-1, 1)
            if(x[i]+y<0):
                y = strength * 0.1 *random.uniform(0, 1)
            if(x[i]+y>3):
                y = strength * 0.1 *random.uniform(-1, 0)
            newsolution.append(round(x[i]+y,2))
        else:
            y = strength * random.uniform(-1, 1)
            if(x[i]+y<-15):
                y = strength *random.uniform(0, 1)
            if(x[i]+y>15):
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
    random.seed(176)
    best_fitness=0
    best_solution=[]
  
    for i in range(20):
        solution, fitness= run_tabu_search(df,max_iterations,beta,id, tabu_size)
        if(fitness>best_fitness):
            best_fitness=fitness
            best_solution=solution
        print(f"Iterations  {(i+1)}:\t Solution: {solution}\t Fitness: {fitness}")
    return best_solution, best_fitness
         