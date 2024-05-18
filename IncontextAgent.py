from game import Game
from openaiAPI import OpenAIAPI
from agent import Agent

class IncontextAgent(Agent):

    def getAction(self, game: Game):
        prompt = self._readtxt('prompt/Incontext.txt')
        response = self.api.sendMessage(prompt, self.mapFormatFunc(game))

        # TODO: response process
        raise NotImplementedError()


    def returnFaliedAction(self, game: Game):
        prompt = self._readtxt('prompt/IncontextFailedAction.txt')
        response = self.api.sendMessage(prompt, self.mapFormatFunc(game))
    
        # TODO: response process
        raise NotImplementedError()
    
    def returnFailedFormat(self, game: Game):
        prompt = self._readtxt('prompt/IncontextFailedFormat.txt')
        response = self.api.sendMessage(prompt, self.mapFormatFunc(game))

        # TODO: response process
        raise NotImplementedError()