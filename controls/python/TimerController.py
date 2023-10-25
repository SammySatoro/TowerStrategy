from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QPushButton


class TimerControllerMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TimerController(metaclass=TimerControllerMeta):
    def __init__(self):
        self._move_duration = {
            True: 2,
            False: 10
        }
        self._game_start_duration = 3
        self._current_time = 3

        self.timer = QTimer()
        self._duration = 1000
        self.timer_button = QPushButton()
        self.game_controller = None
        self.timer.timeout.connect(self.on_timeout)

    def start_timer(self):
        self.timer_button.setText(str(self._current_time))
        self.timer.start(self._duration)

    def on_timeout(self):
        if self._game_start_duration > -1:
            self._game_start_duration -= 1
            self.timer_button.setText(str(self._game_start_duration))
        if self._game_start_duration <= -1:
            self._process_move_countdown()


    def _process_move_countdown(self):
        self._current_time = self._move_duration[self.game_controller.enemy_turn]
        self._move_duration[self.game_controller.enemy_turn] -= 1
        self.timer_button.setText(str(self._current_time))
        if self.game_controller.enemy_turn and self._move_duration[self.game_controller.enemy_turn] == 0:
            self.game_controller.enemy_shoot()
        if self._move_duration[self.game_controller.enemy_turn] <= -1:
            self.switch_turn()

    def switch_turn(self):
        if self.game_controller.enemy_turn:
            self._move_duration[self.game_controller.enemy_turn] = 2
        else:
            self._move_duration[self.game_controller.enemy_turn] = 10
        self.game_controller.enemy_turn = not self.game_controller.enemy_turn


    def pause_resume_button_click(self):
        if self.game_controller.is_paused:
            self.resume()
        else:
            self.pause()

    def pause(self):
        self.game_controller.interface_main_frame.interface_play.pause_resume_button.set_icon(
            "resources/images/icons/resume-64.png")
        self.game_controller.is_paused = not self.game_controller.is_paused
        self.timer.stop()

    def resume(self):
        self.game_controller.interface_main_frame.interface_play.pause_resume_button.set_icon(
            "resources/images/icons/pause-64.png")
        self.game_controller.is_paused = not self.game_controller.is_paused
        self.start_timer()

    def stop_main_timer(self):
        self.timer.stop()

    def set_widget_text(self, text: str):
        self.timer_button.setText(text)

    def reset(self):
        self.timer.stop()
        self._move_duration = {
                True: 2,
                False: 10
            }
        self._game_start_duration = 3
        self._current_time = 3
        self.timer_button.setText(str(self._current_time))