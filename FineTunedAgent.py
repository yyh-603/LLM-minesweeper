from game import Game
from openaiAPI import OpenAIAPI
from agent import Agent

class FineTunedAgent(Agent):
    
    def getAction(self, game: Game):
        prompt = self._readtxt('prompt/FineTuned.txt')
        response = self.api.sendMessage(prompt, self.mapFormatFunc(game))

        # TODO: response process
        raise NotImplementedError()

    def returnFaliedAction(self, game: Game):
        prompt = self._readtxt('prompt/FineTunedFailedAction.txt')
        response = self.api.sendMessage(prompt, self.mapFormatFunc(game))

        # TODO: response process
        raise NotImplementedError()

    def returnFailedFormat(self, game: Game):
        prompt = self._readtxt('prompt/FineTunedFailedFormat.txt')
        response = self.api.sendMessage(prompt, self.mapFormatFunc(game))

        # TODO: response process
        raise NotImplementedError()