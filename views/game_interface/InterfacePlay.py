from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QFrame

from widgets.GameInterfaceButton import GameInterfaceButton


class InterfacePlay(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.pause_resume_button = GameInterfaceButton("", "resources/images/icons/pause-64.png")
        self.change_grid_button = GameInterfaceButton("", "resources/images/icons/change-to-enemy-64.png")
        self.timer_label = GameInterfaceButton("")

        self.layout.addWidget(self.pause_resume_button, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.change_grid_button, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.timer_label)

        self.setLayout(self.layout)

