from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QFrame, QWidget

from controls.python.StylesheetLoader import StylesheetLoader
from widgets.Color import Color
from widgets.MenuButton import MenuButton


class InterfaceExitConfirmationLayout(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.quit_button = MenuButton("Quit")
        self.quit_button.setObjectName("quitButton")
        self.continue_button = MenuButton("Continue")
        self.continue_button.setObjectName("continueButton")

        self.layout.addWidget(self.continue_button)
        self.layout.addWidget(self.quit_button)

        self.setLayout(self.layout)