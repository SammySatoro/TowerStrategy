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
        for row in range(10):
            for col in range(10):
                self.tower_battle_grid.grid_layout.itemAtPosition(row, col).widget().is_selected = False
                self.tower_battle_grid.grid_layout.itemAtPosition(row, col).widget().adjacent_cells = []

    def place_walls(self, combinations: list):
        for cell in self.flatten_array(combinations):
            self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().is_selected = True

    def delete_wall(self, game_cell):
        self._selected_combinations.remove(game_cell.adjacent_cells)
        self.combinations[len(game_cell.adjacent_cells)] += 1
        for cell in game_cell.adjacent_cells:
            self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().is_selected = False
            self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().adjacent_cells = []


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

    def are_cell_close(self, cell: tuple):
        flatten_array = self.flatten_array(self.selected_combinations)
        for c in flatten_array:
            if (cell[1] in (c[1] - 1, c[1], c[1] + 1)) and (cell[0] in (c[0] - 1, c[0], c[0] + 1)):
                return True
        return False


    def set_cell_background_color(self, cell, color: str):
        cell.setStyleSheet(f"background-color: {color};")

    def flatten_array(self, array: list):
       return [element for sublist in array for element in sublist]
