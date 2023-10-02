from PyQt6.QtWidgets import QWidget, QVBoxLayout
from controls.python.StylesheetLoader import StylesheetLoader
from views.game_interface.InterfaceMainFrame import InterfaceMainFrame
from views.game_screen.TowerBattleMainFrame import TowerBattleMainFrame



class GameView(QWidget):
    def __init__(self):
        super().__init__()
        StylesheetLoader(self).load_background_image("resources/images/game_theme.jpg")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.tower_battle_frame = TowerBattleMainFrame()
        self.interface_main_frame = InterfaceMainFrame()

        main_layout.addWidget(self.tower_battle_frame.tower_battle_frame)
        main_layout.addWidget(self.interface_main_frame.interface_frame)

        self.setLayout(main_layout)