from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QFrame

from controls.python.OptionsController import OptionsController
from controls.python.StylesheetLoader import StylesheetLoader
from widgets.MenuButton import MenuButton


class OptionsView(QWidget):
    def __init__(self):
        super().__init__()

        StylesheetLoader(self).load_stylesheet("resources/styles/options.qss")
        StylesheetLoader(self).load_background_image("resources/images/menu_theme.jpg")

        self.main_layout = QVBoxLayout()
        self.top_layout = QHBoxLayout()

        self.back_button = MenuButton("Back")
        self.top_layout.addWidget(self.back_button,
                             alignment=Qt.AlignmentFlag.AlignLeft & Qt.AlignmentFlag.AlignTop)  # Move the "Back" button to the top-left corner

        self.main_layout.addLayout(self.top_layout)

        # Add three horizontal sliders to the center
        self.music_volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.music_volume_label = QLabel(f"Music: ${OptionsController().current_music_volume * 100:.0f}")
        self.music_volume_slider.valueChanged.connect(self.change_music_volume_value)
        self.music_volume_slider.setValue(int(OptionsController().current_music_volume * 100))


        self.sounds_volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.sounds_volume_label = QLabel(f"Sound: {OptionsController().current_sound_volume * 100:.0f}")
        self.sounds_volume_slider.valueChanged.connect(self.change_sound_volume_value)
        self.sounds_volume_slider.setValue(int(OptionsController().current_sound_volume * 100))



        self.center_layout = QVBoxLayout()
        self.center_layout.addWidget(self.music_volume_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.center_layout.addWidget(self.music_volume_slider)
        self.center_layout.addWidget(self.sounds_volume_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.center_layout.addWidget(self.sounds_volume_slider)

        self.container_frame = QFrame()
        self.container_frame.setFixedSize(300, 150)
        self.container_frame.setObjectName("containerFrame")
        self.container_frame.setLayout(self.center_layout)

        self.main_layout.addWidget(self.container_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.main_layout)

    def change_sound_volume_value(self):
        self.sounds_volume_label.setText(f"Sound: {self.sounds_volume_slider.value():.0f}")
        OptionsController().on_sound_volume_changed(self.sounds_volume_slider.value() / 100)

    def change_music_volume_value(self):
        self.music_volume_label.setText(f"Music: {self.music_volume_slider.value():.0f}")
        OptionsController().on_music_volume_changed(self.music_volume_slider.value() / 100)