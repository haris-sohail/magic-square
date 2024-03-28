from util import *




def __main__():
    setOrder(3)
    puzzle, startPos = generatePuzzle()

    if(puzzle):
        showPuzzle(puzzle)
        solvePuzzle(puzzle, startPos)

    else:
        print("Order not valid")

__main__()