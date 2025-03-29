import numpy as np
import random
import matplotlib.pyplot as plt

# Disk parameters
disk_size = 200  # Total cylinders in disk
num_requests = 10  # Number of I/O requests

# Generate random disk requests
requests = np.random.randint(0, disk_size, num_requests)
initial_head = np.random.randint(0, disk_size)

# Genetic Algorithm parameters
population_size = 20
mutation_rate = 0.1
num_generations = 100

def fitness(schedule):
    """Calculate total seek time for a given schedule."""
    seek_time = abs(initial_head - schedule[0])
    for i in range(1, len(schedule)):
        seek_time += abs(schedule[i] - schedule[i - 1])
    return -seek_time  # Negative because we want to minimize seek time

def create_population():
    """Generate initial random population of disk request sequences."""
    return [random.sample(list(requests), len(requests)) for _ in range(population_size)]

def select_parents(population):
    """Select two parents using tournament selection."""
    selected = random.sample(population, 5)  # Tournament size 5
    return sorted(selected, key=fitness, reverse=True)[:2]

def crossover(parent1, parent2):
    """Perform ordered crossover."""
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]
    
    ptr = 0
    for gene in parent2:
        if gene not in child:
            while child[ptr] is not None:
                ptr += 1
            child[ptr] = gene
    return child

def mutate(schedule):
    """Randomly swap two positions in the schedule with some probability."""
    if random.uniform(0, 1) < mutation_rate:
        i, j = random.sample(range(len(schedule)), 2)
        schedule[i], schedule[j] = schedule[j], schedule[i]
    return schedule

# Genetic Algorithm execution
population = create_population()
for _ in range(num_generations):
    new_population = []
    for _ in range(population_size // 2):
        parent1, parent2 = select_parents(population)
        child1, child2 = crossover(parent1, parent2), crossover(parent2, parent1)
        new_population.extend([mutate(child1), mutate(child2)])
    population = new_population

# Select the best schedule from the final population
best_schedule = max(population, key=fitness)
print("Optimized Disk Scheduling Order:", best_schedule)

# Visualization
plt.figure(figsize=(10, 5))
plt.plot(best_schedule, range(len(best_schedule)), marker='o', linestyle='-', color='b', label='Optimized Path')
plt.scatter(requests, range(len(requests)), color='r', label='Requests', zorder=3)
plt.axhline(y=0, color='g', linestyle='--', label='Initial Head Position')
plt.xlabel("Cylinder Number")
plt.ylabel("Order of Execution")
plt.title("Genetic Algorithm Disk Scheduling Visualization")
plt.legend()
plt.grid()
plt.show()
