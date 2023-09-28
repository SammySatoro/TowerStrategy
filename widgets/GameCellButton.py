from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton
from controls.python.StylesheetLoader import StylesheetLoader
from views.game_interface.SharedVariables import SharedVariables, SharedVariablesManager


class GameCellButton(QPushButton):
    def __init__(self, tower_battle_grid, text, x, y, parent=None):
        super().__init__(text, parent)

        self.shared_player = SharedVariablesManager().shared_variables_player

        self.tower_battle_grid = tower_battle_grid
        self.x = x
        self.y = y
        self.adjacent_cells = []
        self._is_selected = False
        self.is_built = False
        self.is_destroyed = False

        StylesheetLoader(self).load_stylesheet("resources/styles/game.qss")

    @property
    def is_selected(self):
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value):
        self._is_selected = value
        if value:
            self.setStyleSheet(f"background-color: green;")
        else:
            self.setStyleSheet(f"background-color: #D7CAC2;")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.shared_player.is_dragging = True
        if event.button() == Qt.MouseButton.RightButton:
            if self.is_selected:
                self.shared_player.delete_wall(self)


    def mouseReleaseEvent(self, event):
        if len(self.shared_player.selected_cells) > 0:
            if self.shared_player.combinations[len(self.shared_player.selected_cells)] > 0:
                self.shared_player.combinations[len(self.shared_player.selected_cells)] -= 1
                self.shared_player.selected_combinations.append(self.shared_player.selected_cells)
                self.shared_player.selected_cells = []
            else:
                for cell in self.shared_player.selected_cells:
                    self.tower_battle_grid.grid_layout.itemAtPosition(cell[1], cell[0]).widget().is_selected = False
                self.shared_player.selected_cells = []



