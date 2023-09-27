from PyQt6.QtCore import QFile, QIODevice, QTextStream
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class StylesheetLoader():
    def __init__(self, layout):
        super().__init__()

        self.layout = layout

    def load_stylesheet(self, stylesheet_path: str):
        # Load the CSS style sheet
        style_sheet_file = QFile(stylesheet_path)
        if style_sheet_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            style_sheet = QTextStream(style_sheet_file).readAll()
            self.layout.setStyleSheet(style_sheet)

    def load_background_image(self, image_path: str):
        background_label = QLabel(self.layout)
        pixmap = QPixmap(image_path)
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, 640, 480)