import pandas as pd
import numpy as np
from Bot import *
from Strategy import *


np.set_printoptions(suppress=True) #array不顯示科學記號

def _fitness(individual,df):
    startingaud=100
   
    Votingstrategy=VotingStrategy(mfi_buy_threshold=individual[0],mfi_sell_threshold=individual[1],k_buy_threshold=individual[2],k_sell_threshold=individual[3],rsi_buy_threshold=individual[4],rsi_sell_threshold=individual[5],kd_w=individual[6],k_w=individual[7],rsi_w=individual[8],mfi_w=individual[9])
    VotingBot=Bot("AI Voting Strategy",Votingstrategy, startingaud)
    VotingBot.execute_trade(df) 

    profit=VotingBot.getaud()
    #print(profit)
    return profit
  
    
def select(pop, fitness,POP_SIZE):
    idx = np.random.choice(np.argsort(fitness)[-20:], size=POP_SIZE)
    return pop[idx]


# mating process (genes crossover)
def crossover(parent, pop,DNA_SIZE,CROSS_RATE,POP_SIZE):     
    if np.random.rand() < CROSS_RATE:                            
        i_ = np.random.randint(0, POP_SIZE, size=1)                           
        cross_points = np.random.randint(0, 2, size=DNA_SIZE).astype(bool)
        parent[cross_points] = pop[i_, cross_points]

    return parent


def mutate(parent,DNA_SIZE,MUTATION_RATE):
    for point in range(DNA_SIZE):
        if np.random.rand() < MUTATION_RATE :
            if point < 5:
                parent[point] = round(np.random.uniform(0,100),0)
            else:
                parent[point] = round(np.random.uniform(0,2),2)
    return parent

def trainGA(df, parameter_size = 10,n_individuals = 100,cross_rate = 0.5,mutation_rate = 0.2,n_generation= 50):
    DNA_SIZE = parameter_size            # DNA length
    POP_SIZE = n_individuals      # population size
    CROSS_RATE = cross_rate       # mating probability (DNA crossover)
    MUTATION_RATE = mutation_rate   # mutation probability
    N_GENERATIONS = n_generation

    pop = np.random.uniform(5,95,(POP_SIZE,DNA_SIZE)).round(0)
    pop[:,5] = np.random.uniform(0,2,POP_SIZE).round(2)
    pop[:,6] = np.random.uniform(0,2,POP_SIZE).round(2)
    pop[:,7] = np.random.uniform(0,2,POP_SIZE).round(2)
    pop[:,8] = np.random.uniform(0,2,POP_SIZE).round(2)
    pop[:,9] = np.random.uniform(0,2,POP_SIZE).round(2)

    
    fitness = np.array([_fitness(individual,df)for individual in pop])
    
    
    for i in range(N_GENERATIONS):
    #GA part (evolution)
        pop_copy = pop.copy()
        for parent in pop:
            child = crossover(parent, pop_copy,DNA_SIZE,CROSS_RATE,POP_SIZE)
            child = mutate(child,DNA_SIZE,MUTATION_RATE)
            parent[:] = child       # parent is replaced by its child
            
        pop = select(pop, fitness,POP_SIZE) #從pop中挑適應值好的個體 取代pop
        
        fitness = np.array([_fitness(individual,df)for individual in pop])
        
        print(f"Generation  {(i+1)}:\t Solution: {pop[np.argmax(fitness)]}\t Fitness: {fitness[np.argmax(fitness)]}")    
    return pop[np.argmax(fitness), :],fitness[np.argmax(fitness)]*-1
          








