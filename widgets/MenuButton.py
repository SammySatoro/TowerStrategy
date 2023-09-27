from PyQt6.QtWidgets import QPushButton

from controls.python.AudioController import AudioController
from controls.python.OptionsController import OptionsController
from controls.python.StylesheetLoader import StylesheetLoader


class MenuButton(QPushButton):
    def __init__(self, text, stylesheet: str = None, parent=None):
        super().__init__(text, parent)

        if stylesheet is not None:
            self.stylesheet = stylesheet
        else:
            self.stylesheet = "resources/styles/menu_button.qss"

        StylesheetLoader(self).load_stylesheet(self.stylesheet)

        self.audio_controller = AudioController("resources/audio/sounds/menu_button_focus.wav", "sound")
        self.audio_controller2 = AudioController("resources/audio/sounds/menu_button_click.wav", "sound")
        self.audio_controller.deleteLater()
        self.audio_controller2.deleteLater()
        self.sound_played = False  # Flag to track if sound has been played
        self.clicked.connect(self.on_click)

    def enterEvent(self, e):
        if not self.sound_played:
            self.audio_controller.play_audio()
            self.sound_played = True

    def leaveEvent(self, e):
        self.sound_played = False

    def on_click(self):
        self.audio_controller2.play_audio()