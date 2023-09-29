from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QFrame

from controls.python.RandomWallsGenerator import RandomWallsGenerator
from views.game_interface.SharedVariables import SharedVariablesManager
from widgets.GameInterfaceButton import GameInterfaceButton


class InterfaceGame(QFrame):
    def __init__(self):
        super().__init__()
        self.shared_player = SharedVariablesManager().shared_variables_player
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.start_game_button = GameInterfaceButton("", "resources/images/icons/play-64.png")
        self.random_walls_button = GameInterfaceButton("", "resources/images/icons/random-64.png")
        self.clear_walls_button = GameInterfaceButton("", "resources/images/icons/clear-64.png")
        self.random_walls_button.clicked.connect(self.place_random_walls)
        self.clear_walls_button.clicked.connect(self.clear_walls)

        self.layout.addWidget(self.start_game_button, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.random_walls_button, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.clear_walls_button, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def place_random_walls(self):
        random_walls_generator = RandomWallsGenerator()
        random_walls_generator.generate()
        self.shared_player.selected_combinations = random_walls_generator.get_all_wall_coordinates()

    def clear_walls(self):
        self.shared_player.clear_grid()


        # for row in range(10):
        #     for col in range(10):
        #         self.shared_player.tower_battle_grid.grid_layout.itemAtPosition(row, col).widget().is_selected = False

        # for cell in coords:
        #     self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().is_selected = True
