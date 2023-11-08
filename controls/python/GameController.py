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
        self.shared_player = SharedVariablesManager().shared_variables_player
        self.shared_enemy = SharedVariablesManager().shared_variables_enemy
        self.interface_main_frame = None
        self.tower_battle_main_frame = None
        self.timer_controller = TimerController()
        self.is_paused = False
        self.game_started = False
        self.enemy_turn = False
        self.prolog_controller = None
        self.timer_controller.timer_button = None
        self.timer_controller.game_controller = self
        self.original_matrix = []
        self.possible_targets = []
        self.focused_walls = []



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
        self.original_matrix = self.get_durability_matrix()
        self.timer_controller.start_timer()

        self.assert_prolog_variables()

    def assert_prolog_variables(self):
        self.prolog_controller.assertz(f"cells({self.shared_player.cells})")
        self.prolog_controller.assertz(f"matrix({self.get_durability_matrix()})")
        self.prolog_controller.assertz(f"original_matrix({self.original_matrix})")

    def get_durability_matrix(self):
        matrix = []
        for i in range(10):
            matrix.append([])
            for j in range(10):
                matrix[i].append(self.shared_player.tower_battle_grid.children()[i * 10 + j + 1].durability)
            #     print(self.shared_player.tower_battle_grid.children()[i * 10 + j + 1].durability, end=" ")
            # print()
        return matrix

    def start_new_game(self):
        self.interface_main_frame.stacked_interface_layout.setCurrentIndex(0)
        self.tower_battle_main_frame.stacked_tower_battle_layout.setCurrentIndex(0)
        self.prolog_controller = PrologController("controls/prolog/file.pl")
        self.shared_player.clear_grid()
        self.shared_enemy.clear_grid()
        self.timer_controller.reset()
        self.game_started = False
        self.is_paused = False
        self.enemy_turn = False
        self.possible_targets = []
        self.focused_walls = []

    def enemy_shoot(self):
        if self.possible_targets:
            target = self.pick_random_possible_target()
        else:
            self.focused_walls = []
            target = self.shared_player.pick_random_cell()
            cell = self.shared_player.tower_battle_grid.grid_layout.itemAtPosition(target.y, target.x).widget()
            if cell.is_selected:
                self.focused_walls = cell.adjacent_cells
            if self.is_game_over(self.shared_player.tower_battle_grid):
                self.timer_controller.stop_main_timer()
                self.tower_battle_main_frame.stacked_tower_battle_layout.setCurrentIndex(2)
                print("GAME OVER!!!")
                return
        self.possible_targets = self.get_possible_targets(target.x, target.y)
        # print("MATRIX\n")
        # for i in range(10):
        #     for j in range(10):
        #         print(self.shared_player.tower_battle_grid.children()[i * 10 + j + 1].durability, end=" ")
        #     print()

    def pick_random_possible_target(self):
        target = random.choice(self.possible_targets)
        cell = self.shared_player.tower_battle_grid.grid_layout.itemAtPosition(target[1], target[0]).widget()
        cell.durability -= 1
        return cell

    def get_possible_targets(self, x, y):
        if not self.focused_walls:
            return []
        possible_targets = self.prolog_controller.pull_query(f"shoot({[x, y]}, Cells)")[0]["Cells"]
        targets = []
        for t in possible_targets:
            if not self.shared_player.tower_battle_grid.grid_layout.itemAtPosition(t[1], t[0]).widget().is_destroyed:
                targets.append(t)

        return targets

    def is_game_over(self, battle_grid):
        for i in range(10):
            for j in range(10):
                cell = battle_grid.children()[i * 10 + j + 1]
                if cell.is_selected and not cell.is_destroyed:
                    return False
        return True
