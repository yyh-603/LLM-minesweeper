from game import Game
from actionFeedback import ActionFeedback
from probability import ProbabilityCalculator
import os

class DataLaoder():
    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self.file_names = os.listdir(self.dir_path)
        self.current_file_index = 0
        self.current_game = None
        self.num_files = len(self.file_names)
    
    def isFinished(self) -> bool:
        return self.current_file_index == self.num_files

    def get_num_files(self) -> int:
        return self.num_files

    def next_game(self) -> Game:
        if self.isFinished():
            return None
        filepath = os.path.join(self.dir_path, self.file_names[self.current_file_index])
        self.current_game = Game(filename = filepath)
        self.current_file_index += 1
        return self.current_game

