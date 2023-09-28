from PyQt6.QtWidgets import QStackedLayout, QFrame

from views.game_interface.SharedVariables import SharedVariablesManager
from views.game_screen.TowerBattleGrid import TowerBattleGrid
from views.game_screen.TowerBattleLayout import TowerBattleLayout


class TowerBattleMainFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.shared_player = SharedVariablesManager().shared_variables_player

        self.exit_confirmation_shown = False

        self.tower_battle_frame = TowerBattleLayout()
        self.tower_battle_grid_player = TowerBattleGrid()
        self.shared_player.tower_battle_grid = self.tower_battle_grid_player
        self.tower_battle_grid_enemy = TowerBattleGrid()

        self.stacked_tower_battle_layout = QStackedLayout()
        self.stacked_tower_battle_layout.addWidget(self.tower_battle_grid_player)
        self.stacked_tower_battle_layout.addWidget(self.tower_battle_grid_enemy)

        self.tower_battle_frame.tower_battle_layout_frame.setLayout(self.stacked_tower_battle_layout)


    # def toggle_layout(self):
    #     self.exit_confirmation_shown = not self.exit_confirmation_shown
    #     if self.exit_confirmation_shown:
    #         self.stacked_interface_layout.setCurrentIndex(1)
    #         self.interface_frame.interface_exit_button.setStyleSheet(
    #             f"background-image: url({'resources/images/icons/open-door-96.png'});")
    #     else:
    #         self.stacked_interface_layout.setCurrentIndex(0)
    #         self.interface_frame.interface_exit_button.setStyleSheet(
    #             f"background-image: url({'resources/images/icons/door-closed-96.png'});")