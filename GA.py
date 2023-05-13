import numpy as np
from Bot import *
from Strategy import *
import random

np.set_printoptions(suppress=True) 

def _fitness(individual,df):
    startingaud=100
    Votingstrategy=VotingStrategy(mfi_buy_threshold_divergence=individual[0],mfi_sell_threshold_divergence=individual[1],d_buy_threshold_divergence=individual[2],d_sell_threshold_divergence=individual[3],d_w=individual[4],kd_w=individual[5],ema_w=individual[6],mfi_w=individual[7])
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
            if point < 4:
                parent[point] = round(np.random.uniform(-15,15),0)
            elif(point==6):
                parent[point] = round(np.random.uniform(1,3),2)
            else:
                parent[point] = round(np.random.uniform(1,5),2)
    return parent

def trainGA(df, parameter_size = 8,n_individuals = 100,cross_rate = 0.5,mutation_rate = 0.2,n_generation= 50):
    DNA_SIZE = parameter_size            # DNA length
    POP_SIZE = n_individuals      # population size
    CROSS_RATE = cross_rate       # mating probability (DNA crossover)
    MUTATION_RATE = mutation_rate   # mutation probability
    N_GENERATIONS = n_generation
    np.random.seed(42)
    pop = np.random.uniform(-15,15,(POP_SIZE,DNA_SIZE)).round(0)
    pop[:,4] = np.random.uniform(2,5,POP_SIZE).round(2)
    pop[:,5] = np.random.uniform(1,5,POP_SIZE).round(2)
    pop[:,6] = np.random.uniform(1,3,POP_SIZE).round(2)
    pop[:,7] = np.random.uniform(1,5,POP_SIZE).round(2)


    
    fitness = np.array([_fitness(individual,df)for individual in pop])
  
    
    for i in range(N_GENERATIONS):
    #GA part (evolution)
        pop_copy = pop.copy()
        for parent in pop:
            child = crossover(parent, pop_copy,DNA_SIZE,CROSS_RATE,POP_SIZE)
            child = mutate(child,DNA_SIZE,MUTATION_RATE)
            parent[:] = child       # parent is replaced by its child
            
        pop = select(pop, fitness,POP_SIZE) 
        
        fitness = np.array([_fitness(individual,df)for individual in pop])
        
        print(f"Generation  {(i+1)}:\t Solution: {pop[np.argmax(fitness)]}\t Fitness: {fitness[np.argmax(fitness)]}")    
    return pop[np.argmax(fitness), :],fitness[np.argmax(fitness)]*-1
          








