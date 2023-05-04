import ccxt
import ta
import pandas as pd
import random
import numpy as np
from deap import creator, base, tools, algorithms
import warnings
warnings.filterwarnings("ignore", message="invalid value encountered in scalar divide", category=RuntimeWarning)

# Genetic Algorithm parameters
IND_SIZE = 2
POP_SIZE = 30
N_GENERATIONS = 5
MUTATION_RATE = 0.2

# Retrieve the historical data
exchange = ccxt.kraken()

def fetch_data():
    ohlcv = exchange.fetchOHLCV('BTC/AUD', timeframe='1m')
    data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    return data 

def apply_ta(data, window, threshold):
    # ADX Indicator
    adx = ta.trend.ADXIndicator(data['high'], data['low'], data['close'], window)
    data['adx'] = adx.adx()
    data['adx_pos'] = adx.adx_pos()
    data['adx_neg'] = adx.adx_neg()

    # Determine the direction of the trend
    data['trend'] = np.where(data['adx_pos'] > data['adx_neg'], 1, -1)

    # Determine if the trend is strong enough to trade
    data['trend_strength'] = np.where(data['adx'] > threshold, True, False)

    return data

def buy_trigger(t, data):
    return (
        data.loc[t, 'trend'] == 1
        and data.loc[t - 1, 'trend'] == -1
        and data.loc[t, 'trend_strength']
        and data.loc[t, 'adx_pos'] > data.loc[t, 'adx_neg']
    )

def sell_trigger(t, data):
    return (
        data.loc[t, 'trend'] == -1
        and data.loc[t - 1, 'trend'] == 1
        and data.loc[t, 'trend_strength']
        and data.loc[t, 'adx_neg'] > data.loc[t, 'adx_pos']
    )

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
    else:
        return 0
    #print(capital)
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
toolbox.register("individual", tools.initCycle, creator.Individual, [toolbox.attr_int]*2)

# Define the population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the fitness function
toolbox.register("evaluate", evaluate_fitness)
toolbox.register("mate", tools.cxUniform, indpb = 0.5)
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
    offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.2)
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

# Print the best parameters and fitness
print(f"Best parameters: {best_params}")
print(f"Best fitness: {best_fitness}")