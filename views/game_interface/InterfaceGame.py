from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QFrame

from controls.python.GameController import GameController
from controls.python.RandomWallsGenerator import RandomWallsGenerator
from views.game_interface.SharedVariables import SharedVariablesManager
from widgets.GameInterfaceButton import GameInterfaceButton


class InterfaceGame(QFrame):
    def __init__(self):
        super().__init__()
        self.shared_player = SharedVariablesManager().shared_variables_player
        self.game_controller = GameController()
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.start_game_button = GameInterfaceButton("", "resources/images/icons/play-64.png")
        self.random_walls_button = GameInterfaceButton("", "resources/images/icons/random-64.png")
        self.clear_walls_button = GameInterfaceButton("", "resources/images/icons/clear-64.png")
        self.start_game_button.clicked.connect(self.game_controller.save_game)
        self.random_walls_button.clicked.connect(self.place_random_walls)
        self.clear_walls_button.clicked.connect(self.clear_walls)

        self.layout.addWidget(self.start_game_button, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.random_walls_button, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.clear_walls_button, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)


    def start_new_game(self):
        self.shared_player.game_controller.start_game()

    def place_random_walls(self):
        random_walls_generator = RandomWallsGenerator()
        random_walls_generator.generate()
        self.shared_player.selected_combinations = random_walls_generator.get_all_wall_coordinates()

    def clear_walls(self):
        self.shared_player.clear_grid()
