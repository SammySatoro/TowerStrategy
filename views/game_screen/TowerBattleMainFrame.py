from PyQt6.QtWidgets import QStackedLayout, QFrame

from controls.python.GameController import GameController
from views.game_screen.TowerBattleGrid import TowerBattleGrid
from views.game_screen.TowerBattleLayout import TowerBattleLayout


class TowerBattleMainFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.game_controller = GameController()
        self.game_controller.tower_battle_main_frame = self
        self.enemy_grid_shown = False

        self.tower_battle_frame = TowerBattleLayout()
        self.tower_battle_grid_player = TowerBattleGrid()
        self.tower_battle_grid_player.setObjectName("towerBattleGridPlayer")
        self.game_controller.shared_player.tower_battle_grid = self.tower_battle_grid_player
        self.tower_battle_grid_enemy = TowerBattleGrid(is_enemy=True)
        self.tower_battle_grid_enemy.setObjectName("towerBattleGridEnemy")
        self.game_controller.shared_enemy.tower_battle_grid = self.tower_battle_grid_enemy

        self.stacked_tower_battle_layout = QStackedLayout()
        self.stacked_tower_battle_layout.addWidget(self.tower_battle_grid_player)
        self.stacked_tower_battle_layout.addWidget(self.tower_battle_grid_enemy)

        self.tower_battle_frame.tower_battle_layout_frame.setLayout(self.stacked_tower_battle_layout)

    def toggle_layout(self):
        self.enemy_grid_shown = not self.enemy_grid_shown
        if self.enemy_grid_shown:
            self.stacked_tower_battle_layout.setCurrentIndex(1)
            self.game_controller.interface_main_frame.interface_play.change_grid_button.set_icon(
                "resources/images/icons/change-to-player-64.png")
        else:
            self.stacked_tower_battle_layout.setCurrentIndex(0)
            self.game_controller.interface_main_frame.interface_play.change_grid_button.set_icon(
                "resources/images/icons/change-to-enemy-64.png")