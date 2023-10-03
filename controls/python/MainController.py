from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from controls.python.AudioController import AudioController
from controls.python.OptionsController import OptionsController
from views.ExitConfirmationView import ExitConfirmationView
from views.GameLoadView import GameLoadView
from views.MainMenuView import MainMenuView
from views.OptionsView import OptionsView
from views.GameView import GameView
from controls.python.GameController import GameController


class MainController(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)

        self.setWindowTitle("Tower Strategy")
        self.setFixedSize(640, 480)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.options_controller = OptionsController()
        self.options_controller.load_options()

        self.menu_page = MainMenuView()
        self.game_page = GameView()
        self.options_page = OptionsView()
        self.exit_confirmation_page = ExitConfirmationView()
        self.game_load_page = GameLoadView()

        self.central_widget.addWidget(self.menu_page)
        self.central_widget.addWidget(self.game_load_page)
        self.central_widget.addWidget(self.game_page)
        self.central_widget.addWidget(self.options_page)
        self.central_widget.addWidget(self.exit_confirmation_page)


        self.menu_page.exit_button.clicked.connect(self.goto_exit_confirmation)
        self.menu_page.options_button.clicked.connect(self.goto_options)
        self.menu_page.play_button.clicked.connect(self.goto_game_load)
        self.options_page.back_button.clicked.connect(self.goto_main_menu)
        self.exit_confirmation_page.no_button.clicked.connect(self.goto_main_menu)
        self.game_load_page.new_game_button.clicked.connect(self.goto_new_game)
        self.game_load_page.continue_button.clicked.connect(self.goto_continue_game_page)
        self.game_page.interface_main_frame.interface_exit_confirmation_layout.quit_button.clicked.connect(self.goto_main_menu)



        self.central_widget.setCurrentWidget(self.menu_page)

        self.audio_controller = AudioController("resources/audio/music/menu_theme.wav", "music")
        self.audio_controller.play_audio_looped()

    def goto_main_menu(self):
        self.options_controller.save_options()
        self.central_widget.setCurrentWidget(self.menu_page)

    def goto_options(self):
        self.central_widget.setCurrentWidget(self.options_page)

    def goto_game_load(self):
        self.central_widget.setCurrentWidget(self.game_load_page)

    def goto_new_game(self):
        self._set_new_game_page()
        self.central_widget.setCurrentWidget(self.game_page)

    def _set_new_game_page(self):
        GameController().start_new_game()

    def goto_continue_game_page(self):
        self.central_widget.setCurrentWidget(self.game_page)

    def goto_exit_confirmation(self):
        self.central_widget.setCurrentWidget(self.exit_confirmation_page)

