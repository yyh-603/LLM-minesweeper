import tkinter as tk
from game import Game
from randomAgent import RandomAgent

class MinesweeperUI:
    def __init__(self, game: Game):
        self.game = game  # The game instance
        self.window = tk.Tk()  # The main window
        self.window.title("Minesweeper")  # Set the window title
        # Initialize the buttons matrix
        self.buttons = [[None for _ in range(game.getWidth())] for _ in range(game.getHeight())]
        # Create the buttons and add them to the window
        for i in range(game.getHeight()):
            for j in range(game.getWidth()):
                self.buttons[i][j] = tk.Button(self.window, command=lambda x=i, y=j: self.open_cell(x, y), width=2, height=1)
                self.buttons[i][j].grid(row=i, column=j)
        
        # Bind the right click event to the toggle_flag method
        for i in range(game.getHeight()):
            for j in range(game.getWidth()):
                self.buttons[i][j].bind('<Button-3>', lambda event, x=i, y=j: self.toggle_flag(x, y))

    def open_cell(self, x, y):
        self.game.openCell(x, y)  # Open the cell in the game
        self.update_buttons()  # Update the buttons' states
        # Check if the game is won or lost
        if self.game.checkWin():
            print("You win!")
        elif self.game.checkLose():
            print("You lose!")
    
    def toggle_flag(self, x, y):
        # Toggle the flag of the cell in the game
        self.game.setFlag(x, y)
        self.update_buttons()  # Update the buttons' states

    def update_buttons(self):
        # Update the text and state of each button based on the game's state
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
        self.game.printMap()  # Print the game's map to the console

    def process_action(self, action, x, y):
        if action == "open":
            self.open_cell(x, y)
        elif action == "flag":
            self.toggle_flag(x, y)

    def run(self):
        agent = RandomAgent()
        while not self.game.checkWin() and not self.game.checkLose():
            _, action, (x, y), _ = agent.getAction(self.game)
            self.process_action("flag", x, y)
            print(x, y)
            self.update_buttons()  # Update the buttons' states
            self.window.after(3000, self.run)
            self.window.mainloop()  # Start the main loop

# Test
if __name__ == "__main__":
    game = Game(filename='partial_unittest_data/9_9_10_1_0.txt')  # Create a game instance
    ui = MinesweeperUI(game)  # Create a UI instance
    ui.run()  # Start the UI
    