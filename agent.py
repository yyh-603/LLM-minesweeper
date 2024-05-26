from game import Game
from openaiAPI import OpenAIAPI
from actionFeedback import ActionFeedback

class Agent:
    def __init__(self, modelName: str):
        self.api = OpenAIAPI(modelName)

    def process_response(self, response: str):
        raise NotImplementedError()
    
    def getAction(self, game: Game):
        raise NotImplementedError()

    def returnFalied(self, game: Game, falied_reason: ActionFeedback):
        raise NotImplementedError()
    