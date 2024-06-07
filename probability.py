from game import Game
import random

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
        self.game: Game = game
        self.width = self.game.getWidth()
        self.height = self.game.getHeight()
        self.current_mine_data = []
        self.need_check_cell = []
        self.no_touch_cell = []
        self.prob = []
        self.current_have_mine = []
        self.total_state_num = 0
        self.cnt_not_open = 0
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
            raise NotImplementedError()
        for x in range(self.height):
            for y in range(self.width):
                self.prob[x][y] = (1 - self.prob[x][y] / self.total_state_num)
    
    
    def getSingleProb(self, x, y):
        if x < 0 or x >= self.height or y < 0 or y >= self.width :
            raise ValueError('x or y is out of range')
        return self.prob[x][y]
    
    
    def getAllProb(self):
        return self.prob
    
    
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
            
            
            
            self.total_state_num += 1
            for i in range(len(self.need_check_cell)):
                if self.current_have_mine[i]:
                    x, y = self.need_check_cell[i]
                    self.prob[x][y] += 1

            for x, y in self.no_touch_cell:
                self.prob[x][y] += left_mines / no_touch_size
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
         

if __name__ == '__main__':
    width = 8
    height = 10
    mine_num = 9
    
    game = Game(width, height, mine_num)
    game.generateMap()
    for _ in range(5):
        x = random.randrange(0, width)
        y = random.randrange(0, height)
        if game.getCellData(x, y) == -1 or game.getCellIsOpen(x, y):
            continue
        game.openCell(x, y)
    
    game.printMap()
    
    probabilityCalculator = ProbabilityCalculator(game)
    probabilityCalculator.run()
    
    prob = probabilityCalculator.getAllProb()
    
    for x in range(width):
        for y in range(height):
            print(prob[x][y], end=' ')
        print()
    