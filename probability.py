from game import Game
import math
import random
import copy

'''
return the survival probability

Initialize the Calculator and send the game state in:
    probabilityCalculator = ProbabilityCalculator(game)

Calculate survival probability:
    probabilityCalculator.run()
    
Get one cell's survival probability:
    probabilityCalculator.getSingleProb(x, y)

Get all cells' survival probability:
    probabilityCalculator.getAllProb()




'''
class ProbabilityCalculator:
    def __init__(self, game):
        self.game: Game = copy.deepcopy(game)
        self.width = self.game.getWidth()
        self.height = self.game.getHeight()
        self.mine_num = self.game.getMinesNum()
        self.current_mine_data = []
        self.need_check_cell = []
        self.no_touch_cell = []
        self.prob = []
        self.current_have_mine = []
        self.total_state_num = 0
        self.cnt_not_open = 0
        
        self.num_of_cell = self.width * self.height
        self.combination = [[0 for _ in range(self.mine_num + 1)] for _ in range(self.num_of_cell + 1)]
        
        for i in range(self.num_of_cell + 1):
            self.combination[i][0] = 1
            for j in range(1, self.mine_num + 1):
                self.combination[i][j] = self.combination[i - 1][j] + self.combination[i - 1][j - 1]
        
        self.run()
    
    def run(self):
        self.cnt_not_open = 0
        self.prob = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.current_mine_data = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.height):
            for y in range(self.width):
                if not self.game.getCellIsOpen(x, y):
                    self.cnt_not_open += 1
                    have_open_cell = False #check whether any opened cell nearby
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if x + i >= 0 and x + i < self.height and y + j >= 0 and y + j < self.width and self.game.getCellIsOpen(x + i, y + j):
                                have_open_cell = True
                                break
                    
                    if have_open_cell:
                        self.need_check_cell.append((x, y))
                    else:
                        self.no_touch_cell.append((x, y))
        
        
        self.have_mine_count = [0 for _ in range(len(self.need_check_cell))]
        self.total_state_num = 0
        self.current_have_mine = [False for _ in range(len(self.need_check_cell))]
        
        self._recur_count(self.game.getMinesNum())
        
        
        if self.total_state_num == 0:
            raise ValueError(f'There are no any possible solution.\n{self.game.gridFormat()}')
        else:
            for x in range(self.height):
                for y in range(self.width):
                    self.prob[x][y] = (1 - self.prob[x][y] / self.total_state_num)
    
    
    def getSingleProb(self, x, y):
        if x < 0 or x >= self.height or y < 0 or y >= self.width :
            raise ValueError('x or y is out of range')
        return self.prob[x][y]
    
    
    def getAllProb(self):
        return self.prob
    
    def getMaxProb(self):
        maxProb = 0
        for x in range(self.height):
            for y in range(self.width):
                if not self.game.getCellIsOpen(x, y):
                    maxProb = max(maxProb, self.prob[x][y])
        return maxProb

    def getMinProb(self):
        minProb = 1
        for x in range(self.height):
            for y in range(self.width):
                if not self.game.getCellIsOpen(x, y):
                    minProb = min(minProb, self.prob[x][y])
        return minProb
    
    def getMinProbPos(self):
        minProb = 1
        min_X = -1
        min_Y = -1
        for x in range(self.height):
            for y in range(self.width):
                if not self.game.getCellIsOpen(x, y):
                    if self.prob[x][y] < minProb:
                        minProb = self.prob[x][y]
                        min_X = x
                        min_Y = y
        
        return (min_X, min_Y)
    
    def getMaxProbPos(self):
        maxProb = -1
        max_X = -1
        max_Y = -1
        for x in range(self.height):
            for y in range(self.width):
                if not self.game.getCellIsOpen(x, y):
                    if self.prob[x][y] > maxProb:
                        maxProb = self.prob[x][y]
                        max_X = x
                        max_Y = y
        
        return (max_X, max_Y)
    
    def getMinProb(self):
        minProb = 2
        for x in range(self.height):
            for y in range(self.width):
                if not self.game.getCellIsOpen(x, y):
                    minProb = min(minProb, self.prob[x][y])
        return minProb
    
    def getMinProbPos(self):
        minProb = 2
        min_X = -1
        min_Y = -1
        for x in range(self.height):
            for y in range(self.width):
                if not self.game.getCellIsOpen(x, y):
                    if self.prob[x][y] < minProb:
                        minProb = self.prob[x][y]
                        min_X = x
                        min_Y = y
        
        return (min_X, min_Y)
    
    
    def _recur_count(self, mines_num, idx = 0):
        if idx == len(self.need_check_cell):
            
            left_mines = mines_num
            no_touch_size = len(self.no_touch_cell)
            if left_mines > no_touch_size:
                return
            
            for x in range(self.height):
                for y in range(self.width):
                    if self.game.getCellIsOpen(x, y) and self.game.getCellData(x, y) != self.current_mine_data[x][y]:
                        return
            
            
            self.total_state_num += self.combination[no_touch_size][left_mines]
            
            for i in range(len(self.need_check_cell)):
                if self.current_have_mine[i]:
                    x, y = self.need_check_cell[i]
                    self.prob[x][y] += self.combination[no_touch_size][left_mines]

            for x, y in self.no_touch_cell:
                self.prob[x][y] += left_mines / no_touch_size * self.combination[no_touch_size][left_mines]
            return
        #####
        
        can_put_mine = True
        if mines_num == 0:
            can_put_mine = False
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.need_check_cell[idx][0] + i
                y = self.need_check_cell[idx][1] + j
                if self._inRange(x, y) and self.game.getCellIsOpen(x, y):
                    real_mine_cnt = self.game.getCellData(x, y)
                    if self.current_mine_data[x][y] == real_mine_cnt:
                        can_put_mine = False
                        break
        
        
        if can_put_mine:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = self.need_check_cell[idx][0] + i
                    y = self.need_check_cell[idx][1] + j
                    if self._inRange(x, y):
                        self.current_mine_data[x][y] += 1
            
            self.current_have_mine[idx] = True
            self._recur_count(mines_num - 1, idx + 1)
            
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = self.need_check_cell[idx][0] + i
                    y = self.need_check_cell[idx][1] + j
                    if self._inRange(x, y):
                        self.current_mine_data[x][y] -= 1
        
        self.current_have_mine[idx] = False
        self._recur_count(mines_num, idx + 1)
    
    def _inRange(self, x, y):
        return (x >= 0 and x < self.height and y >= 0 and y < self.width)
         

# if __name__ == '__main__':
#     width = 8
#     height = 10
#     mine_num = 9
    
#     game = Game(width, height, mine_num)
#     game.generateMap()
#     for _ in range(1):
#         canOpenCell = []
#         for x in range(game.height):
#             for y in range(game.width):
#                 if (not game.getCellIsOpen(x, y)) and game.getCellData(x, y) != -1:
#                     canOpenCell.append((x, y))
                    
#         if len(canOpenCell) == 0:
#             break
#         randID = random.randrange(0,len(canOpenCell))
#         game.openCell(canOpenCell[randID][0], canOpenCell[randID][1])
    
#     game.printMap()
    
#     probabilityCalculator = ProbabilityCalculator(game)
    
#     prob = probabilityCalculator.getAllProb()
    
#     for x in range(width):
#         for y in range(height):
#             print(prob[x][y], end=' ')
#         print()
    
#     print(probabilityCalculator.getMaxProb())
#     print(probabilityCalculator.getMaxProbPos())

if __name__ == '__main__':
    game = Game(filename='testcase/5_5_4_1_91.txt')
    prob = ProbabilityCalculator(game)
    print(prob.getAllProb())
    print(prob.getMaxProb())
    print(prob.getMinProb())