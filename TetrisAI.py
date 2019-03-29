from numpy import *
from copy import copy, deepcopy

#game data

#currentBoard and tetrominoQueue will be the two variables that need to be refreshed after each move, getting data from the capture card. 
#in order to account for delay in the capture card, we may need to run multiple moves in this program effectively blind 
#play the currentTetromino, and the next couple in the queue, before refreshing the queue). Proper integration for fast play will take some time
currentBoard = array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1]
])

# 3D array (array of 2D array tetrominos, the upcoming tetrominos on the right of the game board)
tetrominoQueue = array([
  [
    [0, 1], 
    [1, 1], 
    [1, 0]
  ], 
  [
    [1, 1], 
    [1, 1]
  ], 
  [
    [1, 1, 1, 1]
  ], 
  [
    [0, 1], 
    [1, 1], 
    [1, 0]
  ], 
  [
    [1, 1, 1],
    [0, 1, 0]
  ]
])





#Height analysis functions (for tetromino's, boards, and determining collisions)

# takes in the current Tetromino and returns a height map (how far down does each column of the piece extend)
# examples:
# [1,1,1,1] returns [1,1,1,1]
# [1,1,1],
# [0,1,0] returns [1,2,1]
# [1,1],
# [1,1] returns [2,2]
# [0,1],
# [1,1],
# [1,0] returns [3,2]
def CTHeight(currentTetromino):
    # (height, width) of currentTetromino 2D array
    dimensions = currentTetromino.shape
    # will hold heightList, will be returned
    heightList = []
    # for each column of tetromino
    for i in range(0, dimensions[1]):
        # columnHeight initialized to 0
        columnHeight = 0
        # iterate down through each row of current column
        for j in range(0, dimensions[0]):
            # if the current space contains a block (is a 1, not a 0),
            # columnHeight is set to j+1 (+1 is to account for 0 indexing of arrays)
            if currentTetromino[j][i] == 1:
                columnHeight = j + 1
        # append the columnHeight to the heightList
        heightList.append(columnHeight)
    return heightList

#takes in the currentBoard and returns a heightmap (highest block for each column)
#example: currentBoard is 
#...
#    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
#    [1, 1, 0, 0, 1, 1, 1, 0, 0, 1],
#    [1, 1, 1, 1, 0, 1, 1, 0, 0, 1],
#    [1, 1, 0, 1, 1, 1, 1, 1, 0, 1]

#    [3, 3, 2, 2, 3, 4, 3, 1, 0, 4] will be the return value
def boardHeight(currentBoard):
    # will hold heightList, will be returned
    heightList = []
    # for each column of board
    for i in range(10):
        # columnHeight initialized to 0
        columnHeight = 0
        # iterate up through each row of current column, until the top (0)
        for j in range(19, -1, -1):
            # if the current space contains a block (is a 1, not a 0),
            # columnHeight is set to 20 - j
            if currentBoard[j][i] == 1:
                columnHeight = 20 - j 
        # append the columnHeight to the heightList
        heightList.append(columnHeight)
    return heightList

#returns a list of how many spaces down the current tetromino can move before it makes contact with a piece on the board (collision). 
#Indexed to go from leftmost to rightmost side. Since some tetrominos are wider than others, the list can have a variable length:
#up to 10 if the tetromino is width 1 (a height difference for each column), as small as 7 if teromino is width 4
# First element will always represent the furthest left the tetromino can be, last element the furthest right. 
#example return: [15, 15, 16, 15, 14, 14, 15, 17, 14]
#takes in the currentTetromino and heightLists for it and the board
def minHeightDiff(currentTetromino, CTHeightList, CBHeightList):
    #list of minimum height differences, left to right, will be returned.
    heightDiffList = [] 
    #tetrominoDimensions[1] will be width of current tetromino
    tetrominoDimensions = currentTetromino.shape
    #start at left of board, go right until you hit the wall with the current tetromino, accounting for variable width
    for i in range(0, 10 - (tetrominoDimensions[1] - 1)):
        #height differences for each column of the tetromino
        heightDiffs = []
        #cycle through each column of the currentTetromino
        for j in range(0, len(CTHeightList)):
            #calculate the height difference between bottom of tetromino and highest piece of board FOR THIS COLUMN
            heightDiff = 20 - (CTHeightList[j] + CBHeightList[i+j])
            heightDiffs.append(heightDiff)
        #the minHeightDiff is how far the tetromino can be moved down before contacting a board piece. Append to the final heightDiffList
        minHeightDiff = min(heightDiffs)
        heightDiffList.append(minHeightDiff)
    return heightDiffList





#AI Stuff (Node/State Generation and Heuristic Analysis)

#will return a 3D array (2D array of all possible boards/moves with the current Tetromino). 
#assumes direct drops only
def generatePossibleBoards(currentTetromino, currentBoard, heightDiffList):
    #array will hold 2D array boards and be returned
    possibleBoards = []
    #height and width of currentTetromino
    dimensions = currentTetromino.shape
    #used to make the tetromino increment/travel rightwards, for each possible move
    count = 0 
    #for each minHeight (distance Tetromino must travel down before collision), create a possible board
    for minHeight in heightDiffList:
        #testBoard must be a COPY of the current board, not a reference to it
        testBoard = deepcopy(currentBoard)
        # for each column of tetromino
        for i in range(0, dimensions[1]):
            # iterate down through each row of current column
            for j in range(0, dimensions[0]):
                #adding the tetromino to the board. Coordinates use j and i, and BOARD coordinate is offset by minHeight (how far down to move piece) and count (how far right to move piece)
                testBoard[j + minHeight][i+count] += (currentTetromino[j][i])
        count += 1 #right one
        possibleBoards.append(testBoard) #append to final returned possibleBoards list
    return(possibleBoards)

#given a board state, computes number of complete lines
def computeCompleteLines(board):
    #number of complete lines initialized to 0
    completeLines = 0
    #for each row/line of the board, check if it is complete (all 1s)
    for row in range (20):
        #complete initialized to True, switched to False if 0 is in line
        complete = True
        #for each column in line
        for column in range(10):
            #if 0 is found, line isn't complete, break the loop
            if (board[row][column]) == 0:
                complete = False
                break
        #if the line is complete, increment completeLines
        if (complete):
            completeLines = completeLines + 1
    return (completeLines)

#computes and returns the number of holes in the board (0s with 1s somewhere above them)
def computeHoles(board, boardHeightList):
    #we need the indexes of the height coordinates, e.g., not 0 for the bottom, but 19
    heightIndexList = []
    for i in range (size(boardHeightList)):
        heightIndexList.append(20 - boardHeightList[i])

    #number of holes initialized to 0
    holes = 0
    #for each column of the board
    for column in range (10):
        #check each row, from the index of the highest 1 in the column down to the bottom of the board. If a 0 is found, it by definition has a 1 above it and is a hole
        for row in range(heightIndexList[column], 20):
            if (board[row][column] == 0):
                holes = holes + 1 #increment hole counter
    return holes

#computes and returns the variation between adjacent column heights (bumpiness, wells, etc). 
#a relatively flat grid is desirable as there is less risk to create holes
def computeBumpiness(boardHeightList):
    bumpinessTotal = 0
    #only for i in range 9 becuase last column is reached via i+1
    for i in range (9):
        #variation between columnHeight and the next
        variation = abs(boardHeightList[i] - boardHeightList[i+1])
        #add variation to the bumpinessTotal
        bumpinessTotal = bumpinessTotal + variation
    return(bumpinessTotal)

#returns the heuristic value of a board, taking into account:
#aggregate height, complete lines, holes, and bumpiness
def computeHeuristicVal(board):
    boardHeightList = boardHeight(board)

    #4 heuristics
    aggregateHeight = sum(boardHeightList)
    completeLines = computeCompleteLines(board)
    holes = computeHoles(board, boardHeightList)
    bumpiness = computeBumpiness(boardHeightList)

    #parameters/values to multiply each heuristic by, since the scales and level of importance are not equal
    ParamAggregateHeight = -0.5
    ParamCompleteLines = 0.75   #positive because this should be maximized, not minimized!
    ParamHoles = -0.33
    ParamBumpiness = -0.2
    
    #puts heuristic together into value to evaluate (higher is better)
    heuristicVal = ParamAggregateHeight * aggregateHeight + ParamCompleteLines * completeLines + ParamHoles * holes + ParamBumpiness * bumpiness

    print("A Test Board (NOT currentBoard; currentTetromino is placed)")
    print(board)
    print("Aggregate Height: ", aggregateHeight)
    print("Complete Lines: ", completeLines)
    print("Holes: ", holes)
    print("Bumpiness: ", bumpiness)
    print("Heuristic Value: ", heuristicVal, "\n")

    return heuristicVal





def main():
    #must be global so that it can be changed within main
    global tetrominoQueue
    # assign the current tetromino to be the tetromino at the top of the queue
    currentTetromino = tetrominoQueue[0]
    # delete the first/top tetromino from the queue (the currentTetromino)
    tetrominoQueue = delete(tetrominoQueue, 0)
    # has to be of type numpy array, not list
    currentTetromino = array(currentTetromino)
    # get heightList of tetromino
    CTHeightList = CTHeight(currentTetromino)
    print ("Current Tetromino Height List: ", CTHeightList)
    CBHeightList = boardHeight(currentBoard)
    print ("Current Board     Height List: ", CBHeightList)
    heightDiffList = minHeightDiff(currentTetromino, CTHeightList, CBHeightList)
    print("Height Difference (CB)   List: ", heightDiffList)
    possibleBoards = generatePossibleBoards(currentTetromino, currentBoard, heightDiffList)
    #print(possibleBoards)
    #will hold heuristic value for each possibleBoard
    heuristicValList = []
    for board in range(len(possibleBoards)):
        heuristicValList.append(computeHeuristicVal(possibleBoards[board]))
    print("Heuristic Value List: ", heuristicValList)
    #the bestMove is the board with the maximum heuristic
    bestMove = max(heuristicValList)
    #numpy.argmin gets the index of said maximum heuristic
    bestMoveIndex = argmin(heuristicValList)
    print("Best Move: ", bestMove, "Value, Index of", bestMoveIndex)

if __name__ == '__main__':
    main()





#to-do
#how many moves left or right is chosen best state? Switch would then be given input such as left, left, left, drop. 
#rotation block data, in seperate file that is included
#actually use next tetromino in queue in a looping manner
#switch, when generating currentBoard, should ignore the currentTetromino (ignore pieces at top of board that aren't in contact with another piece below them?)