from game import Game
from game import GameState
import random
from pathlib import Path
import copy
import os
import argparse
def get_argument():
    opt = argparse.ArgumentParser()
    opt.add_argument('--height',
                        type=int,
                        required=False,
                        help='height of the game',
                        default=9)
    opt.add_argument('--width',
                        type=int,
                        required=False,
                        help='width of the game',
                        default=9)
    opt.add_argument('--mines_num',
                        type=int,
                        required=False,
                        help='number of mines',
                        default=10)
    opt.add_argument('--random_select_num',
                        type=int,
                        required=False,
                        help='number of random select',
                        default=5)
    opt.add_argument('--case_count',
                        type=int,
                        required=False,
                        help='number of test cases',
                        default=5
                        )
    opt.add_argument('--dir_path',
                        type=str,
                        required=False,
                        help='directory path',
                        default='partial_unittest_data')
    opt.add_argument("--fixed_seed",
                        type=bool,
                        required=False,
                        help="fixed seed",
                        default=False)

    config = vars(opt.parse_args())
    return config

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
                if i == 0 and game.getCellData(x, y) == 0:
                    foundNotOpen = True
                if i != 0:
                    foundNotOpen = True

        
        nextGameState = copy.deepcopy(game)
        nextGameState.openCell(x, y)
        if nextGameState.gameState != GameState.PLAYING:
            break
        
        game.openCell(x, y)
    
    return game


if __name__ == '__main__':
    
    config = get_argument()

    if config['fixed_seed']:
        random.seed(114514)
    
    dir_path = Path(config['dir_path'])
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    height = config['height']
    width = config['width']
    minesNum = config['mines_num']
    randomSelectNum = config['random_select_num']
    caseCount = config['case_count']

    for stepNum in range(1, randomSelectNum + 1):
        for i in range(caseCount):
            path = Path.joinpath(dir_path, f'{height}_{width}_{minesNum}_{stepNum}_{i}.txt')

            game = generateImcompleteMap(height, width, minesNum, stepNum)

            grid = game.gridFormat()
            answer = game.getAllData()
            
            file = open(path, 'w')
            file.write(grid)
            for row in answer:
                file.write(' '.join([str(x) for x in row]) + '\n')
            file.close()