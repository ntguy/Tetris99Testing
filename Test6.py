from numpy import *

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
    # (height, width) of currentBoard 2D array
    dimensions = currentBoard.shape
    # will hold heightList, will be returned
    heightList = []
    # for each column of board
    for i in range(0, dimensions[1]):
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

if __name__ == '__main__':
    main()


#to-do
#for all column positions (top of board) of the tetromino, calculate the minimum distance between heightList of tetromino and board
# 0 1
# 1 1
# 1 0
# 0 0
# 1 0
# 1 1

# 1 3 RESULT: 1 and 3, piece can be lowered 1
#generate test board for each move possibility, with tetromino dropped
#the hard part lol, evaluate which test board state is the best.
#how many moves left or right is that state? Switch would then be given input such as left, left, left, drop. 

