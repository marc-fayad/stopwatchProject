from PyQt6.QtWidgets import *
from view import *
import sys


def ui_quit():
    sys.exit()


class Controller(QMainWindow, Ui_Stopwatch):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.start_button.clicked.connect(lambda: self.start())
        self.reset_button.clicked.connect(lambda: self.reset())
        self.quit_button.clicked.connect(lambda: ui_quit())
        self.lap_button.clicked.connect(lambda: self.lap())

        self.running = False
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.milliseconds = 0

        self.millisecondsString = ''
        self.secondsString = ''
        self.minutesString = ''
        self.hoursString = ''

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.time_change)

        self.lap_hours = 0
        self.lap_minutes = 0
        self.lap_seconds = 0
        self.lap_milliseconds = 0

        self.lap_count = 0

        self.lap_millisecondsString = ''
        self.lap_secondsString = ''
        self.lap_minutesString = ''
        self.lap_hoursString = ''

        self.lapTimer = QtCore.QTimer(self)
        self.lapTimer.timeout.connect(self.lap_time_change)

    def start(self):
        if not self.running:
            self.running = True
            self.time_change()
            self.lap_time_change()
            self.start_button.setText('Pause')

        else:
            self.running = False
            self.start_button.setText('Start')

    def reset(self):
        self.running = False
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.time_label.setText('00:00:00.00')
        self.lap1.setText('')
        self.lap2.setText('')
        self.lap3.setText('')
        self.lap4.setText('')
        self.lap_reset()
        self.lap_count = 0
        self.start_button.setText('Start')

    def time_change(self):
        if self.running:
            self.timer.start(10)
            self.milliseconds += 1
            if self.milliseconds == 100:
                self.seconds += 1
                self.milliseconds = 0
            if self.seconds == 60:
                self.minutes += 1
                self.seconds = 0
            if self.minutes == 60:
                self.hours += 1
                self.minutes = 0

            self.millisecondsString = f'{self.milliseconds}' if self.milliseconds > 9 else f'0{self.milliseconds}'
            self.secondsString = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
            self.minutesString = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
            self.hoursString = f'{self.hours}' if self.hours > 9 else f'0{self.hours}'

            self.time_label.setText(f'{self.hoursString}:{self.minutesString}:{self.secondsString}.'
                                    f'{self.millisecondsString}')

    def lap(self):
        if self.running:
            self.lap_count += 1
            if self.lap_count < 1:
                pass
            else:
                self.lap_reset()
            self.lap_time_change()

    def lap_reset(self):
        self.lapTimer.stop()
        self.lap_hours = 0
        self.lap_minutes = 0
        self.lap_seconds = 0
        self.lap_milliseconds = 0

    def lap_time_change(self):
        if self.running:
            self.lapTimer.start(10)
            self.lap_milliseconds += 1
            if self.lap_milliseconds == 100:
                self.lap_seconds += 1
                self.lap_milliseconds = 0
            if self.lap_seconds == 60:
                self.lap_minutes += 1
                self.lap_seconds = 0
            if self.lap_minutes == 60:
                self.lap_hours += 1
                self.lap_minutes = 0

            self.lap_millisecondsString = f'{self.lap_milliseconds}' if \
                self.lap_milliseconds > 9 else f'0{self.lap_milliseconds}'
            self.lap_secondsString = f'{self.lap_seconds}' if self.lap_seconds > 9 else f'0{self.lap_seconds}'
            self.lap_minutesString = f'{self.lap_minutes}' if self.lap_minutes > 9 else f'0{self.lap_minutes}'
            self.lap_hoursString = f'{self.lap_hours}' if self.lap_hours > 9 else f'0{self.lap_hours}'

            if self.lap_count == 0:
                self.lap1.setText(f'Lap {self.lap_count + 1}: {self.lap_hoursString}:{self.lap_minutesString}:'
                                  f'{self.lap_secondsString}.{self.lap_millisecondsString}')
            elif self.lap_count == 1:
                self.lap2.setText(f'Lap {self.lap_count + 1}: {self.lap_hoursString}:{self.lap_minutesString}:'
                                  f'{self.lap_secondsString}.{self.lap_millisecondsString}')
            elif self.lap_count == 2:
                self.lap3.setText(f'Lap {self.lap_count + 1}: {self.lap_hoursString}:{self.lap_minutesString}:'
                                  f'{self.lap_secondsString}.{self.lap_millisecondsString}')
            elif self.lap_count == 3:
                self.lap4.setText(f'Lap {self.lap_count + 1}: {self.lap_hoursString}:{self.lap_minutesString}:'
                                  f'{self.lap_secondsString}.{self.lap_millisecondsString}')
