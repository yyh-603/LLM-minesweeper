from game import Game
from openaiAPI import OpenAIAPI

class Agent:
    def __init__(self, modelName: str, mapFormatFunc):
        self.api = OpenAIAPI(modelName)
        self.mapFormatFunc = mapFormatFunc

    def _readtxt(self, filePath: str) -> str:
        with open(filePath, 'r') as f:
            return f.read()
    
    def getAction(self, game: Game):
        raise NotImplementedError()

    def returnFaliedAction(self, game: Game):
        raise NotImplementedError()
    
    def returnFailedFormat(self, game: Game):
        raise NotImplementedError()