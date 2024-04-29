from game import Game
from game import GameState
from ui import MinesweeperUI

if __name__ == "__main__":
    game = Game(9, 9, 10)
    ui = MinesweeperUI(game)
    ui.run()