from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QFrame

from controls.python.StylesheetLoader import StylesheetLoader


class TowerBattleLayout(QFrame):
    def __init__(self,  parent=None):
        super().__init__(parent)

        StylesheetLoader(self).load_stylesheet("resources/styles/game.qss")

        self.setObjectName("towerBattleLayout")
        self.setFixedSize(640, 380)
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.tower_battle_layout_frame = QFrame()
        self.tower_battle_layout_frame.setFixedSize(360, 360)
        self.tower_battle_layout_frame.setObjectName("towerBattleLayoutFrame")
        self.layout.addWidget(self.tower_battle_layout_frame, Qt.AlignmentFlag.AlignCenter)



        self.setLayout(self.layout)
