from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel

from controls.python.StylesheetLoader import StylesheetLoader


class GameOverView(QWidget):
    def __init__(self):
        super().__init__()

        StylesheetLoader(self).load_stylesheet("resources/styles/menu.qss")

        main_layout = QVBoxLayout()

        new_continue_frame = QFrame()
        new_continue_frame.setObjectName("newContinueFrame")
        new_continue_container = QVBoxLayout()

        self.game_over_label = QLabel("Game Over")

        new_continue_container.addWidget(self.game_over_label)
        new_continue_frame.setLayout(new_continue_container)
        main_layout.addWidget(new_continue_frame)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.setLayout(main_layout)
