from game import Game
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

    def write_response(self, response) -> None:
        filename = self.file_names[self.current_file_index - 1][0 : -4] + "_response.txt"
        response_dir_path = self.dir_path + "_response"
        if not os.path.exists(response_dir_path):
            os.mkdir(response_dir_path)
        with open(os.path.join(response_dir_path, filename), "w") as f:
            if isinstance(response, str):
                f.write(response)
            elif isinstance(response, list):
                for i, item in enumerate(response):
                    f.write(f'------- {i}th response -------\n')
                    f.write(item + '\n')
    
    def get_current_file_name(self):
        return self.file_names[self.current_file_index - 1]
    
