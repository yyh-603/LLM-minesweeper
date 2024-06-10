from game import Game
from agent import Agent
from actionFeedback import ActionFeedback
import random

class RandomAgent():
    def __init__(self):
        pass

    def getAction(self, game: Game, falied_reason: ActionFeedback = ActionFeedback.SUCCESS):
        valid_pos = []
        for i in range(game.height):
            for j in range(game.width):
                if not game.getCellIsOpen(i, j):
                    valid_pos.append((i, j))
        action = random.choice(["open", "flag"])
        x, y = random.choice(valid_pos)
        return True, action, (x, y), "114514"