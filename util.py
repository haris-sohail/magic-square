import random as rand
import copy

def getRandomNumber(done, order):
    numberToStore = rand.randint(1, order * order)
    while(numberToStore in done):
        numberToStore = rand.randint(1, order * order)

    return numberToStore

def showPuzzle(puzzle):
    print('\n')
    for row in puzzle:
        print(" | ".join(map(str, row)))

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

def solvePuzzle(puzzle, startPos):
    # generate a population by swaping the square with all the empty squares one by one
    population = getPopulations(puzzle, startPos)

    for i in range(100): # run for 100 generations
        fitness = [getFitness(chromo) for chromo in population] # get fitness for all chromosomes

        chromo1, chromo2 = selection(population, fitness)
