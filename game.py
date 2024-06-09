import random
from enum import Enum
from actionFeedback import ActionFeedback

class Cell:
    def __init__(self, data, isOpen = False, hasFlag = False):
        '''
        - data: number in the cell, -1 if the cell is a mine
        - isOpen: a boolean indicating whether the cell is open or not
        - hasFlag: a boolean indicating whether the cell has a flag or not
        '''
        self.data = data
        self.isOpen = isOpen
        self.hasFlag = hasFlag
    
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
    def __init__(self, height = -1, width = -1, minesNum = -1, filename = None):
        self.gameState = GameState.PLAYING
        if filename is not None:
            self.loadMap(filename)
        elif height == -1 or width == -1 or minesNum == -1:
            raise ValueError('Either the filename or the height, width, and minesNum should be provided.')
        else:
            self.width = width
            self.height = height
            self.map = []
            self.minesNum = minesNum
            self.generateMap()

    def loadMap(self, filename):
        '''
        Load the map from a file
        - filename: the name of the file
        '''
        self.map = []
        self.minesNum = 0
        with open(filename, "r") as file:
            lines = file.readlines()
            self.height, self.width = len(lines) // 2, len(lines[0].split())
            for i in range(len(lines)):
                lines[i] = lines[i].split()
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    cell = Cell(lines[i + self.height][j], isOpen = lines[i][j] != '.', hasFlag = lines[i][j] == 'F')
                    if cell.data == -1:
                        self.minesNum += 1
                    row.append(cell)
                self.map.append(row)
                

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
        if self.isValidOpenCell(x, y) != ActionFeedback.SUCCESS:
            return self.isValidOpenCell(x, y)
        
        self.map[x][y].open()
        if self.map[x][y].data == 0:
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if 0 <= x + k < self.height and 0 <= y + j < self.width and not self.map[x + k][y + j].isOpen and not self.map[x + k][y + j].hasFlag:
                        self.openCell(x + k, y + j)
        return ActionFeedback.SUCCESS
    
    def isValidOpenCell(self, x, y):
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
        if self.isValidSetFlag(x, y) != ActionFeedback.SUCCESS:
            return self.isValidSetFlag(x, y)
        if self.map[x][y].hasFlag:
            self.map[x][y].removeFlag()
        else:
            self.map[x][y].setFlag()
        return ActionFeedback.SUCCESS

    def isValidSetFlag(self, x, y):
        if not self.validPos(x, y):
            return ActionFeedback.INVALID_CELL
        if self.gameState != GameState.PLAYING:
            return ActionFeedback.GAME_HAS_ENDED
        if self.map[x][y].isOpen:
            return ActionFeedback.FLAG_NUMBER_CELL
        return ActionFeedback.SUCCESS

    def getCellData(self, x, y):
        '''
        Get the data of the cell
        - x: x coordinate of the cell
        - y: y coordinate of the cell
        '''
        return self.map[x][y].data
    
    def getAllData(self):
        '''
        Get the data of all cells
        '''
        return [[self.map[i][j].data for j in range(self.width)] for i in range(self.height)]

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
    mp = Game(filename='incompleteMap\\8_10_10_5_3.txt')
    print(mp.gridFormat())
    data = mp.getAllData()
    for i in range(len(data)):
        for j in range(len(data[i])):
            print(data[i][j], end=(' ' if j != len(data[i]) - 1 else '\n'))