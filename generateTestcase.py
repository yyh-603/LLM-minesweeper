from game import Game
from game import GameState
import random
from pathlib import Path
import copy
import os

def generateImcompleteMap(height: int, width: int, minesNum: int, randomSelectNum: int = 5):
    game = Game(height = height, width = width, minesNum = minesNum)
    
    for i in range(randomSelectNum):
        
        foundNotOpen = False
        x = 0
        y = 0
        
        while not foundNotOpen:
            x = random.randint(0, height - 1)
            y = random.randint(0, width - 1)
            if (not game.getCellIsOpen(x, y)) and (game.getCellData(x, y) != -1):
                foundNotOpen = True
        
        nextGameState = copy.deepcopy(game)
        nextGameState.openCell(x, y)
        if nextGameState.gameState != GameState.PLAYING:
            break
        
        game.openCell(x, y)
    
    return game.gridFormat()


if __name__ == '__main__':
    
    dir_path = Path('.\\incompleteMap')
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    height = 8
    width = 10
    minesNum = 10
    
    for stepNum in range(1, 6):
        for i in range(10):
            path = Path.joinpath(dir_path, f'{height}_{width}_{minesNum}_{stepNum}_{i}.txt')
            
            file = open(path, 'w')
            file.write(generateImcompleteMap(height, width, minesNum, stepNum))
            file.close()