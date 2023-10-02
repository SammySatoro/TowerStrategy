from PyQt6.QtWidgets import QStackedLayout, QFrame, QPushButton

from views.game_interface.SharedVariables import SharedVariablesManager
from views.game_screen.TowerBattleGrid import TowerBattleGrid
from views.game_screen.TowerBattleLayout import TowerBattleLayout


class TowerBattleMainFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.shared_player = SharedVariablesManager().shared_variables_player
        self.shared_enemy = SharedVariablesManager().shared_variables_enemy

        self.enemy_grid_shown = False

        self.tower_battle_frame = TowerBattleLayout()
        self.tower_battle_grid_player = TowerBattleGrid()
        self.tower_battle_grid_player.setObjectName("towerBattleGridPlayer")
        self.shared_player.tower_battle_grid = self.tower_battle_grid_player
        self.tower_battle_grid_enemy = TowerBattleGrid()
        self.tower_battle_grid_enemy.setObjectName("towerBattleGridEnemy")
        self.shared_enemy.tower_battle_grid = self.tower_battle_grid_enemy

        self.toggle_grid_button = QPushButton("TOGGLE")
        self.toggle_grid_button.clicked.connect(self.toggle_layout)

        self.stacked_tower_battle_layout = QStackedLayout()
        self.stacked_tower_battle_layout.addWidget(self.tower_battle_grid_player)
        self.stacked_tower_battle_layout.addWidget(self.tower_battle_grid_enemy)

        self.tower_battle_frame.tower_battle_layout_frame.setLayout(self.stacked_tower_battle_layout)
        self.tower_battle_frame.layout.addWidget(self.toggle_grid_button)

    def toggle_layout(self):
        self.enemy_grid_shown = not self.enemy_grid_shown
        if self.enemy_grid_shown:
            self.stacked_tower_battle_layout.setCurrentIndex(1)
        else:
            self.stacked_tower_battle_layout.setCurrentIndex(0)