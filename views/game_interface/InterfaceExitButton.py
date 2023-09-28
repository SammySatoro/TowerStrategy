from PyQt6.QtWidgets import QPushButton

from controls.python.StylesheetLoader import StylesheetLoader


class InterfaceExitButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.is_clicked = False

        StylesheetLoader(self).load_stylesheet("resources/styles/game.qss")

        self.setObjectName("exitButton")
        self.setFixedSize(50, 88)
