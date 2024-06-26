from game import Game
from actionFeedback import ActionFeedback

class FineTunedPrompt:
    def __init__(self):
        self.covered = '.'
        self.flagged = 'F'
        self.mined = '*'
        self.feedback = {
            ActionFeedback.SUCCESS: "You have successfully performed the action.",
            ActionFeedback.FORMAT_ERROR: "Please follow the format.",
            ActionFeedback.INVALID_CELL: "You cannot choose the cell out of bound.",
            ActionFeedback.OPEN_NUMBER_CELL: "You cannot perform \"open\" action on a opened cell. Please choose another cell.",
            ActionFeedback.OPEN_FLAGGED_CELL: "Please unflag the cell before opening it.",
            ActionFeedback.FLAG_NUMBER_CELL: "You cannot flag an opened cell."
        }
        

    def intro_game(self) -> str:
        ret = """---MINESWEEPER INTRODUCTION---
Minesweeper is a single-player puzzle game. The objective of the game is to clear a rectangular board containing hidden "mines" without detonating any of them, with help from clues about the number of neighboring mines in each field.
"""
        return ret
    
    def intro_cell_state(self) -> str:
        ret = """---MINESWEEPER CELL STATE---
Minesweeper board is a grid of cells. Each cell can be in one of the following states:
- Covered: The cell is covered and its content is hidden. You can reveal the content of the cell by "open" it. We use `{self.covered} to represent a covered cell.
- Flagged: The cell is covered and marked with a flag. You can flag a cell by "flag" it. Flagged cell cannot be opened. You can unflag a cell by "flag" on a flagged cell, which will return to "Covered" state. We use `{self.flagged}` to represent a flagged cell.
- Opened: The cell is opened and its content is revealed. Note that you cannot open an opened cell. The content of the cell can be:
    - Empty: The cell has no mine and no neighboring mine. If you open an empty cell, it will reveal all its neighboring cells recursively.
    - Number: The cell has no mine and has a number indicating the number of neighboring mines.
    - Mine: The cell has a mine. If you open a cell with mine, you lose the game.
    We use numbers from 0 to 8 to represent the number of neighboring mines. We use `*` to represent a mine.
"""
        return ret
    
    def intro_actions(self) -> str:
        ret = """---MINESWEEPER ACTIONS---
You can perform the following actions during the game:
- Open: Open a covered cell. If the cell has no mine and no neighboring mine, it will reveal all its neighboring cells recursively.
- Flag: Flag a covered cell. Flagged cell cannot be opened. You can unflag a cell by "flag" on a flagged cell, which will return to "Covered" state.
"""
        return ret

    def action_format(self) -> str:
        ret = """---MINESWEEPER ACTION FORMAT---
To perform an action, you need to specify the action and the cell you want to perform the action on. The format is:
    <action> <row> <column>
Where:
- <action> is the action you want to perform, which can be "open" or "flag".
- <row> is the row number of the cell, starting from 0.
- <column> is the column number of the cell, starting from 0.
For example:
    open 0 0
    flag 1 2
""" 
        return ret

    def regulation(self) -> str:
        ret = """---MINESWEEPER REGULATION---
Please ensure:
- The row and column numbers are within the board size.
- The action is valid based on the current state of the cell.
- Submit one action in each turn.
- Think carefully before making a move.
"""
        return ret

    def response_guide(self, game, feedback):
        if feedback is not None or feedback != ActionFeedback.SUCCESS:
            feedback_str = f"NOTICE: {self.feedback[feedback]}"
        else:
            feedback_str = ""
        grid = game.gridFormat()
        ret = f"""---RESPONSE GUIDE---
Let's think step by step.
{feedback_str}
Begin your action in "ACTION:" part.
TABLE:
{grid}
"""
        return ret

    def system_message(self):
        return """You are a clever minesweeper player. 
You have to choose the most safety cell to open it or flag it.
You will not guess answer, instead, you will output your action by your inference.
"""
    
if __name__ == '__main__':
    game = Game(9, 9, 10)
    game.openCell(4, 4)
    prompt = FineTunedPrompt()
    print(prompt.intro_game())
    print(prompt.intro_cell_state())
    print(prompt.intro_actions())
    print(prompt.action_format())
    print(prompt.regulation())
    print(prompt.response_guide(game, ActionFeedback.FLAG_NUMBER_CELL))
