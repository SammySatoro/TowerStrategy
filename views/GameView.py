from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QFrame

from controls.python.StylesheetLoader import StylesheetLoader
from views.game_interface.InterfaceExitConfirmationLayout import InterfaceExitConfirmationLayout
from views.game_interface.InterfaceGame import InterfaceGame
from views.game_interface.InterfaceLayout import InterfaceLayout
from widgets.Color import Color


class GameView(QWidget):
    def __init__(self):
        super().__init__()

        self.exit_confirmation_shown = False

        StylesheetLoader(self).load_stylesheet("resources/styles/game.qss")
        StylesheetLoader(self).load_background_image("resources/images/game_theme.jpg")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        game_screen_frame = QFrame()
        game_screen_frame.setObjectName("gameScreenFrame")
        game_screen_layout = QVBoxLayout()
        game_screen_layout.setSpacing(0)
        game_screen_layout.setContentsMargins(0, 0, 0, 0)
        game_screen_layout.addWidget(Color("transparent"))

        self.interface_frame = InterfaceLayout()

        self.interface_frame.interface_exit_button.clicked.connect(self.toggle_layout)
        self.interface_exit_confirmation_layout = InterfaceExitConfirmationLayout()
        self.interface_game = InterfaceGame()

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.interface_game)
        self.stacked_layout.addWidget(self.interface_exit_confirmation_layout)

        self.interface_frame.interface_layout_frame.setLayout(self.stacked_layout)

        game_screen_frame.setLayout(game_screen_layout)
        main_layout.addWidget(game_screen_frame)
        main_layout.addWidget(self.interface_frame)

        self.setLayout(main_layout)

    def toggle_layout(self):
        self.exit_confirmation_shown = not self.exit_confirmation_shown
        if self.exit_confirmation_shown:
            self.stacked_layout.setCurrentIndex(1)
            self.interface_frame.interface_exit_button.setStyleSheet(
                f"background-image: url({'resources/images/icons/open-door-96.png'});")
        else:
            self.stacked_layout.setCurrentIndex(0)
            self.interface_frame.interface_exit_button.setStyleSheet(
                f"background-image: url({'resources/images/icons/door-closed-96.png'});")