
#Muhammad Kashif
#I21-0851
#Section Y
#Artificial Intelligence Assignment 2


import numpy as np
import random
import time
import resource

# Define constants
POPULATION_SIZE = 10
MUTATION_RATE = 0.2
MAX_GENERATIONS = 1000

# Define the magic constant for a 3x3 magic square
MAGIC_CONSTANT = 15

def is_magic_square(square):
    """Check if the given square is a magic square."""
    sums = [np.sum(row) for row in square]  # Row sums
    sums += [np.sum(square[:, i]) for i in range(3)]  # Column sums
    sums.append(np.trace(square))  # Main diagonal sum
    sums.append(np.trace(np.fliplr(square)))  # Secondary diagonal sum
    return all(sum == MAGIC_CONSTANT for sum in sums)

def generate_individual():
    """Generate a random valid individual."""
    while True:
        individual = list(range(1, 10))  # Numbers 1 to 9
        random.shuffle(individual)
        individual = np.array(individual).reshape(3, 3)
        if is_magic_square(individual):
            return individual


def main():

    start_time = time.time()
    start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # Generate initial population
    population = [generate_individual() for _ in range(POPULATION_SIZE)]

    for generation in range(MAX_GENERATIONS):
        # Evaluate fitness
        fitness_scores = [fitness_function(individual) for individual in population]
        max_fitness = max(fitness_scores)
        best_individual = population[fitness_scores.index(max_fitness)]

        # Check if solution is found
        if max_fitness == 8:  # All rows, columns, and diagonals sum to MAGIC_CONSTANT
            print("Solution found in generation", generation)
            print("Magic Square:")
            print(best_individual)
            break

        # Evolve population
        population = evolve_population(population)

    else:
        print("No solution found within the maximum number of generations.")

    # Calculate time and memory usage
    end_time = time.time()
    end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    time_elapsed = end_time - start_time
    memory_used = (end_memory - start_memory) / 1024  # Convert to KB

    print("Time elapsed: {:.4f} seconds".format(time_elapsed))
    print("Memory used: {:.2f} KB".format(memory_used))

if __name__ == "__main__":
    main()