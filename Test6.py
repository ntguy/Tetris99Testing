from numpy import *
from copy import copy, deepcopy

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
    [1, 1], 
    [1, 1]
  ],
  [
    [1, 1, 1],
    [0, 1, 0]
  ]
])

constBoardWidth = 10
constBoardHeight = 20



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
def CBHeight(currentBoard):
    # will hold heightList, will be returned
    heightList = []
    # for each column of board
    for i in range(0, constBoardWidth):
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

#returns a list of how many spaces down the current tetromino can move before it makes contact with a piece on the board (collision). Indexed to go from leftmost to rightmost side. Since some tetrominos are wider than others, the list can have a variable length. First element will always represent the furthest left the tetromino can be, last element the furthest right. 
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
    print (CTHeightList)
    CBHeightList = CBHeight(currentBoard)
    print (CBHeightList)
    heightDiffList = minHeightDiff(currentTetromino, CTHeightList, CBHeightList)
    print(heightDiffList)
    possibleBoards = generatePossibleBoards(currentTetromino, currentBoard, heightDiffList)
    print(possibleBoards)

if __name__ == '__main__':
    main()



#to-do
#generate test board for each move possibility, with tetromino dropped
#the hard part lol, evaluate which test board state is the best.
#how many moves left or right is that state? Switch would then be given input such as left, left, left, drop. 