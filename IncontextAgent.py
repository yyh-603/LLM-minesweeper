from game import Game
from agent import Agent
from IncontextPrompt import IncontextPrompt
from actionFeedback import ActionFeedback
import re

class IncontextAgent(Agent):

    def _process_response(self, response: str):
        pattern =  r"REASON: (?P<reason>.*)\nACTION: (?P<action>open|flag) (?P<x>\d+) (?P<y>\d+)"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            ret = {
                "response": response,
                "reason": match.group("reason"),
                "action": match.group("action"),
                "x": int(match.group("x")),
                "y": int(match.group("y"))
            }
            return True, ret
        else:
            return False, {"response": response}

    def getAction(self, game: Game, falied_reason: ActionFeedback = ActionFeedback.SUCCESS):
        promptgen = IncontextPrompt()
        prompt = ""
        prompt += promptgen.intro_game()
        prompt += promptgen.intro_cell_state()
        prompt += promptgen.intro_actions()
        prompt += promptgen.action_format()
        prompt += promptgen.regulation()
        prompt += promptgen.example_1()
        prompt += promptgen.example_2()
        prompt += promptgen.example_3()
        prompt += promptgen.response_guide(game, falied_reason)
        response = self.api.sendMessage(promptgen.system_message(), prompt)

        valid, response = self._process_response(response)
        if not valid:
            return False, None, None, response['response']
        else:
            return True, response["action"], (response["x"], response["y"]), response['response']
