from game import Game
from actionFeedback import ActionFeedback
from probability import ProbabilityCalculator
import math

class AnalysisGame(Game):
    def __init__(self, height: int, width: int, minesNum: int):
        super().__init__(height=height, width=width, minesNum=minesNum)
        self.valid_open_count = 0
        self.total_open_count = 0
        self.format_error_count = 0
        self.total_action_count = 0
        self.logic_error_count = 0
        self.probability_ln_sum = 0

    def openCell(self, x, y):
        '''
        Open a cell
        - x: x coordinate of the cell
        - y: y coordinate of the cell
        '''
        self.total_open_count += 1
        action_feedback = self.isValidOpenCell(x, y)
        if action_feedback != ActionFeedback.SUCCESS:
            self.logic_error_count += 1
            return action_feedback
        
        self.valid_open_count += 1
        probabilityCalculator = ProbabilityCalculator(self)
        prob = probabilityCalculator.getSingleProb(x, y)
        self.probability_ln_sum += math.log(prob)
        
        super().openCell(x, y)
        return action_feedback

    def setFlag(self, x, y):
        action_feedback = self.isValidSetFlag(x, y)
        if action_feedback != ActionFeedback.SUCCESS:
            self.logic_error_count += 1
            return action_feedback
        super().setFlag(x, y)
        return action_feedback
    
    def getTotalOpenNum(self):
        return self.total_open_count
    
    def getValidOpenNum(self):
        return self.valid_open_count
    
    def getValidRate(self):
        return self.valid_open_count / self.total_open_count
    
    def getAverageProbability(self):
        return math.exp(self.probability_ln_sum / self.valid_open_count)
    

if __name__ == '__main__':
    game = AnalysisGame(8, 10, 10)
    print(game.openCell(5, 5))
    print(game.openCell(5, 5))
    print(game.setFlag(7, 7))
    print(game.openCell(7, 7))
    print(game.setFlag(7, 7))
    print(game.openCell(7, 7))
    print(game.openCell(15, 15))
    print(game.logic_error_count) # should be 3
    