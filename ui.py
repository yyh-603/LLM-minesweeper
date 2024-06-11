import tkinter as tk
from game import Game
from IncontextAgent import IncontextAgent
from FineTunedAgent import FineTunedAgent
from CoTAgent import CoTAgent
from randomAgent import RandomAgent
import time
from agent import Agent
import argparse

class MinesweeperUI:
    def __init__(self, game: Game, agent: Agent):
        self.game = game  # The game instance
        self.agent = agent  # The agent instance
        self.window = tk.Tk()  # The main window
        self.window.title("Minesweeper")  # Set the window title
        # Initialize the buttons matrix
        self.buttons = [[None for _ in range(game.getWidth())] for _ in range(game.getHeight())]
        # Create the buttons and add them to the window
        for i in range(game.getHeight()):
            for j in range(game.getWidth()):
                self.buttons[i][j] = tk.Label(self.window, width=2, height=1)
                self.buttons[i][j].grid(row=i, column=j)

    def update_buttons(self):
        for i in range(self.game.getHeight()):
            for j in range(self.game.getWidth()):
                if self.game.getCellIsOpen(i, j):
                    # If the cell is open, set the label's text to the number of mines around the cell
                    data = self.game.getCellData(i, j)
                    if data == -1:
                        self.buttons[i][j]['text'] = 'X'
                    else:
                        self.buttons[i][j]['text'] = str(self.game.getCellData(i, j))
                elif self.game.getCellHasFlag(i, j):
                    self.buttons[i][j]['text'] = 'F'
                else:
                    # If the cell is not open, clear the label's text
                    self.buttons[i][j]['text'] = ''
        if self.game.checkWin():
            print('You win!')
            input("Press Enter to continue...")
            self.window.destroy()
            return
        elif self.game.checkLose():
            print('You lose!')
            input("Press Enter to continue...")
            self.window.destroy()
            return
        _, action, (x, y), _ = self.agent.getAction(self.game)
        if action == "open":
            self.game.openCell(x, y)
        elif action == "flag":
            self.game.setFlag(x, y)

    def run(self):
        self.update_buttons()  # Update the labels immediately
        self.window.after(1000, self.run)  # Schedule the next update in 1 second
        self.window.mainloop()  # Start the Tkinter event loop

def get_argument():
    opt = argparse.ArgumentParser()
    opt.add_argument("--model_name",
                        type=str,
                        required=True,
                        help="model name")
    opt.add_argument("--test_type",
                        type=str,
                        choices=['Incontext', 'FineTuned', 'CoT', 'Random'],
                        required=True,
                        help="test type")
    opt.add_argument("--file_path",
                        type=str,
                        required=True,
                        help="map file path")
    opt.add_argument("--CoTCount",
                        type=int,
                        required=False,
                        help="CoT count")
    opt.add_argument("--fixed-seed",
                        type=bool,
                        required=False,
                        help="fixed seed",
                        default=False)                     
    
    config = vars(opt.parse_args())
    return config

if __name__ == "__main__":
    config = get_argument()
    game = Game(filename=config["file_path"])  # Create a game instance
    if config['test_type'] == "Incontext":
        agent = IncontextAgent(config["model_name"])
    elif config['test_type'] == "FineTuned":
        agent = FineTunedAgent(config["model_name"])
    elif config['test_type'] == "CoT":
        agent = CoTAgent(config["model_name"], config["CoTCount"])
    elif config['test_type'] == "Random":
        agent = RandomAgent()
    ui = MinesweeperUI(game, agent)  # Create a UI instance
    ui.run()  # Start the UI