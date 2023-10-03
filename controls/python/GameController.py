from pyswip import Prolog
import random

from controls.python.JSONController import JSONController
from controls.python.TimerController import TimerController
from views.game_interface.SharedVariables import SharedVariablesManager

class GameControllerMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class GameController(metaclass=GameControllerMeta):
    def __init__(self):
        self.save_file = JSONController.get_absolute_path_to_config_json("game_save.json")
        self.shared_player = SharedVariablesManager().shared_variables_player
        self.shared_enemy = SharedVariablesManager().shared_variables_enemy
        self.interface_main_frame = None
        self.tower_battle_main_frame = None
        self.timer_controller = TimerController()
        self.is_paused = False
        self.game_started = False
        self.enemy_turn = False

        self.timer_controller.timer_button = None
        self.timer_controller.game_controller = self

    def check_game_save(self):
        print(JSONController().json_file_has_records(self.save_file))
        return JSONController().json_file_has_records(self.save_file)

    def load_game_save(self):
        if self.check_game_save():
            pass

    def save_game(self):
        data = {
            "player": self.shared_player.tower_battle_grid.get_cells_data(),
            "enemy": self.shared_enemy.tower_battle_grid.get_cells_data()
        }
        JSONController().save_data_to_json(data, self.save_file)

    def start_game(self):
        self.game_started = True
        self.enemy_turn = random.choice([True, False])
        self.timer_controller.start_timer()
        self.save_game()


    def start_new_game(self):
        self.interface_main_frame.stacked_interface_layout.setCurrentIndex(0)
        self.shared_player.clear_grid()
        self.shared_enemy.clear_grid()
        self.timer_controller.reset()
        self.is_paused = False

