from game import Game
from IncontextPrompt import IncontextPrompt
class CoTPrompt(IncontextPrompt):
    def continue_response_guide(self, game, reason, action, x, y):
        grid = game.gridFormat()
        ret = f"""---RESPONSE GUIDE---
According to the current game state, exisiting reason and action, please judge the existing action is good or not.
Give your reason in "CORRECTION REASON:" part, and your action after corrected in "CORRECTION ACTION:" part.
Notice that the action may contain invalid action.
TABLE:
{grid}
REASON: {reason}
ACTION: {action} {x} {y}
"""
        
    def continue_example_1(self):
        ret = f"""---MINESWEEPER EXAMPLE 1---
TABLE:
. . . 1 0 0 1 . .
. . . 2 0 0 1 . .
. . . 1 0 0 1 1 1
. . . 1 0 0 0 0 0
. . . 1 0 0 0 0 0
. . . 1 0 0 0 0 0
. . . 2 1 1 0 0 0
. . . . . 2 0 0 0
. . . . . 2 0 0 0
REASON: Because the cell at (3, 3) has 1 neighboring mine, and only 1 neighboring cell is not opened, we can know that the cell at (3, 2) is a mine. So we flag it.
ACTION: flag 3 2
CORRECTION REASON: There are 3 neighboring cell of the cell at (3, 3) is not opened, so we can't know the cell at (3, 2) is a mine.
Consider another cell, the cell at (2, 6) has 1 neighboring mine, and only 1 neighboring cell is not opened, we can know that the cell at (1, 7) is a mine. So we flag it.
CORRECTION ACTION: flag 1 7
"""
        return ret
    def continue_example_2(self):
        ret = f"""---MINESWEEPER EXAMPLE 2---
TABLE:
. . . . . . . . . 
. . . . . . . . .
1 1 1 1 . . . . .
0 0 0 1 1 . . . .
0 0 0 0 1 . . . .
0 1 1 2 2 . . . .
0 1 F . . . . . .
0 1 1 3 . . . . .
0 0 0 1 . . . . .
REASON: Because the cell at (1, 7) has 1 neighboring mine, and we know that the cell at (1, 8) is a mine, we can open the cell at (2, 7) safely.
ACTION: open 2 7
CORRECTION REASON: There is no information about the cell at (1, 7).
Consider another cell, the cell at (5, 2) has 1 neighboring mine, and we know that the cell at (6, 2) is a mine, we can open the cell at (6, 3) safely.
CORRECTION ACTION: open 6 3
"""
        return ret
    def continue_example_3(self):
        ret = f"""---MINESWEEPER EXAMPLE 3---
TABLE:
0 0 1 . . 1 0 0 0 
0 0 1 2 . 2 1 1 0
1 1 0 1 1 2 . 1 0
. 2 0 0 0 1 1 1 0
. 2 0 0 0 0 0 0 0
. 2 1 1 0 0 0 0 0
. . F 3 1 1 0 0 0
. 3 F 3 F 1 0 1 1
. 2 1 2 1 1 0 1 .
REASON: Because the cell at (8, 1) has 2 neighboring mines, and we know that the cell at (7, 2) is a mine, we know that the cells (7, 0) and (8, 0) has 1 mine.
The cell are (7, 1) has 3 neighboring mines, and we know that the cell at (7, 2), (6, 2) has two mines, and (7, 0) and (8, 0) has one mine, we can open the cell at (6, 1) safely.
ACTION: open 6 1
CORRECTION REASON: The existing reason is reasonable, There is no need to change it.
CORRECTION ACTION: open 6 1
"""
        return ret
        