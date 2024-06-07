from game import Game
from openaiAPI import OpenAIAPI
from agent import Agent
from CoTPrompt import CoTPrompt
from actionFeedback import ActionFeedback
import re

class CoTAgent(Agent):

    def __init__(self, model_name, CoTCount):
        super().__init__(model_name)
        self.CoTCount = CoTCount
    
    def _process_response(self, response: str):
        pattern =  r"REASON: (?P<reason>.*)\nACTION: (?P<action>open|flag) (?P<x>\d+) (?P<y>\d+)"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            ret = {
                "reason": match.group("reason"),
                "action": match.group("action"),
                "x": int(match.group("x")),
                "y": int(match.group("y"))
            }
            return True, ret
        else:
            return False, None
    
    def _process_continue_response(self, response: str):
        pattern =  r"CORRECTION REASON: (?P<reason>.*)\nCORRECTION ACTION: (?P<action>open|flag) (?P<x>\d+) (?P<y>\d+)"
        match = re.search(pattern, response, re.DOTALL)
        if match:
            ret = {
                "reason": match.group("reason"),
                "action": match.group("action"),
                "x": int(match.group("x")),
                "y": int(match.group("y"))
            }
            return True, ret
        else:
            return False, None

    def getAction(self, game: Game, falied_reason: ActionFeedback):
        promptgen = CoTPrompt()
        prompt_base = ""
        prompt_base += promptgen.intro_game()
        prompt_base += promptgen.intro_cell_state()
        prompt_base += promptgen.intro_actions()
        prompt_base += promptgen.action_format()
        prompt_base += promptgen.regulation()

        # first query
        first_prompt = prompt_base
        first_prompt += promptgen.example_1()
        first_prompt += promptgen.example_2()
        first_prompt += promptgen.example_3()
        first_prompt += promptgen.response_guide(game, falied_reason)
        response = self.api.sendMessage(promptgen.system_message(), first_prompt)
        
        # print(f'first response: {response}')

        valid, response = self._process_response(response)
        if not valid:
            return False, None, None
        
        # continue query
        for _ in range(self.CoTCount):
            reason = response["reason"]
            action = response["action"]
            x = response["x"]
            y = response["y"]
            continue_prompt = prompt_base
            continue_prompt += promptgen.continue_example_1()
            continue_prompt += promptgen.continue_example_2()
            continue_prompt += promptgen.continue_example_3()
            continue_prompt += promptgen.continue_response_guide(game, reason, action, x, y)
            response = self.api.sendMessage(promptgen.system_message(), continue_prompt)
            # print(f'continue response {_}: {response}')

            valid, response = self._process_continue_response(response)
            if not valid:
                return False, None, None
        
        return True, response["action"], (response["x"], response["y"])