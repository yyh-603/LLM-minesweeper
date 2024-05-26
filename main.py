from game import Game
from openaiAPI import OpenAIAPI
from IncontextAgent import IncontextAgent

def main():
    game = Game(9, 9, 10)
    agent = IncontextAgent("gpt-3.5-turbo")