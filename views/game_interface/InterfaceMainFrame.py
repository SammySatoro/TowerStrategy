from PyQt6.QtWidgets import QStackedLayout, QFrame

from views.game_interface.InterfaceExitConfirmationLayout import InterfaceExitConfirmationLayout
from views.game_interface.InterfaceGame import InterfaceGame
from views.game_interface.InterfacePlay import InterfacePlay
from views.game_interface.InterfaceLayout import InterfaceLayout
from controls.python.GameController import GameController

class InterfaceMainFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.exit_confirmation_shown = False
        self.game_controller = GameController()
        self.game_controller.interface_main_frame = self

        self.interface_frame = InterfaceLayout()
        self.interface_exit_confirmation_layout = InterfaceExitConfirmationLayout()
        self.interface_game = InterfaceGame()
        self.interface_play = InterfacePlay()
        self.interface_frame.interface_exit_button.clicked.connect(self.change_layout)
        self.interface_exit_confirmation_layout.continue_button.clicked.connect(self.change_layout)
        self.interface_exit_confirmation_layout.quit_button.clicked.connect(self.change_layout)
        self.interface_game.start_game_button.clicked.connect(self.on_game_started)
        self.interface_play.change_grid_button.clicked.connect(self.game_controller.tower_battle_main_frame.toggle_layout)

        self.game_controller.timer_controller.timer_button = self.interface_play.timer_label
        self.interface_play.pause_resume_button.clicked.connect(self.game_controller.timer_controller.pause_resume_button_click)

        self.stacked_interface_layout = QStackedLayout()
        self.stacked_interface_layout.addWidget(self.interface_game)
        self.stacked_interface_layout.addWidget(self.interface_play)
        self.stacked_interface_layout.addWidget(self.interface_exit_confirmation_layout)

        self.interface_frame.interface_layout_frame.setLayout(self.stacked_interface_layout)


    def on_game_started(self):
        durabilities = self.game_controller.shared_player.walls_durabilities
        if not (3 in durabilities or 2 in durabilities):
            self.stacked_interface_layout.setCurrentIndex(1)

    def change_layout(self):
        self.exit_confirmation_shown = not self.exit_confirmation_shown
        if self.exit_confirmation_shown:
            self.stacked_interface_layout.setCurrentIndex(2)
            self.interface_frame.interface_exit_button.setStyleSheet(
                f"background-image: url({'resources/images/icons/open-door-96.png'});")
        else:
            self.stacked_interface_layout.setCurrentIndex(self.game_controller.game_started)
            self.interface_frame.interface_exit_button.setStyleSheet(
                f"background-image: url({'resources/images/icons/door-closed-96.png'});")