from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel

from views.ExitConfirmationView import ExitConfirmationView
from controls.python.StylesheetLoader import StylesheetLoader
from widgets.MenuButton import MenuButton


class MainMenuView(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        StylesheetLoader(self).load_stylesheet("resources/styles/menu.qss")
        StylesheetLoader(self).load_background_image("resources/images/menu_theme.jpg")

        main_layout = QVBoxLayout()

        menu_buttons_container = QFrame()
        menu_buttons_container.setObjectName("menuButtonsContainer")

        # Create a QVBoxLayout for the container
        container_layout = QVBoxLayout()

        # Create Play, Options, and Exit buttons
        self.play_button = MenuButton("Play")
        self.options_button = MenuButton("Options")
        self.exit_button = MenuButton("Exit")
        self.exit_button.clicked.connect(self.show_exit_confirmation)

        # Add buttons to the container's layout
        container_layout.addWidget(self.play_button)
        container_layout.addWidget(self.options_button)
        container_layout.addWidget(self.exit_button)

        # Set the container's layout
        menu_buttons_container.setLayout(container_layout)

        # Add the menu_buttons_container to main_layout and set alignment
        main_layout.addWidget(menu_buttons_container)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)

        self.setLayout(main_layout)


    def show_exit_confirmation(self):
        self.exit_confirmation = ExitConfirmationView()
