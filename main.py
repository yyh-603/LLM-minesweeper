from AnalysisGame import AnalysisGame
from IncontextAgent import IncontextAgent
from FineTunedAgent import FineTunedAgent
from CoTAgent import CoTAgent
from actionFeedback import ActionFeedback
import argparse

def get_argument():
    opt = argparse.ArgumentParser()
    opt.add_argument("--model_name",
                        type=str,
                        required=True,
                        help="model name")
    opt.add_argument("--test_type",
                        type=str,
                        choices=['Incontext', 'FineTuned', 'CoT'],
                        required=True,
                        help="test type")
    opt.add_argument("--CoTCount",
                        type=int,
                        required=False,
                        help="CoT count")
    opt.add_argument("--height",
                        type=int,
                        required=False,
                        help="height of the game",
                        default=9)
    opt.add_argument("--width",
                        type=int,
                        required=False,
                        help="width of the game",
                        default=9)
    opt.add_argument("--mine_num",
                        type=int,
                        required=False,
                        help="number of mines",
                        default=10)
    opt.add_argument("--format_error_threshold",
                        type=int,
                        required=False,
                        help="format error threshold",
                        default=5)
    opt.add_argument("--logic_error_threshold",
                        type=int,
                        required=False,
                        help="logic error threshold",
                        default=5)
    opt.add_argument("--debug",
                        type=bool,
                        required=False,
                        help="debug mode",
                        default=False)
    
    config = vars(opt.parse_args())
    return config

def main():
    config = get_argument()
    FORMAT_ERROR_THRESHOLD = config["format_error_threshold"]
    LOGIC_ERROR_THRESHOLD = config["logic_error_threshold"]
    GAME_WIDTH = config["width"]
    GAME_HEIGHT = config["height"]
    MINE_NUM = config["mine_num"]
    DEBUG_MODE = config["debug"]
    DEBUG_MODE = True
    
    game = AnalysisGame(GAME_HEIGHT, GAME_WIDTH, MINE_NUM)
    
    for i in range(GAME_HEIGHT):
        find_0 = False
        for j in range(GAME_WIDTH):
            if game.getCellData(i, j) == 0:
                find_0 = True
                game.openCell(i, j)
                break
        if find_0:
            break
    
    agent = None
    if config["test_type"] == "Incontext":
        agent = IncontextAgent(config["model_name"])
    elif config["test_type"] == "CoT":
        if config["CoTCount"] is None:
            raise ValueError()
        agent = CoTAgent(config["model_name"], config["CoTCount"])
    elif config["test_type"] == "FineTuned":
        agent = FineTunedAgent(config["model_name"])

    last_error = ActionFeedback.SUCCESS
    while True:
        if game.checkLose():
            print("GPT lose the game")
            break
        if game.checkWin():
            print("GPT win the game")
            break
        
        if game.format_error_count >= FORMAT_ERROR_THRESHOLD:
            print("Format error threshold reached")
            break

        if game.logic_error_count >= LOGIC_ERROR_THRESHOLD:
            print("Logic error threshold reached")
            break

        if DEBUG_MODE:
            game.printMap()
        
        valid, action, pos = agent.getAction(game, last_error)

        if not valid:
            print("Format error")
            game.format_error_count += 1
            last_error = ActionFeedback.FORMAT_ERROR
            continue
            
        x, y = pos
        if DEBUG_MODE:
            print(action, x, y)
        game.total_action_count += 1

        if action == "open":
            last_error = game.openCell(x, y)
            if DEBUG_MODE:
                print(last_error)
        
        if action == "flag":
            last_error = game.setFlag(x, y)
            if DEBUG_MODE:
                print(last_error)
        
    print(f"Valid rate: {game.getValidRate()}")
    print(f"Average probability accurancy: {game.getAverageProbabilityAccurancy()}")
        
if __name__ == '__main__':
    main()