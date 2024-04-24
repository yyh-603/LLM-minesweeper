import tkinter as tk
from game import Game, GameState

class MinesweeperUI:
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.window.title("Minesweeper")
        self.buttons = [[None for _ in range(game.map.width)] for _ in range(game.map.height)]
        for i in range(game.map.height):
            for j in range(game.map.width):
                self.buttons[i][j] = tk.Button(self.window, command=lambda x=i, y=j: self.open_cell(x, y), width=2, height=1)
                self.buttons[i][j].grid(row=i, column=j)
        
        for i in range(game.map.height):
            for j in range(game.map.width):
                self.buttons[i][j] = tk.Button(self.window, command=lambda x=i, y=j: self.open_cell(x, y), width=2, height=1)
                self.buttons[i][j].grid(row=i, column=j)
                self.buttons[i][j].bind('<Button-3>', lambda event, x=i, y=j: self.toggle_flag(x, y))

    def open_cell(self, x, y):
        self.game.openCell(x, y)
        self.update_buttons()
        if self.game.state == GameState.WIN:
            print("You win!")
        elif self.game.state == GameState.LOSE:
            print("You lose!")
    
    def toggle_flag(self, x, y):
        if self.game.map.map[x][y].hasFlag:
            self.game.removeFlag(x, y)
        else:
            self.game.setFlag(x, y)
        self.update_buttons()

    def update_buttons(self):
        for i in range(self.game.map.height):
            for j in range(self.game.map.width):
                if self.game.map.map[i][j].isOpen:
                    if self.game.map.map[i][j].data == -1:
                        self.buttons[i][j].config(text="X", state="disabled")
                    else:
                        self.buttons[i][j].config(text=str(self.game.map.map[i][j].data), state="disabled")

                elif self.game.map.map[i][j].hasFlag:
                    self.buttons[i][j].config(text="F")
                
                else:
                    self.buttons[i][j].config(text="", state="normal")
        print(self.game.map.gridFormat())

    def run(self):
        self.window.mainloop()

# Test
if __name__ == "__main__":
    game = Game(10, 10, 10)
    ui = MinesweeperUI(game)
    ui.run()