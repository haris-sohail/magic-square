
# magic-square

Magic square puzzle solved using Genetic Algorithm

## Puzzle structure 

1) `setOrder(val)` function is used to set the order of the puzzle. Note that only odd ordered puzzles are valid magic square puzzles. Order 3 puzzle is of the form:

```
|2 3 4|
|1 5 6|
|7 9 8|
```

2) `generatePuzzle()` generates a random puzzle of size `order * order`, and also gives the starting position for the puzzle, highlighted in the this puzzle: 

```
|2 3 4|
|1 [5] 6|
|7 9 8|
```

## Solving the puzzle

### Populations

`getPopulations(puzzle, startPos)` gives populations by swapping the start position element by every element in the puzzle, like so:

```
|5 3 4|
|1 2 6|   
|7 9 8|
```

```
|2 5 4|
|1 3 6|
|7 9 8|
```

```
|2 3 5|
|1 4 6|
|7 9 8|
```

```
...
```

### Fitness

`getFitness(chromo)` gives the fitness of a particular chromosome. It is the summation of distance of every element in a row, column and diagonal

### Selection

`selection(population, fitness)` for selecting individuals (chromosomes) from a population based on their fitness scores in a genetic algorithm.

1. It calculates the total fitness of the population.
2. It generates a random value `r` within the range of total fitness.
3. It iterates through the population, accumulating fitness scores until the accumulated score exceeds `r`. It selects the chromosome corresponding to this point.
4. It repeats the above steps to select a second chromosome.

### Crossover 

`crossover(chromo1, chromo2)` 

1. It initializes two empty offspring chromosomes (`offspring1` and `offspring2`) of the same size as the parent chromosomes.
2. It iterates over each element in the parent chromosomes.
3. For each element, it randomly selects one of the parent chromosomes with a probability of 0.5.
4. It finds the position of the current element in the selected parent chromosome.
5. It inserts the element into the corresponding position in both offspring chromosomes.
6. It increments the value of the element (`square`) to be inserted in the offspring chromosomes.
7. It repeats steps 3-6 for all elements in the parent chromosomes.
8. Finally, it returns the two offspring chromosomes resulting from the crossover operation.

### Mutation

`mutation(chromo)` picks two random indices from the chromosome and swap them






