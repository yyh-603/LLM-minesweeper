from game import Game
from openaiAPI import OpenAIAPI
from agent import Agent

class CoTAgent(Agent):

    def __init__(self, CoTCount):
        self.CoTCount = CoTCount

    def getAction(self, game: Game):
        firstPrompt = self._readtxt('prompt/CoTFirst.txt')
        contiPrompt = self._readtxt('prompt/CoTConti.txt')
        contentBased = self._readtxt('prompt/CoTContent.txt')
        response = self.api.sendMessage(firstPrompt, self.mapFormatFunc(game))
        
        for _ in range(self.CoTCount):
            # TODO: make content from response
            # content need include action, reason, and game
            raise NotImplementedError()
            content = contentBased + response + self.mapFormatFunc(game)

            response = self.api.sendMessage(contiPrompt, content)
        
        # TODO: response process

    def returnFailedAction(self, game: Game):
        raise NotImplementedError()

    def returnFailedFormat(self, game: Game):
        raise NotImplementedError()
