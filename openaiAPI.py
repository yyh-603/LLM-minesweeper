import openai
from game import Game
import os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY

class OpenAIAPI:
    '''
    client: OpenAI API client
    model_type: the type of model to use
    '''
    def __init__(self, model_type):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.model_type = model_type

    def sendInit():
        pass


    def sendMap(self, prompt, map: Game):
        # print(map.gridFormat())
        response = self.client.chat.completions.create(
            model = self.model_type,
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": map.gridFormat()}
            ],
        )
        return response.choices[0].message.content

    def sendWin():
        pass
    
    def sendLose():
        pass

if __name__ == '__main__':
    map = Game(10, 10, 10)
    api = OpenAIAPI("gpt-3.5-turbo")
    count = 0
    prompt = """
You are a minesweeper player. You are given a map of minesweeper.
number in the map stands for the number of mines around the cell. "F" stands for flag. "." stands for unknown cell.
The map is formatted as follows:
0 0 0 0 0 0 0 0 0 0 
0 0 1 1 2 2 2 1 1 1
0 0 1 F 2 . . . . .
0 0 1 1 2 2 2 1 2 .
1 1 0 0 0 0 0 0 1 .
. 1 0 0 0 0 0 0 1 1
. 1 0 1 1 1 0 0 0 0
. 1 1 2 . 1 0 0 1 1
. . . . . 2 0 0 1 .
. . . . . 1 0 0 1 .
For example, the only flag in the map is at (2, 3).
index starts from 0.
index from top to bottom, left to right.
You can do the following actions:
1. Open a cell: open x y
2. Set a flag: flag x y
3. Remove a flag: remove x y
A possible action of above map is: flag 5 0
You can only open a cell if it is not flagged and not already opened.
You can only set a flag if the cell is not opened.
You can only remove a flag if the cell is flagged.
Given a map, you have to response the next action you want to do.
You don't need to output your reason.
Output format:
[Action] [x] [y]
"""
    while True:
        response = api.sendMap(prompt, map)
        print(response)
        op, x, y = response.split()
        x = int(x)
        y = int(y)
        valid = False
        if op.lower() == "open":
            valid = map.openCell(x, y)
        if op.lower() == "flag":
            valid = map.setFlag(x, y)
        if op.lower() == "remove":
            valid = map.removeFlag(x, y)
        if not valid:
            break

        count += 1
        print(count)
        print(map.gridFormat())

        if map.checkWin():
            print("You win!")
            break

        if map.checkLose():
            print("You lose!")
            break
