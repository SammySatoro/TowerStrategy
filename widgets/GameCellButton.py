from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton

from controls.python.GameController import GameController
from controls.python.StylesheetLoader import StylesheetLoader


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
        self._durability = -1

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
            self.durability = 0
            self.setText("")

    @property
    def durability(self):
        return self._durability

    @durability.setter
    def durability(self, value):
        self._durability = value
        if self.is_selected:
            if not self.is_enemy:
                self.setText(str(self.durability))
            if self._durability == 0:
                cells_count = len(self.adjacent_cells)
                for cell in self.adjacent_cells:
                    if self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().durability == 0:
                        cells_count -= 1
                if cells_count == 0:
                    self.game_controller.in_focus = False
                    for cell in self.adjacent_cells:
                        self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().durability = -1
                        cells_to_destroy = self.game_controller.prolog_controller.pull_query(f"get_close_cells({[cell[0], cell[1]]}, X)")[0]['X']
                        for ctd in cells_to_destroy:
                            self.tower_battle_grid.grid_layout.itemAtPosition(ctd[1], ctd[0]).widget().durability = -1
        if self._durability == -1:
            if not self.game_controller.enemy_turn:
                if [self.x, self.y] in self.game_controller.shared_enemy.cells:
                    self.game_controller.shared_enemy.cells.remove([self.x, self.y])
                else:
                    if [self.x, self.y] in self.game_controller.shared_player.cells:
                        self.game_controller.shared_player.cells.remove([self.x, self.y])
            self.is_destroyed = True

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
        if value:
            self.setText("")
        if self.is_selected:
            self.set_background_color(f"black" if value else f"#D7CAC2")
        else:
            self.set_background_color(f"blue" if value else f"#D7CAC2")

    def mousePressEvent(self, event):
        if not self.is_enemy:
            if not self.game_controller.game_started:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.game_controller.shared_player.is_dragging = True
                if event.button() == Qt.MouseButton.RightButton:
                    if self.is_selected:
                        self.game_controller.shared_player.delete_wall(self)
        else:
            if not self.game_controller.enemy_turn and event.button() == Qt.MouseButton.LeftButton:
                if not self.is_destroyed:
                    if self.is_selected:
                        self.game_controller.in_focus = True
                        self.is_broken = True
                        self.durability -= 1
                        if self.durability == -1:
                            self.setText(str(""))
                        else:
                            self.setText(str(self.durability))
                        if self.is_broken and self.game_controller.shared_enemy.is_destroyed_wall(self):
                            self.game_controller.shared_enemy.destroy_wall(self)
                    else:
                        self.set_background_color("blue")
                    self.game_controller.timer_controller.switch_turn()

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
            "is_enemy": self.is_enemy,
            "durability": self.durability
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
        self.durability = data["durability"]

    def clear_state(self):
        self.is_selected = False
        self.is_broken = False
        self.is_destroyed = False

    def on_shot(self):
        if not self.is_enemy:
            pass
