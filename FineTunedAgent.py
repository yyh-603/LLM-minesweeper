from game import Game
from agent import Agent
from FineTunedPrompt import FineTunedPrompt
from actionFeedback import ActionFeedback
import re 
from probability import ProbabilityCalculator
import math

class FineTunedAgent(Agent):

    def _process_response(self, response: str):
        pattern =  r"(?P<action>open|flag) (?P<x>\d+) (?P<y>\d+)"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            ret = {
                "response": response,
                "action": match.group("action"),
                "x": int(match.group("x")),
                "y": int(match.group("y"))
            }
            return True, ret
        else:
            return False, {"response": response}
    
    def getAction(self, game: Game, falied_reason: ActionFeedback = ActionFeedback.SUCCESS):
        promptgen = FineTunedPrompt()
        prompt = ""
        prompt += promptgen.intro_game()
        prompt += promptgen.intro_cell_state()
        prompt += promptgen.intro_actions()
        prompt += promptgen.action_format()
        prompt += promptgen.regulation()
        prompt += promptgen.response_guide(game, falied_reason)
        response = self.api.sendMessage(promptgen.system_message(), prompt)

        valid, response = self._process_response(response)
        if not valid:
            return False, None, None, response["response"]
        else:
            return True, response["action"], (response["x"], response["y"]), response["response"]

if __name__ == "__main__":
    game = Game(filename='testcase/5_5_4_1_91.txt')
    agent = FineTunedAgent("ft:gpt-3.5-turbo-0125:yyh-603:test:9YdqsY2Z")
    # valid, action, pos, response = agent.getAction(game)
    valid, action, pos, response = True, "open", (0, 4), "open 0 4"
    valid_action_count = 0
    format_error_count = 0
    logic_error_count = 0
    not_zero_count = 0
    zero_count = 0
    probability_ln_sum = 0
    print(response)
    if not valid:
        format_error_count += 1
    x, y = pos
    print(action, x, y)

    if action == "open":
        prob = ProbabilityCalculator(game)
        feedback = game.openCell(x, y)
        if feedback == ActionFeedback.SUCCESS:
            valid_action_count += 1
            print(prob.getMaxProb())
            val = prob.getSingleProb(x, y) / prob.getMaxProb()
            
            if abs(val) <= 1e-6:
                zero_count += 1
            else:
                not_zero_count += 1
                probability_ln_sum += math.log(val)
        else:
            print("Logic error")
            logic_error_count += 1
    
    if action == "flag":
        prob = ProbabilityCalculator(game)
        feedback = game.setFlag(x, y)
        if feedback == ActionFeedback.SUCCESS:
            valid_action_count += 1
            val = (1 - prob.getSingleProb(x, y)) / (1 - prob.getMinProb())
            if abs(val) <= 1e-6:
                zero_count += 1
            else:
                not_zero_count += 1
                probability_ln_sum += math.log(val)
        else:
            logic_error_count += 1