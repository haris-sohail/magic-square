import random as rand
import copy

def getRandomNumber(done, order):
    numberToStore = rand.randint(1, order * order)
    while(numberToStore in done):
        numberToStore = rand.randint(1, order * order)

    return numberToStore

def showPuzzle(puzzle):
    n = len(puzzle)
    m = len(puzzle[0])

    # Print the puzzle
    print('\n')
    for row in puzzle:
        print(" | ".join(map(str, row)))

    # Calculate and print the sum of each row
    for i, row in enumerate(puzzle):
        row_sum = sum(row)
        print(f"Sum of Row {i + 1}: {row_sum}")

    # Calculate and print the sum of each column
    for j in range(m):
        col_sum = sum(puzzle[i][j] for i in range(n))
        print(f"Sum of Column {j + 1}: {col_sum}")

    # Calculate and print the sum of the main diagonal
    main_diag_sum = sum(puzzle[i][i] for i in range(min(n, m)))
    print(f"Sum of Main Diagonal: {main_diag_sum}")

    # Calculate and print the sum of the reverse diagonal
    reverse_diag_sum = sum(puzzle[i][m - 1 - i] for i in range(min(n, m)))
    print(f"Sum of Reverse Diagonal: {reverse_diag_sum}")

    print('\n')
    
def find_element_position_2d(lst, element):
    for i, row in enumerate(lst):
        if element in row:
            j = row.index(element)
            return (i, j)
    return None

def setOrder(val):
    global order
    order = val

def generatePuzzle():
    if order % 2 == 0: # puzzle can not be of even order 
        return False
    
    done = []
    puzzle = []

    for i in range(order):
        puzzleRow = []
        for j in range(order):
            
            numberToStore = getRandomNumber(done, order)
            done.append(numberToStore)

            # store the number in the puzzle
            puzzleRow.append(numberToStore)

        puzzle.append(puzzleRow)

    # get a random element from the 2d list
    randSquare = rand.randint(1, (order * order))
    return puzzle, find_element_position_2d(puzzle, randSquare)

def getPopulations(puzzle, startPos):
    population = []
    toAppend = []

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):

            # swap the elements
            puzzle[i][j], puzzle[startPos[0]][startPos[1]] = puzzle[startPos[0]][startPos[1]], puzzle[i][j] 
            toAppend = copy.deepcopy(puzzle)
            population.append(toAppend)

            # swap again to default position
            puzzle[i][j], puzzle[startPos[0]][startPos[1]] = puzzle[startPos[0]][startPos[1]], puzzle[i][j]

    return population

def getDiagonals(list):
    n = len(list)
    main_diagonal = [list[i][i] for i in range(n)]
    reverse_diagonal = [list[i][n - 1 - i] for i in range(n)]
    return main_diagonal, reverse_diagonal

def getFitness(chromo):
    """
    The fitness is the summed distance of each element in a row, col and diagonal
    Therefore lower fitness values are better than higher ones 
    """

    goalSum = order * (((order * order) + 1) / 2)
    rowScore = 0
    colScore = 0
    diag1Score = 0
    diag2Score = 0

    # get the sum of each row, col and diagonal and compare with goal
    for row in chromo:
        rowScore += abs(sum(row) - goalSum)

    transposed_chromo = zip(*chromo)
    for col in transposed_chromo:
        colScore += abs(sum(col) - goalSum)

    diag1, diag2 = getDiagonals(chromo)

    diag1Score += abs(sum(diag1) - goalSum)
    diag2Score += abs(sum(diag2) - goalSum)

    return rowScore + colScore + diag1Score + diag2Score

def selection(pop, fitness):
    total = sum(fitness)
    r = rand.uniform(0, total)
    partial_sum = 0
    for i in range(len(pop)):
        partial_sum += fitness[i]
        if partial_sum > r:
            chromo1 = pop[i]
            break
    total = sum(fitness)
    r = rand.uniform(0, total)
    partial_sum = 0
    for i in range(len(pop)):
        partial_sum += fitness[i]
        if partial_sum > r:
            chromo2 = pop[i]
            break

    return chromo1, chromo2

def insertInOffspring(insertInd, toInsert, offSpring):
    if(offSpring[insertInd[0]][insertInd[1]]):
        # insert in any random position if not occupied
        insertX = rand.randint(0, order - 1)
        insertY = rand.randint(0, order - 1)

        while(offSpring[insertX][insertY] != None):
            insertX = rand.randint(0, order - 1)
            insertY = rand.randint(0, order - 1)

        offSpring[insertX][insertY] = toInsert


    else:
        offSpring[insertInd[0]][insertInd[1]] = toInsert

    return offSpring

def getEmptyList(n, m):
    empty_list = [[None] * m for _ in range(n)]
    return empty_list

def crossover(chromo1, chromo2):
    offspring1 = getEmptyList(order, order)
    offspring2 = getEmptyList(order, order)
    square = 1

    for i in range(len(chromo1)):
        for j in range(len(chromo1)):
            if(rand.random() < 0.5):
                # find the position of square in chromosome 1 
                insertInd = find_element_position_2d(chromo1, square)
            else:
                # find the position of square in chromosome 2
                insertInd = find_element_position_2d(chromo2, square)

            insertInOffspring(insertInd, square, offspring1)
            insertInOffspring(insertInd, square, offspring2)

            square += 1



    return offspring1, offspring2

def mutation(chromo):
    # pick two random indices from the chromosome and swap them
    randSquare1 = rand.randint(1, (order * order))
    randSquare2 = rand.randint(1, (order * order))

    randSquare1Ind = find_element_position_2d(chromo, randSquare1)
    randSquare2Ind = find_element_position_2d(chromo, randSquare2)

    # swap
    chromo[randSquare1Ind[0]][randSquare1Ind[1]], chromo[randSquare2Ind[0]][randSquare2Ind[1]] = \
    chromo[randSquare2Ind[0]][randSquare2Ind[1]], chromo[randSquare1Ind[0]][randSquare1Ind[1]]

    return chromo


def solvePuzzle(puzzle, startPos):
    # generate a population by swaping the square with all the empty squares one by one
    population = getPopulations(puzzle, startPos)
    i = None
    for i in range(1000): # run for n generations
        fitness = [getFitness(chromo) for chromo in population] # get fitness for all chromosomes

        chromo1, chromo2 = selection(population, fitness) # selection for crossover

        offspring1, offspring2 = crossover(chromo1, chromo2)

        # mutate both offsprings

        offspring1 = mutation(offspring1)

        offspring2 = mutation(offspring2)

        # replace the two worst chromosomes with the new offsprings

        worst_idx1 = fitness.index(max(fitness))

        population[worst_idx1] = offspring1

        fitness[worst_idx1] = getFitness(offspring1)

        worst_idx2 = fitness.index(max(fitness))

        population[worst_idx2] = offspring2

        fitness[worst_idx2] = getFitness(offspring2)

        # if fitness is 0 break the loop
        if(min(fitness) == 0):
            break
        

    # get the chromosome with the lowest fitness
    best_idx = fitness.index(min(fitness))
    showPuzzle(population[best_idx])
    print("Fitness: ", fitness[best_idx])
    print("Solution found after ", i, " generations")


