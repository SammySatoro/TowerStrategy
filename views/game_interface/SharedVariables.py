import random

from PyQt6.QtWidgets import QFrame


class SharedVariablesMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class SharedVariablesManager(metaclass=SharedVariablesMeta):
    def __init__(self):
        self.shared_variables_player = SharedVariables()
        self.shared_variables_enemy = SharedVariables()

class SharedVariables():
    _instances = []

    def __new__(cls):
        if len(cls._instances) < 2:
            instance = super(SharedVariables, cls).__new__(cls)
            cls._instances.append(instance)
            instance.initialize()
            return instance
        else:
            raise Exception("Only two instances of SharedVariables are allowed.")


    def initialize(self):
        self.is_dragging = False
        self.selected_cells = []
        self._selected_combinations = []
        self.combinations = {
            1: 4,
            2: 3,
            3: 2,
            4: 1
        }
        self.available_cells = self._set_available_cells()
        self.possible_cells = []
        self.cells = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [0, 1], [1, 1],
            [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2],
            [5, 2], [6, 2], [7, 2], [8, 2], [9, 2], [0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3],
            [8, 3], [9, 3], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [9, 4], [0, 5],
            [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5], [9, 5], [0, 6], [1, 6], [2, 6], [3, 6],
            [4, 6], [5, 6], [6, 6], [7, 6], [8, 6], [9, 6], [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7],
            [7, 7], [8, 7], [9, 7], [0, 8], [1, 8], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [8, 8], [9, 8],
            [0, 9], [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [7, 9], [8, 9], [9, 9]]
        self.walls_durabilities = [3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.tower_battle_grid = QFrame()

    @property
    def selected_combinations(self):
        return self._selected_combinations

    @selected_combinations.setter
    def selected_combinations(self, combinations: list):
        self.clear_grid()
        self._selected_combinations = combinations
        self.combinations[1] = 0
        self.combinations[2] = 0
        self.combinations[3] = 0
        self.combinations[4] = 0

        self.set_adjacent_cells()
        self.place_walls(self._selected_combinations)


    def pick_random_cell(self):                                    # to prolog
        target = random.choice(self.available_cells)
        cell = self.tower_battle_grid.grid_layout.itemAtPosition(target[1], target[0]).widget()
        cell.durability -= 1
        return cell

    def add_to_possible_cells(self, cells):
        for cell in cells:
            if cell not in self.possible_cells:
                self.possible_cells.append(cells)

    def _set_available_cells(self):
        cells = []
        for i in range(10):
            for j in range(10):
                cells.append([i, j])
        return cells

    def set_adjacent_cells(self):
        for comb in self._selected_combinations:
            for c in comb:
                self.tower_battle_grid.grid_layout.itemAtPosition(c[1], c[0]).widget().adjacent_cells = comb

    def clear_grid(self):
        self._selected_combinations = []
        self.combinations[1] = 4
        self.combinations[2] = 3
        self.combinations[3] = 2
        self.combinations[4] = 1
        self.walls_durabilities = [3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        for row in range(10):
            for col in range(10):
                self.tower_battle_grid.grid_layout.itemAtPosition(row, col).widget().clear_state()
                self.tower_battle_grid.grid_layout.itemAtPosition(row, col).widget().adjacent_cells = []

    def place_walls(self, combinations: list):
        for cell in self.flatten_array(combinations):
            self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().is_selected = True
        self.assign_durability()

    def assign_durability(self):
        self.walls_durabilities = [3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        for cell in self.flatten_array(self._selected_combinations):
            durability = random.choice(self.walls_durabilities)
            self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().durability = durability
            self.walls_durabilities.remove(durability)

    def delete_wall(self, game_cell):
        self._selected_combinations.remove(game_cell.adjacent_cells)
        self.combinations[len(game_cell.adjacent_cells)] += 1
        for cell in game_cell.adjacent_cells:
            self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().is_selected = False
            self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().adjacent_cells = []

    def is_destroyed_wall(self, game_cell):
        for cell in game_cell.adjacent_cells:
            a_cell = self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget()
            if not a_cell.is_broken or not a_cell.durability == 0:
                return False
        return True

    def destroy_wall(self, game_cell):
        for cell in game_cell.adjacent_cells:
            self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().is_destroyed = True

    def get_available_combinations(self):
        return [key for key, value in self.combinations.items() if value > 0]

    def check_available_combinations(self):
        return self.get_available_combinations() != []

    def get_max_available_combination(self):
        return max(self.get_available_combinations())

    def combination_constraint(self):
        if self.get_max_available_combination() == len(self.selected_cells) \
                and len(self.selected_cells) in self.get_available_combinations():
            self.is_dragging = False

    def are_cells_close(self, cell: tuple):
        flatten_array = self.flatten_array(self.selected_combinations)
        for c in flatten_array:
            if (cell[1] in (c[1] - 1, c[1], c[1] + 1)) and (cell[0] in (c[0] - 1, c[0], c[0] + 1)):
                return True
        return False


    def flatten_array(self, array: list):
       return [element for sublist in array for element in sublist]
