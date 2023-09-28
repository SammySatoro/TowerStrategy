from PyQt6.QtWidgets import QStackedLayout, QFrame

from views.game_interface.InterfaceExitConfirmationLayout import InterfaceExitConfirmationLayout
from views.game_interface.InterfaceGame import InterfaceGame
from views.game_interface.InterfaceLayout import InterfaceLayout


class InterfaceMainFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.exit_confirmation_shown = False

        self.interface_frame = InterfaceLayout()
        self.interface_exit_confirmation_layout = InterfaceExitConfirmationLayout()
        self.interface_game = InterfaceGame()
        self.interface_frame.interface_exit_button.clicked.connect(self.toggle_layout)
        self.interface_exit_confirmation_layout.continue_button.clicked.connect(self.toggle_layout)

        self.stacked_interface_layout = QStackedLayout()
        self.stacked_interface_layout.addWidget(self.interface_game)
        self.stacked_interface_layout.addWidget(self.interface_exit_confirmation_layout)

        self.interface_frame.interface_layout_frame.setLayout(self.stacked_interface_layout)


    def toggle_layout(self):
        self.exit_confirmation_shown = not self.exit_confirmation_shown
        if self.exit_confirmation_shown:
            self.stacked_interface_layout.setCurrentIndex(1)
            self.interface_frame.interface_exit_button.setStyleSheet(
                f"background-image: url({'resources/images/icons/open-door-96.png'});")
        else:
            self.stacked_interface_layout.setCurrentIndex(0)
            self.interface_frame.interface_exit_button.setStyleSheet(
                f"background-image: url({'resources/images/icons/door-closed-96.png'});")