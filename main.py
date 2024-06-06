from game import Game
from IncontextAgent import IncontextAgent
from actionFeedback import ActionFeedback
from probability import ProbabilityCalculator
from CoTAgent import CoTAgent

FORMAT_ERROR_THRESHOLD = 5
LOGIC_ERROR_THRESHOLD = 5
GAME_WIDTH = 9
GAME_HEIGHT = 9
MINE_NUM = 10

def main():
    game = Game(GAME_HEIGHT, GAME_WIDTH, MINE_NUM)
    for i in range(GAME_HEIGHT):
        for j in range(GAME_WIDTH):
            if game.getCellData(i, j) == 0:
                game.openCell(i, j)
                break

    agent = CoTAgent("gpt-3.5-turbo", 3)
    format_error_count = 0
    logic_error_count = 0
    valid_open_count = 0
    valid_open_rate = 1.0
    valid_action_count = 0
    total_action_count = 0
    last_error = None
    while True:
        if game.checkLose():
            print("GPT lose the game")
            break
        if game.checkWin():
            print("GPT win the game")
            break

        if format_error_count >= FORMAT_ERROR_THRESHOLD:
            print("Format error threshold reached")
            break

        if logic_error_count >= LOGIC_ERROR_THRESHOLD:
            print("Logic error threshold reached")
            break

        game.printMap()
        valid, action, pos = agent.getAction(game, last_error)

        if not valid:
            print("Format error")
            format_error_count += 1
            last_error = ActionFeedback.FORMAT_ERROR
            continue
            
        x, y = pos
        print(action, x, y)
        total_action_count += 1
        
        if not game.validPos(x, y):
            print("Logic error")
            logic_error_count += 1
            last_error = ActionFeedback.INVALID_CELL
            continue
        
        if action == "open":
            if game.getCellIsOpen(x, y):
                print("Logic error")
                logic_error_count += 1
                last_error = ActionFeedback.OPEN_NUMBER_CELL
            elif game.getCellHasFlag(x, y):
                print("Logic error")
                logic_error_count += 1
                last_error = ActionFeedback.OPEN_FLAGGED_CELL
            else:
                print("valid move")
                valid_action_count += 1
                valid_open_count += 1
                prob_gen =  ProbabilityCalculator(game)
                prob_gen.run()
                valid_open_rate *= prob_gen.getSingleProb(x, y)
                game.openCell(x, y)
                last_error = None

        
        if action == "flag":
            if game.getCellIsOpen(x, y):
                print("Logic error")
                logic_error_count += 1
                last_error = ActionFeedback.FLAG_NUMBER_CELL
            else:
                print("valid move")
                if game.getCellHasFlag(x, y):
                    game.removeFlag(x, y)
                else:
                    game.setFlag(x, y)
                last_error = None
        
    print(f"valid open count: {valid_open_count}.")
    print(f"valid open rate: {valid_open_rate}.")
    print(f"valid action count: {valid_action_count}.")
    print(f"valid action rate: {valid_action_count / total_action_count}.")

        
if __name__ == '__main__':
    main()