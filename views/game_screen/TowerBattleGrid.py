from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QFrame

from controls.python.StylesheetLoader import StylesheetLoader
from views.game_interface.SharedVariables import SharedVariablesManager
from widgets.GameCellButton import GameCellButton


class TowerBattleGrid(QFrame):
    def __init__(self):
        super().__init__()

        self.shared_player = SharedVariablesManager().shared_variables_player

        StylesheetLoader(self).load_stylesheet("resources/styles/game.qss")

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)


        for row in range(10):
            for col in range(10):
                cell_button = GameCellButton(self, "", col, row)
                cell_button.setObjectName("cellButton")
                cell_button.setFixedSize(36, 36)
                self.grid_layout.addWidget(cell_button, row, col)

        self.setLayout(self.grid_layout)

    def get_cells_data(self):
        cells_data = []
        for row in range(10):
            for column in range(10):
                cells_data.append(self.grid_layout.itemAtPosition(row, column).widget().get_data())
        return cells_data

    def mouseMoveEvent(self, event):
        if self.shared_player.check_available_combinations() and self.shared_player.is_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            child = self.childAt(event.pos())
            if isinstance(child, GameCellButton) and not child.is_selected:
                cellXY = (child.x, child.y)
                if cellXY not in self.shared_player.selected_cells:
                    if self.shared_player.are_cell_close(cellXY):
                        for cell in self.shared_player.selected_cells:
                            self.grid_layout.itemAtPosition(cell[1], cell[0]).widget().is_selected = False
                            self.grid_layout.itemAtPosition(cell[1], cell[0]).widget().adjacent_cells = []
                        self.shared_player.selected_cells = []
                    else:
                        self.shared_player.selected_cells.append(cellXY)
                        child.is_selected = True
                        child.adjacent_cells = self.shared_player.selected_cells
                self.shared_player.combination_constraint()