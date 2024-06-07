import random
from enum import Enum
from actionFeedback import ActionFeedback

class Cell:
    def __init__(self, data):
        '''
        - data: number in the cell, -1 if the cell is a mine
        - isOpen: a boolean indicating whether the cell is open or not
        - hasFlag: a boolean indicating whether the cell has a flag or not
        '''
        self.data = data
        self.isOpen = False
        self.hasFlag = False
    
    def open(self):
        self.isOpen = True
    
    def setFlag(self):
        self.hasFlag = True
    
    def removeFlag(self):
        self.hasFlag = False
    
    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data
    
    def getIsOpen(self):
        return self.isOpen
    
    def getHasFlag(self):
        return self.hasFlag

class GameState(Enum):
    PLAYING = 0
    WIN = 1
    LOSE = 2

class Game:
    def __init__(self, height, width, minesNum):
        self.width = width
        self.height = height
        self.map = []
        self.minesNum = minesNum
        self.gameState = GameState.PLAYING
        self.generateMap()

    def generateMap(self):
        '''
        Generate the map with mines and numbers
        '''
        if self.minesNum > self.width * self.height:
            raise ValueError('The number of mines is greater than the number of cells.')
        # Initialize the map
        self.map = [[Cell(0) for i in range(self.width)] for j in range(self.height)]
        # Place the mines
        for i in range(self.minesNum):
            x = random.randint(0, self.height - 1)
            y = random.randint(0, self.width - 1)
            while self.map[x][y].data == -1:
                x = random.randint(0, self.height - 1)
                y = random.randint(0, self.width - 1)
            self.map[x][y].data = -1
            # Update the numbers around the mine
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if 0 <= x + k < self.height and 0 <= y + j < self.width and self.map[x + k][y + j].data != -1:
                        self.map[x + k][y + j].data += 1
    
    
    def openCell(self, x, y):
        '''
        Open a cell
        - x: x coordinate of the cell
        - y: y coordinate of the cell
        '''
        if self.isValidAction(x, y) != ActionFeedback.SUCCESS:
            return self.isValidAction(x, y)
        
        self.map[x][y].open()
        if self.map[x][y].data == 0:
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if 0 <= x + k < self.height and 0 <= y + j < self.width:
                        self.openCell(x + k, y + j)
        return ActionFeedback.SUCCESS
    
    def isValidAction(self, x, y):
        if not self.validPos(x, y):
            return ActionFeedback.INVALID_CELL
        if self.gameState != GameState.PLAYING:
            return ActionFeedback.GAME_HAS_ENDED
        if self.map[x][y].isOpen:
            return ActionFeedback.OPEN_NUMBER_CELL
        if self.map[x][y].hasFlag:
            return ActionFeedback.OPEN_FLAGGED_CELL
        return ActionFeedback.SUCCESS


    def setFlag(self, x, y):
        '''
        Set a flag on the cell
        - x: x coordinate of the cell
        - y: y coordinate of the cell
        '''
        if self.gameState != GameState.PLAYING:
            return False
        if self.map[x][y].isOpen:
            return False
        if self.map[x][y].hasFlag:
            return False
        self.map[x][y].setFlag()
        return True
    
    def removeFlag(self, x, y):
        '''
        Remove the flag on the cell
        - x: x coordinate of the cell
        - y: y coordinate of the cell
        '''
        if self.gameState != GameState.PLAYING:
            return False
        if self.map[x][y].isOpen:
            return False
        if not self.map[x][y].hasFlag:
            return False
        self.map[x][y].removeFlag()
        return True

    def getCellData(self, x, y):
        '''
        Get the data of the cell
        - x: x coordinate of the cell
        - y: y coordinate of the cell
        '''
        return self.map[x][y].data

    def getCellIsOpen(self, x, y):
        '''
        Get the isOpen of the cell
        - x: x coordinate of the cell
        - y: y coordinate of the cell
        '''
        try: 
            isOpen = self.map[x][y].isOpen
        except Exception as e:
            print(f'{x} {y}')
            print(e)
        return self.map[x][y].isOpen
    
    def getCellHasFlag(self, x, y):
        '''
        Get the hasFlag of the cell
        - x: x coordinate of the cell
        - y: y coordinate of the cell
        '''
        return self.map[x][y].hasFlag
    
    def getCellDatas(self):
        '''
        Get the data of all cells
        '''
        return [[self.map[i][j].data for j in range(self.width)] for i in range(self.height)]

    def getCellIsOpens(self):
        '''
        Get the isOpen of all cells
        '''
        return [[self.map[i][j].isOpen for j in range(self.width)] for i in range(self.height)]
    
    def getCellHasFlags(self):
        '''
        Get the hasFlag of all cells
        '''
        return [[self.map[i][j].hasFlag for j in range(self.width)] for i in range(self.height)]

    def getMap(self):
        '''
        Get the map
        '''
        return self.map

    def checkWin(self):
        '''
        Check if the player wins
        '''
        for i in range(self.height):
            for j in range(self.width):
                if not self.map[i][j].isOpen and self.map[i][j].data != -1:
                    return False
        self.gameState = GameState.WIN
        return True

    def checkLose(self):
        '''
        Check if the player loses
        '''
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j].isOpen and self.map[i][j].data == -1:
                    self.gameState = GameState.LOSE
                    return True
        return False

    def validPos(self, x, y):
        '''
        Check if the position is valid
        '''
        return 0 <= x and x < self.height and 0 <= y and y < self.width

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getMinesNum(self):
        return self.minesNum
    
    def getSize(self):
        return self.height, self.width

    def getAdjacent(self, x, y):
        if not self.validPos(x, y):
            raise ValueError('(x, y) is not a valid position.')
        ret = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.validPos(i, j) and (i, j) != (x, y):
                    ret.append((i, j))
        return ret

    def gridFormat(self):
        ret = ""
        for i in range(self.height):
            tmp = ""
            for j in range(self.width):
                if self.map[i][j].getIsOpen():
                    data = self.map[i][j].getData()
                    if data == -1:
                        tmp += '* '
                    else:
                        tmp += str(data) + ' '
                else:
                    if self.map[i][j].getHasFlag():
                        tmp += "F "
                    else:
                        tmp += '. '
            ret += tmp + '\n'
        return ret

    def indexFormat(self):
        ret = ""
        for i in range(self.height):
            for j in range(self.width):
                tmp = f"({i}, {j}): "
                if self.map[i][j].getIsOpen():
                    data = self.map[i][j].getData()
                    if data == -1:
                        tmp += '*'
                    else:
                        tmp += str(data)
                else:
                    if self.map[i][j].getHasFlag():
                        tmp += 'F'
                    else:
                        tmp += '.'
                ret += tmp + '\n'
        return ret

    def printMap(self):
        '''
        Print the map
        '''
        print(self.gridFormat())
    
    def printGameState(self):
        '''
        Print the game state
        '''
        if self.gameState == GameState.PLAYING:
            print('Playing')
        elif self.gameState == GameState.WIN:
            print('Win')
        elif self.gameState == GameState.LOSE:
            print('Lose')

if __name__ == '__main__':
    mp = Game(9, 9, 10)
    
    print(mp.openCell(5, 5))
    print(mp.gridFormat())