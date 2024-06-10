from AnalysisGame import AnalysisGame
from IncontextAgent import IncontextAgent
from FineTunedAgent import FineTunedAgent
from randomAgent import RandomAgent
from CoTAgent import CoTAgent
from actionFeedback import ActionFeedback
from dataLoader import DataLaoder
from probability import ProbabilityCalculator
import argparse
import random
import math
import os

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

    agent = None
    if config["test_type"] == "Incontext":
        agent = IncontextAgent(config["model_name"])
    elif config["test_type"] == "CoT":
        if config["CoTCount"] is None:
            raise ValueError()
        agent = CoTAgent(config["model_name"], config["CoTCount"])
    elif config["test_type"] == "FineTuned":
        agent = FineTunedAgent(config["model_name"])
    elif config['test_type'] == "Random":
        agent = RandomAgent()

    '''
    valid_action_count: number of valid actions
    format_error_count: number of format errors
    logic_error_count: number of logic errors
    not_zero_count: number of not zero probabilities
    zero_count: number of zero probabilities
    probability_ln_sum: sum of log(probability)
    valid_action_count + format_error_count + logic_error_count = data_loader.get_num_files()
    not_zero_count + zero_count = valid_action_count
    '''
    valid_action_count = 0
    format_error_count = 0
    logic_error_count = 0
    not_zero_count = 0
    zero_count = 0
    probability_ln_sum = 0

    for test_case_id in range(data_loader.get_num_files()):
        game = data_loader.next_game()
        print(f"Test case {test_case_id}")
        if DEBUG_MODE:
            game.printMap()

        # # special process start

        # valid, action, pos, response = None, None, None, None
        # file_names = os.listdir('testcase_response')
        # target_file = data_loader.get_current_file_name()
        # if target_file[0 : -4] + "_response.txt" in file_names:
        #     with open(f'testcase_response/{target_file[0 : -4]}_response.txt', 'r') as f:
        #         response = f.read()
        #     valid, response = agent._process_response(response)
        #     action, pos, response = response['action'], (response['x'], response['y']), response['response']
        # else:        
        #     valid, action, pos, response = agent.getAction(game)
        #     data_loader.write_response(response)

        # # special process end
        valid, action, pos, response = agent.getAction(game)
        data_loader.write_response(response)

        if not valid:
            if DEBUG_MODE:
                print("Format error")
            format_error_count += 1
            continue
        x, y = pos
        if DEBUG_MODE:
            print(action, x, y)

        if action == "open":
            prob = ProbabilityCalculator(game)
            feedback = game.openCell(x, y)
            if feedback == ActionFeedback.SUCCESS:
                valid_action_count += 1
                if abs(prob.getMaxProb()) <= 1e-6:
                    val = 0
                else:
                    val = prob.getSingleProb(x, y) / prob.getMaxProb()
                if abs(val) <= 1e-6:
                    zero_count += 1
                else:
                    not_zero_count += 1
                    probability_ln_sum += math.log(val)
            else:
                if DEBUG_MODE:
                    print("Logic error")
                logic_error_count += 1
        
        if action == "flag":
            prob = ProbabilityCalculator(game)
            feedback = game.setFlag(x, y)
            if feedback == ActionFeedback.SUCCESS:
                valid_action_count += 1
                if abs(prob.getMinProb() - 1) <= 1e-6:
                    val = 0
                val = (1 - prob.getSingleProb(x, y)) / (1 - prob.getMinProb())
                if abs(val) <= 1e-6:
                    zero_count += 1
                else:
                    not_zero_count += 1
                    probability_ln_sum += math.log(val)
            else:
                if DEBUG_MODE:
                    print("Logic error")
                logic_error_count += 1
    
    model_name = config['model_name']
    test_type = config['test_type']
    if config['test_type'] == 'FineTuned':
        model_name = "FineTuned"
    with open(f'output_{model_name}_{test_type}.txt', 'w') as f:
        f.write(f"model: {config['model_name']}\n")
        f.write(f"test_type: {config['test_type']}\n")
        if config['test_type'] == 'CoT':
            f.write(f"CoT count: {config['CoTCount']}\n")
        f.write(f"Total test case: {data_loader.get_num_files()}\n")
        f.write(f"Valid action count: {valid_action_count}\n")
        f.write(f"Format error count: {format_error_count}\n")
        f.write(f"Logic error count: {logic_error_count}\n")
        f.write(f"Zero count: {zero_count}\n")
        f.write(f"Not zero count: {not_zero_count}\n")
        f.write('---------------------------------\n')
        f.write(f"Valid rate: {valid_action_count / data_loader.get_num_files()}\n")
        f.write(f"Format Error rate: {format_error_count / data_loader.get_num_files()}\n")
        f.write(f"Logic Error rate: {logic_error_count / data_loader.get_num_files()}\n")
        if valid_action_count != 0:
            f.write(f"Failed rate: {zero_count / valid_action_count}\n")
            f.write(f"Success rate: {not_zero_count / valid_action_count}\n")
        if not_zero_count != 0:
            f.write(f"Average probability: {math.exp(probability_ln_sum / not_zero_count)}\n")
        
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'error: {e}')