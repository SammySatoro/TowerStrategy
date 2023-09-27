from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame

from controls.python.GameController import GameController
from controls.python.StylesheetLoader import StylesheetLoader
from widgets.MenuButton import MenuButton


class GameLoadView(QWidget):
    def __init__(self):
        super().__init__()

        StylesheetLoader(self).load_stylesheet("resources/styles/menu.qss")
        StylesheetLoader(self).load_background_image("resources/images/menu_theme.jpg")

        main_layout = QVBoxLayout()

        new_continue_frame = QFrame()
        new_continue_frame.setObjectName("newContinueFrame")
        new_continue_container = QVBoxLayout()

        self.new_game_button = MenuButton("New Game")
        self.continue_button = MenuButton("Continue")

        new_continue_container.addWidget(self.new_game_button)
        new_continue_container.addWidget(self.continue_button)
        new_continue_frame.setLayout(new_continue_container)
        main_layout.addWidget(new_continue_frame)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.setLayout(main_layout)
