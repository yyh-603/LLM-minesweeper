from game import Game
from agent import Agent
from FineTunedPrompt import FineTunedPrompt
from actionFeedback import ActionFeedback
import re 

class FineTunedAgent(Agent):

    def _process_response(self, response: str):
        pattern =  r"(?P<action>open|flag) (?P<x>\d+) (?P<y>\d+)"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            ret = {
                "action": match.group("action"),
                "x": int(match.group("x")),
                "y": int(match.group("y"))
            }
            return True, ret
        else:
            return False, None
    
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
            return False, None, None
        else:
            return True, response["action"], (response["x"], response["y"])