import ccxt
import ta
import pandas as pd
import random
import numpy as np
from deap import creator, base, tools, algorithms

# Genetic Algorithm parameters
IND_SIZE = 2
POP_SIZE = 10
N_GENERATIONS = 5
MUTATION_RATE = 0.1

# Retrieve the historical data
exchange = ccxt.kraken()

def fetch_data():
    ohlcv = exchange.fetchOHLCV('BTC/AUD', timeframe='1m')
    data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    return data 

def apply_ta(data, window, stddev):
    # BollingerBands Indicator
    bb = ta.volatility.BollingerBands(data['close'], window=window, window_dev=stddev)
    data['bb_upperband'] = bb.bollinger_hband()
    data['bb_lowerband'] = bb.bollinger_lband()

    return data

def buy_trigger(t, data):
    return data.loc[t, 'close'] < data.loc[t, 'bb_lowerband']

def sell_trigger(t, data):
    return data.loc[t, 'close'] > data.loc[t, 'bb_upperband']

def evaluate_bot(data, short_window, long_window, initial_capital=100, fee_percentage=0.02):
    data = apply_ta(data, short_window, long_window)
    capital = initial_capital
    btc_holding = 0
    bought = False

    for t in range(1, len(data)):
        if not bought and buy_trigger(t, data) and not buy_trigger(t - 1, data) and not (sell_trigger(t, data) and not sell_trigger(t - 1, data)):
            btc_purchase = capital * (1 - fee_percentage)
            btc_holding = btc_purchase / data.loc[t, 'close']
            capital = 0
            bought = True
        elif bought and sell_trigger(t, data) and not sell_trigger(t - 1, data) and not (buy_trigger(t, data) and not buy_trigger(t - 1, data)):
            capital = btc_holding * data.loc[t, 'close'] * (1 - fee_percentage)
            btc_holding = 0
            bought = False

    # Sell the remaining BTC holding at the close of the last day
    if bought:
        capital = btc_holding * data.loc[len(data) - 1, 'close'] * (1 - fee_percentage)

    return capital

# ------------------------------------------------------
# GENETIC ALGORITHM BIT STARTS HERE

def select_parents(population, fitness_values):
    selected_parents = []
    for i in range(2):
        idx = np.random.choice(len(population), size=3, replace=False)
        fitness_scores = [fitness_values[i] for i in idx]
        selected_parents.append(population[idx[np.argmax(fitness_scores)]])
    return selected_parents

def crossover(parents):
    child = []
    for i in range(len(parents[0])):
        if random.random() < 0.5:
            child.append(parents[0][i])
        else:
            child.append(parents[1][i])
    # Ensure that the child contains valid SMA window sizes
    child[0] = max(10, min(child[0], 100))
    child[1] = max(10, min(child[1], 500))
    return child

def mutation(individual):
    mutated_individual = individual.copy()
    # Choose a random SMA window size to mutate
    idx = random.randint(0, 1)
    mutated_individual[idx] = random.randint(10, 100) if idx == 0 else random.randint(100, 500)
    return mutated_individual

def evaluate_fitness(individual):
    data = fetch_data()
    data = apply_ta(data, individual[0], individual[1])
    final_capital = evaluate_bot(data, individual[0], individual[1])
    return (final_capital,)


# Run the optimization using the genetic algorithm
toolbox = base.Toolbox()
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Define the individuals
toolbox.register("attr_int", random.randint, 10, 100)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=2)

# Define the population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the fitness function
toolbox.register("evaluate", evaluate_fitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=10, up=100, indpb=MUTATION_RATE)
toolbox.register("select", tools.selTournament, tournsize=3)

# Run the optimization using the genetic algorithm
pop = toolbox.population(n=POP_SIZE)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("min", np.min)
stats.register("max", np.max)

for gen in range(N_GENERATIONS):
    offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    # Update the population with the offspring
    pop[:] = offspring
    hof.update(pop)
    
    record = stats.compile(pop)
    print(f"Generation {gen+1}: {record}")

best_params = hof[0]
best_fitness = evaluate_fitness(best_params)

def main():
    # Initialize the population
    pop = toolbox.population(n=50)

    # Run the genetic algorithm for 10 generations
    for gen in range(10):
        # Evaluate the fitness of each individual in the population
        fitnesses = map(toolbox.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # Select the next generation of individuals using tournament selection
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation to the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < 0.2:
                toolbox.mutate(mutant)
                del mutant.fitness.values

# Print the best parameters and fitness
print(f"Best parameters: {best_params}")
print(f"Best fitness: {best_fitness}")