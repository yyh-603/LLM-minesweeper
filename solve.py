from game import Game
import copy

class Solver:
    def solveEasy(_game: Game):
        game = copy.deepcopy(_game)
        determinedMine = set()
        while True:
            opened = set()
            for i in range(game.getHeight()):
                for j in range(game.getWidth()):
                    if game.getCellIsOpen(i, j):
                        opened.add((i, j))
            valid = False
            for cord in opened:
                adj = game.getAdjacent(cord[0], cord[1])
                notOpened = set()
                adjMineCount = 0

                for adjCord in adj:
                    if not game.getCellIsOpen(adjCord[0], adjCord[1]):
                        notOpened.add(adjCord)
                        if adjCord in determinedMine:
                            adjMineCount += 1
                
                
                if len(notOpened) == game.getCellData(cord[0], cord[1]):
                    for adjCord in notOpened:
                        determinedMine.add(adjCord)
                        if not game.getCellHasFlag(adjCord[0], adjCord[1]):
                            game.setFlag(adjCord[0], adjCord[1])
                            valid = True
                
                if adjMineCount == game.getCellData(cord[0], cord[1]):
                    for adjCord in notOpened:
                        if adjCord not in determinedMine:
                            game.openCell(adjCord[0], adjCord[1])
                            valid = True
                

            if not valid:
                break
            
            if game.checkWin():
                break
                
        return game.checkWin()

    def solveHard(game):
        pass

if __name__ == "__main__":
    winCount = 0

    for _ in range(100):
        game = Game(9, 9, 10)
        found0 = False
        for i in range(9):
            for j in range(9):
                if game.getCellData(i, j) == 0:
                    game.openCell(i, j)
                    found0 = True
                    break
            if found0:
                break
        winCount += Solver.solveEasy(game)

    print(winCount)
            