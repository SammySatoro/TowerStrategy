import random

from controls.python.JSONController import JSONController
from controls.python.TimerController import TimerController
from views.game_interface.SharedVariables import SharedVariablesManager
from controls.python.PrologController import PrologController

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

        self.prolog_controller = PrologController("file.pl")
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

    def get_wall_cells(self):
        wall_cells = []
        for idx, wall in enumerate(self.shared_player._selected_combinations):
            wall_cells.append([])
            for cell in wall:
                wall_cells[idx].append([cell[0], cell[1]])
        return wall_cells

    def start_game(self):
        self.game_started = True
        self.enemy_turn = random.choice([True, True, False, False, False])
        self.timer_controller.start_timer()
        self.save_game()

        # matrix1 = [[0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        #     [0, 3, 0, 0, 0, 0, 0, 0, 0, 1], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 2, 0, 1, 1, 2, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 1, 1, 0, 0]]
        #
        # wall_cells = [[[7, 0], [7, 1], [6, 1], [6, 2]], [[1, 2], [1, 3], [1, 4]], [[3, 6], [4, 6], [5, 6]],
        #     [[9, 6], [9, 7]], [[6, 9], [7, 9]], [[1, 8], [2, 8]], [[3, 0]], [[7, 6]], [[9, 3]], [[1, 6]]]
        #
        # cells = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [0, 1], [1, 1], [2, 1],
        #     [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2],
        #     [6, 2], [7, 2], [8, 2], [9, 2], [0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3],
        #     [9, 3], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [9, 4], [0, 5], [1, 5],
        #     [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5], [9, 5], [0, 6], [1, 6], [2, 6], [3, 6], [4, 6],
        #     [5, 6], [6, 6], [7, 6], [8, 6], [9, 6], [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7],
        #     [8, 7], [9, 7], [0, 8], [1, 8], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [8, 8], [9, 8], [0, 9],
        #     [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [7, 9], [8, 9], [9, 9]]
        #
        # self.prolog_controller.assertz(f"cells({cells})")
        # self.prolog_controller.assertz(f"matrix({matrix1})")
        # self.prolog_controller.assertz(f"wall_cells({wall_cells})")
        #
        # for row in range(10):
        #     for col in range(10):
        #         print(
        #             int(self.shared_player.tower_battle_grid.grid_layout.itemAtPosition(row, col).widget().is_selected),
        #             end=" "
        #         )
        #     print()
        #
        # print(self.get_wall_cells())


    def start_new_game(self):
        self.interface_main_frame.stacked_interface_layout.setCurrentIndex(0)
        self.shared_player.clear_grid()
        self.shared_enemy.clear_grid()
        self.timer_controller.reset()
        self.is_paused = False
