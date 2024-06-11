import random

from game import Game

from FineTunedPrompt import FineTunedPrompt
from probability import ProbabilityCalculator
from actionFeedback import ActionFeedback
from generateTestcase import generateImcompleteMap

import jsonlines

import tqdm

# return one line of 
class FineTuneDataGenerator:
    def __init__(self):
        self.promptGen = FineTunedPrompt()
        
        
    def generateFineTuneData_open(self, height: int, width: int, minesNum: int, ResultOfAction: ActionFeedback, randomSelectNum: int):
        x = -1
        y = -1
        game = generateImcompleteMap(height, width, minesNum, randomSelectNum)
        found_valid_case = False
        weight = 0
        while not found_valid_case:
            if ResultOfAction == ActionFeedback.SUCCESS:
                probabilityCalculator = ProbabilityCalculator(game)
                x, y = probabilityCalculator.getMaxProbPos()
                if x != -1 and y != -1:
                    found_valid_case = True
                    weight = 1

            elif ResultOfAction == ActionFeedback.INVALID_CELL:
                x = random.randint(0, height - 1)
                y = random.randint(0, width - 1)
                type_of_invalid = random.randint(0, 2) # 0 : x out of range, 1: y out of range, 2 : x and y out of range
                if type_of_invalid == 0:
                    x = height + random.randint(0, 1)
                elif type_of_invalid == 1:
                    y = width + random.randint(0, 1)
                else:
                    x = height + random.randint(0, 1)
                    y = width + random.randint(0, 1)
                found_valid_case = True
            
            elif ResultOfAction == ActionFeedback.OPEN_NUMBER_CELL:
                number_cell = []
                for i in range(height):
                    for j in range(width):
                        if game.getCellIsOpen(i, j):
                            number_cell.append((i, j))
                
                if len(number_cell) != 0:
                    x, y = number_cell[random.randint(0, len(number_cell) - 1)]
                    found_valid_case = True
                
            elif ResultOfAction == ActionFeedback.OPEN_FLAGGED_CELL:
                not_open_cell = []
                for i in range(height):
                    for j in range(width):
                        if not game.getCellIsOpen(i, j):
                            not_open_cell.append((i, j))
                
                if len(not_open_cell) != 0:
                    x, y = not_open_cell[random.randint(0, len(not_open_cell) - 1)]
                    game.setFlag(x, y)
                    found_valid_case = True
            else:
                raise ValueError('the ResultOfAction is invalid')

            if not found_valid_case:
                game = generateImcompleteMap(height, width, minesNum, randomSelectNum)
        
        system_message = self.promptGen.system_message()
        
        user_message = ''
        user_message += self.promptGen.intro_game()
        user_message += self.promptGen.intro_cell_state()
        user_message += self.promptGen.intro_actions()
        user_message += self.promptGen.action_format()
        user_message += self.promptGen.regulation()
        
        assistant_message = f'open {x} {y}'
        
        returnObj = {"messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message + self.promptGen.response_guide(game, ActionFeedback.SUCCESS)}, 
            {"role": "assistant", "content": assistant_message, "weight": weight}
            ]}
        
        if ResultOfAction != ActionFeedback.SUCCESS:
            probabilityCalculator = ProbabilityCalculator(game)
            ans_x, ans_y = probabilityCalculator.getMaxProbPos()
            returnObj["messages"].append({"role": "user", "content": user_message + self.promptGen.response_guide(game, ResultOfAction)})
            returnObj["messages"].append({"role": "assistant", "content": f'open {ans_x} {ans_y}', "weight": 1})
        return returnObj

    def generateFineTuneData_flag(self, height: int, width: int, minesNum: int, ResultOfAction: ActionFeedback, randomSelectNum: int = 5):
        x = -1
        y = -1
        game = generateImcompleteMap(height, width, minesNum, randomSelectNum)
        found_valid_case = False
        weight = 0
        
        while not found_valid_case:
            if ResultOfAction == ActionFeedback.SUCCESS:
                probabilityCalculator = ProbabilityCalculator(game)
                x, y = probabilityCalculator.getMinProbPos()
                if x != -1 and y != -1 and abs(probabilityCalculator.getMinProb()) < 1e-6:
                    found_valid_case = True
                    weight = 1
                    
            elif ResultOfAction == ActionFeedback.INVALID_CELL:
                x = random.randint(0, height - 1)
                y = random.randint(0, width - 1)
                type_of_invalid = random.randint(0, 2) # 0 : x out of range, 1: y out of range, 2 : x and y out of range
                if type_of_invalid == 0:
                    x = height + random.randint(0, 1)
                elif type_of_invalid == 1:
                    y = width + random.randint(0, 1)
                else:
                    x = height + random.randint(0, 1)
                    y = width + random.randint(0, 1)
                found_valid_case = True
            
            elif ResultOfAction == ActionFeedback.FLAG_NUMBER_CELL:
                number_cell = []
                for i in range(height):
                    for j in range(width):
                        if game.getCellIsOpen(i, j):
                            number_cell.append((i, j))
                
                if len(number_cell) != 0:
                    x, y = number_cell[random.randint(0, len(number_cell) - 1)]
                    found_valid_case = True
            else:
                raise ValueError('the ResultOfAction is invalid')
            
            if not found_valid_case:
                game = generateImcompleteMap(height, width, minesNum, randomSelectNum)
        
        system_message = self.promptGen.system_message()
        
        user_message = ''
        user_message += self.promptGen.intro_game()
        user_message += self.promptGen.intro_cell_state()
        user_message += self.promptGen.intro_actions()
        user_message += self.promptGen.action_format()
        user_message += self.promptGen.regulation()
        user_message += self.promptGen.response_guide(game, ResultOfAction)
        
        assistant_message = f'flag {x} {y}'
        
        returnObj = {"messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message + self.promptGen.response_guide(game, ActionFeedback.SUCCESS)}, 
            {"role": "assistant", "content": assistant_message, "weight": weight}
            ]}
        if ResultOfAction != ActionFeedback.SUCCESS:
            probabilityCalculator = ProbabilityCalculator(game)
            ans_x, ans_y = probabilityCalculator.getMinProbPos()
            returnObj["messages"].append({"role": "user", "content": user_message + self.promptGen.response_guide(game, ResultOfAction)})
            returnObj["messages"].append({"role": "assistant", "content": f'open {ans_x} {ans_y}', "weight": 1})
        
        return returnObj

if __name__ == '__main__':
    fineTuneDataGenerator = FineTuneDataGenerator()
    
    with jsonlines.open('FineTuneData50.jsonl', 'w') as writer:
        for i in tqdm.tqdm(range(30)):
            writer.write(fineTuneDataGenerator.generateFineTuneData_open(5, 5, 4, ActionFeedback.SUCCESS, 1))
        
        for i in range(10):
            writer.write(fineTuneDataGenerator.generateFineTuneData_flag(5, 5, 4, ActionFeedback.SUCCESS, 1))
        
        for i in range(2):
            writer.write(fineTuneDataGenerator.generateFineTuneData_open(5, 5, 4, ActionFeedback.INVALID_CELL, 1))
            writer.write(fineTuneDataGenerator.generateFineTuneData_open(5, 5, 4, ActionFeedback.OPEN_FLAGGED_CELL, 1))
            writer.write(fineTuneDataGenerator.generateFineTuneData_open(5, 5, 4, ActionFeedback.OPEN_NUMBER_CELL, 1))
            writer.write(fineTuneDataGenerator.generateFineTuneData_flag(5, 5, 4, ActionFeedback.FLAG_NUMBER_CELL, 1))
            writer.write(fineTuneDataGenerator.generateFineTuneData_flag(5, 5, 4, ActionFeedback.INVALID_CELL, 1))