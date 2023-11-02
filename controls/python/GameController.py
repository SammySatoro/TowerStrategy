import random
from pyswip import Prolog
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
        self.prolog_controller = PrologController("controls/prolog/file.pl")
        self.timer_controller.timer_button = None
        self.timer_controller.game_controller = self

        self.in_focus = False
        self.possible_targets = []


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
        self.prolog_controller.assertz(f"cells({self.shared_player.cells})")
        self.prolog_controller.assertz(f"matrix({self.get_durability_matrix()})")
        self.prolog_controller.assertz(f"original_matrix({self.get_durability_matrix()})")

        m = self.prolog_controller.pull_query(f"matrix(M)")[0]["M"]

        for row in m:
            for item in row:
                print(item, end=" ")
            print()

    def get_durability_matrix(self):
        matrix = []
        for i in range(10):
            matrix.append([])
            for j in range(10):
                matrix[i].append(self.shared_player.tower_battle_grid.children()[i * 10 + j + 1].durability)
                print(self.shared_player.tower_battle_grid.children()[i * 10 + j + 1].durability, end=" ")
            print()
        return matrix

    def start_new_game(self):
        self.interface_main_frame.stacked_interface_layout.setCurrentIndex(0)
        self.shared_player.clear_grid()
        self.shared_enemy.clear_grid()
        self.timer_controller.reset()
        self.game_started = False
        self.is_paused = False
        self.enemy_turn = False
        self.in_focus = False

    def enemy_shoot(self):
        for i in range(10):
            for j in range(10):
                if [j, i] in self.shared_player.cells:
                    print(self.shared_player.cells[i * 10 + j], end=" ")
                else:
                    print("[   ]")
            print()

        if self.possible_targets:
            target = self.pick_random_possible_target()
        else:
            target = self.shared_player.pick_random_cell()
        print([target.x, target.y])
        self.possible_targets = self.prolog_controller.pull_query(f"shoot({[target.x, target.y]}, Cells)")[0]["Cells"]
        print(f"pos cells: {self.possible_targets}")

    def pick_random_possible_target(self):
        target = random.choice(self.possible_targets)
        cell = self.shared_player.tower_battle_grid.grid_layout.itemAtPosition(target[1], target[0]).widget()
        cell.durability -= 1
        return cell
