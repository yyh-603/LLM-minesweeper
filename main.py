from game import Game
from game import GameState
from ui import MinesweeperUI

if __name__ == "__main__":
    game = Game(10, 10, 10)
    ui = MinesweeperUI(game)
    ui.run()