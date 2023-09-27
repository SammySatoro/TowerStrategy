import json
import os

class JSONController():

    @staticmethod
    def save_data_to_json(data, file_name):
        directory = os.path.dirname(file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(directory)
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def load_data_from_json(file_name):
        try:
            with open(file_name, 'r') as json_file:
                data = json.load(json_file)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    @staticmethod
    def json_file_has_records(file_name):
        try:
            with open(file_name, 'r') as json_file:
                data = json.load(json_file)
                return bool(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    @staticmethod
    def get_absolute_path_to_config_json(file_name):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        relative_path_to_json = os.path.join("..", "..", "config", file_name)
        return os.path.abspath(os.path.join(script_directory, relative_path_to_json))