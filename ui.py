import tkinter as tk
from game import Game

class MinesweeperUI:
    def __init__(self, game: Game):
        self.game = game
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.buttons = [[None for _ in range(game.getWidth())] for _ in range(game.getHeight())]
        for i in range(game.getHeight()):
            for j in range(game.getWidth()):
                self.buttons[i][j] = tk.Button(self.window, command=lambda x=i, y=j: self.open_cell(x, y), width=2, height=1)
                self.buttons[i][j].grid(row=i, column=j)
        
        for i in range(game.getHeight()):
            for j in range(game.getWidth()):
                self.buttons[i][j] = tk.Button(self.window, command=lambda x=i, y=j: self.open_cell(x, y), width=2, height=1)
                self.buttons[i][j].grid(row=i, column=j)
                self.buttons[i][j].bind('<Button-3>', lambda event, x=i, y=j: self.toggle_flag(x, y))

    def open_cell(self, x, y):
        self.game.openCell(x, y)
        print(x, y)
        self.update_buttons()
        if self.game.checkWin():
            print("You win!")
        elif self.game.checkLose():
            print("You lose!")
    
    def toggle_flag(self, x, y):
        # if self.game.getCellHasFlag(x, y):
        #     self.game.removeFlag(x, y)
        # else:
        self.game.setFlag(x, y)
        self.update_buttons()

    def update_buttons(self):
        for i in range(self.game.getHeight()):
            for j in range(self.game.getWidth()):
                if self.game.getCellIsOpen(i, j):
                    if self.game.getCellData(i, j) == -1:
                        self.buttons[i][j].config(text="X", state="disabled")
                    else:
                        self.buttons[i][j].config(text=str(self.game.getCellData(i, j)), state="disabled")

                elif self.game.getCellHasFlag(i, j):
                    self.buttons[i][j].config(text="F")
                
                else:
                    self.buttons[i][j].config(text="", state="normal")
        self.game.printMap()

    def run(self):
        self.window.mainloop()

# Test
if __name__ == "__main__":
    game = Game(filename='partial_unittest_data/9_9_10_1_0.txt')
    ui = MinesweeperUI(game)
    ui.run()