from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QWidget, QApplication, QFrame

from controls.python.StylesheetLoader import StylesheetLoader
from widgets.MenuButton import MenuButton


class ExitConfirmationView(QWidget):
    def __init__(self):
        super().__init__()

        StylesheetLoader(self).load_stylesheet("resources/styles/exit_confirmation.qss")
        StylesheetLoader(self).load_background_image("resources/images/menu_theme.jpg")

        main_layout = QVBoxLayout()

        message_label = QLabel("Are you sure?")

        self.yes_button = MenuButton("Yes")
        self.no_button = MenuButton("No")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.yes_button, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.no_button, alignment=Qt.AlignmentFlag.AlignCenter)

        container_frame = QFrame()
        container_frame.setObjectName("containerFrame")

        layout = QVBoxLayout()
        layout.addWidget(message_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(button_layout)

        container_frame.setLayout(layout)
        main_layout.addWidget(container_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        self.yes_button.clicked.connect(self.accept_exit)
        self.no_button.clicked.connect(self.close)


    def accept_exit(self):
        QApplication.exit()
