from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QMainWindow

from controls.python.OptionsController import OptionsController


class AudioController(QMainWindow):
    def __init__(self, audio_file: str, audio_type: str):
        super().__init__()

        options_controller = OptionsController()
        if audio_type == "music":
            options_controller.music_players.append(self)
            self.volume = OptionsController().current_music_volume
        elif audio_type == "sound":
            options_controller.sound_players.append(self)
            self.volume = OptionsController().current_sound_volume

        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setSource(QUrl.fromLocalFile(audio_file))
        self.audio_output.setVolume(self.volume)

    def set_volume(self, value: float):
        self.volume = value
        self.audio_output.setVolume(self.volume)

    def play_audio_looped(self):
        self.media_player.mediaStatusChanged.connect(self.handle_media_status)
        self.media_player.play()

    def play_audio(self):
        self.media_player.play()

    def handle_media_status(self, status):
        if status == self.media_player.mediaStatus():
            # Restart the media playback when it reaches the end
            self.media_player.setPosition(0)
            self.media_player.play()