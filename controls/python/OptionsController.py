from controls.python.JSONController import JSONController
import os

class OptionsControllerMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class OptionsController(metaclass=OptionsControllerMeta):

    def __init__(self):
        self.options_file = JSONController.get_absolute_path_to_config_json("options.json")

        self.current_music_volume = 0.25
        self.current_sound_volume = 0.25
        self.music_players = []
        self.sound_players = []

    def set_music_volume(self, volume):
        if self.music_players != []:
            for audio in self.music_players:
                audio.set_volume(volume)

    def set_sound_volume(self, volume):
        if self.sound_players != []:
            for audio in self.sound_players:
                audio.set_volume(volume)

    def on_music_volume_changed(self, position):
        self.set_music_volume(position)
        self.current_music_volume = position

    def on_sound_volume_changed(self, position):
        self.set_sound_volume(position)
        self.current_sound_volume = position

    def save_options(self):
        options = {"music_volume": self.current_music_volume, "sound_volume": self.current_sound_volume}
        JSONController().save_data_to_json(options, self.options_file)

    def load_options(self):
        options: dict = JSONController().load_data_from_json(self.options_file)
        self.current_music_volume = float(options.get("music_volume", 0.25))
        self.current_sound_volume = float(options.get("sound_volume", 0.25))
        self.set_music_volume(self.current_music_volume)
        self.set_sound_volume(self.current_sound_volume)