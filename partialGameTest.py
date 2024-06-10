from AnalysisGame import AnalysisGame
from IncontextAgent import IncontextAgent
from FineTunedAgent import FineTunedAgent
from CoTAgent import CoTAgent
from actionFeedback import ActionFeedback
from dataLoader import DataLaoder
from probability import ProbabilityCalculator
import argparse
import random
import math

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
    opt.add_argument("--dir_path",
                        type=str,
                        required=True,
                        help="directory path")
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
    opt.add_argument("--fixed-seed",
                        type=bool,
                        required=False,
                        help="fixed seed",
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
    FIXED_SEED = config["fixed_seed"]
    
    if FIXED_SEED:
        random.seed(114514)
    
    data_loader = DataLaoder(config["dir_path"])



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

    valid_open_count = 0
    total_open_count = 0
    valid_flag_count = 0
    total_flag_count = 0
    format_error_count = 0
    logic_error_count = 0
    probability_ln_sum = 0

    for test_case_id in range(data_loader.get_num_files()):
        game = data_loader.next_game()
        if DEBUG_MODE:
            print(f"Test case {test_case_id}")
            game.printMap()
        
        valid, action, pos = agent.getAction(game)
        
        if not valid:
            print("Format error")
            format_error_count += 1
            continue
        x, y = pos
        if DEBUG_MODE:
            print(action, x, y)

        if action == "open":
            total_open_count += 1
            prob = ProbabilityCalculator(game)
            feedback = game.openCell(x, y)
            if feedback == ActionFeedback.SUCCESS:
                valid_open_count += 1
                probability_ln_sum += math.log(prob.getSingleProb(x, y))
            else:
                logic_error_count += 1
        
        if action == "flag":
            total_flag_count += 1
            prob = ProbabilityCalculator(game)
            feedback = game.setFlag(x, y)
            if feedback == ActionFeedback.SUCCESS:
                valid_flag_count += 1
                probability_ln_sum += math.log(1 - prob.getSingleProb(x, y))
            else:
                logic_error_count += 1
    
    print(f"valid open rate: {valid_open_count / total_open_count}")
    print(f"valid flag rate: {valid_flag_count / total_flag_count}")
    print(f"total valid rate: {(valid_open_count + valid_flag_count) / (total_open_count + total_flag_count)}")
    print(f"average probability: {math.exp(probability_ln_sum / (valid_open_count + valid_flag_count))}")
        
if __name__ == '__main__':
    main()