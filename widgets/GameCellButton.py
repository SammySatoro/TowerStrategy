from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton

from controls.python.GameController import GameController
from controls.python.StylesheetLoader import StylesheetLoader
from views.game_interface.SharedVariables import SharedVariablesManager


class GameCellButton(QPushButton):
    def __init__(self, tower_battle_grid, text, x, y, parent=None):
        super().__init__(text, parent)

        self.game_controller = GameController()

        self.tower_battle_grid = tower_battle_grid
        self.x = x
        self.y = y
        self.adjacent_cells = []
        self._is_selected = False
        self._is_broken = False
        self._is_destroyed = False
        self.is_enemy = False
        self.durability = 0

        StylesheetLoader(self).load_stylesheet("resources/styles/game.qss")

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value):
        self._is_selected = value
        if value:
            self.set_background_color(f"#D7CAC2" if self.is_enemy else f"green")
        else:
            self.set_background_color(f"#D7CAC2")

    @property
    def is_broken(self):
        return self._is_broken

    @is_broken.setter
    def is_broken(self, value):
        self._is_broken = value
        self.set_background_color(f"yellow" if value else f"#D7CAC2")

    @property
    def is_destroyed(self):
        return self._is_destroyed

    @is_destroyed.setter
    def is_destroyed(self, value):
        self._is_destroyed = value
        self.set_background_color(f"black" if value else f"#D7CAC2")

    def mousePressEvent(self, event):
        if not self.is_enemy:
            if event.button() == Qt.MouseButton.LeftButton:
                self.game_controller.shared_player.is_dragging = True
            if event.button() == Qt.MouseButton.RightButton:
                if self.is_selected:
                    self.game_controller.shared_player.delete_wall(self)
        else:
            if event.button() == Qt.MouseButton.LeftButton:
                if self.is_selected:
                    self.is_broken = True
                    if self.is_broken and self.game_controller.shared_enemy.is_destroyed_wall(self):
                        self.game_controller.shared_enemy.destroy_wall(self)
                else:
                    self.set_background_color("blue")

    def mouseReleaseEvent(self, event):
        if len(self.game_controller.shared_player.selected_cells) > 0:
            if self.game_controller.shared_player.combinations[len(self.game_controller.shared_player.selected_cells)] > 0:
                self.game_controller.shared_player.combinations[len(self.game_controller.shared_player.selected_cells)] -= 1
                self.game_controller.shared_player.selected_combinations.append(self.game_controller.shared_player.selected_cells)
                self.game_controller.shared_player.selected_cells = []
            else:
                for cell in self.game_controller.shared_player.selected_cells:
                    self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().is_selected = False
                self.game_controller.shared_player.selected_cells = []

    def set_background_color(self, color: str):
        self.setStyleSheet(f"background-color: {color};")

    def get_data(self):
        data = {
            "x": self.x,
            "y": self.y,
            "adjacent_cells": self.adjacent_cells,
            "is_selected": self.is_selected,
            "is_broken": self.is_broken,
            "is_destroyed": self.is_destroyed,
            "is_enemy": self.is_enemy
        }
        return data

    def set_data(self, data):
        self.x = data["x"]
        self.y = data["y"]
        self.adjacent_cells = data["adjacent_cells"]
        self.is_selected = data["is_selected"]
        self.is_broken = data["is_broken"]
        self.is_destroyed = data["is_destroyed"]
        self.is_enemy = data["is_enemy"]

    def clear_state(self):
        self.is_selected = False
        self.is_broken = False
        self.is_destroyed = False