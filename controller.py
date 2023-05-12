from PyQt6.QtWidgets import *
from view import *
import sys
import csv


class Controller(QMainWindow, Ui_Stopwatch):
    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes controller for GUI, creating connection with view.py file to enable interaction with GUI.
        :param args: Essential for initialization of controller, based on knowledge from Test 10
        :param kwargs: Same as above
        """
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # Connecting buttons created in QtCreator with functions defined below
        self.start_button.clicked.connect(lambda: self.start())
        self.reset_button.clicked.connect(lambda: self.reset())
        self.quit_button.clicked.connect(lambda: self.ui_quit())
        self.lap_button.clicked.connect(lambda: self.lap())

        # Creation and formatting of a csv file to store lap times from the stopwatch
        self.laps = open('laps.csv', 'w')
        self.lap_writer = csv.writer(self.laps)
        self.lap_writer.writerow(['Lap #', 'Hours', 'Minutes', 'Seconds', 'Milliseconds'])
        self.laps.close()

        # Defining variables to store information such as whether the stopwatch is running or not, the hours, minutes,
        # seconds, and milliseconds of the stopwatch and lap stopwatch, and a count of what the current lap is
        self.running = False

        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.milliseconds = 0

        self.millisecondsString = '00'
        self.secondsString = '00'
        self.minutesString = '00'
        self.hoursString = '00'

        self.lap_hours = 0
        self.lap_minutes = 0
        self.lap_seconds = 0
        self.lap_milliseconds = 0

        self.lap_count = 0

        self.lap_millisecondsString = '00'
        self.lap_secondsString = '00'
        self.lap_minutesString = '00'
        self.lap_hoursString = '00'

        # Creation of timers from QtCore that are linked with the time_change() and lap_time_change() functions,
        # essential for the running and timing of the stopwatch
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.time_change)

        self.lapTimer = QtCore.QTimer(self)
        self.lapTimer.timeout.connect(self.lap_time_change)

        # Creation of an empty list to be used later to store time values in the csv file
        self.lap_list = []

    def ui_quit(self) -> None:
        """
        Function connected to the Quit button that exits the GUI using the sys module. Also contains a built-in
        function to ensure the 'laps' csv file is closed.
        """
        self.laps.close()
        sys.exit()

    def start(self) -> None:
        """
        Function used to start and pause the regular stopwatch and start the lap stopwatch.
        """
        if not self.running:
            self.running = True
            self.time_change()
            self.lap_time_change()
            self.start_button.setText('Pause')

        else:
            self.running = False
            self.start_button.setText('Start')

    def reset(self) -> None:
        """
        Function to reset the stopwatch GUI, including laps, labels, and timers.
        """
        self.running = False
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.time_label.setText('00:00:00.00')
        self.lap1.setText('')
        # Calls lap_reset() function defined below, essentially stops the lapTimer and resets values
        self.lap_reset()
        self.lap_count = 0
        self.start_button.setText('Start')

    def time_change(self) -> None:
        """
        The mathematical counter for the main stopwatch. Runs the function every millisecond and updates the time
        variables defined in initialization.
        """
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

            # Stores the time variables into strings to help account for single- and double-digit values. ex. if there
            # are 5 seconds elapsed, the label will show '05' instead of '5'
            self.millisecondsString = f'{self.milliseconds}' if self.milliseconds > 9 else f'0{self.milliseconds}'
            self.secondsString = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
            self.minutesString = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
            self.hoursString = f'{self.hours}' if self.hours > 9 else f'0{self.hours}'

            # Sets the label of the stopwatch as a working timer using strings
            self.time_label.setText(f'{self.hoursString}:{self.minutesString}:{self.secondsString}.'
                                    f'{self.millisecondsString}')

    def lap(self) -> None:
        """
        Ran whenever the Lap button is clicked. Increases a lap counter and begins the lap stopwatch. Also writes into
        the csv file to store the lap time values.
        """
        if self.running:
            self.lap_count += 1
            if self.lap_count < 1:
                pass
            else:
                self.lap_reset()
            self.lap_time_change()

            # Appends the lap times into the previously defined csv file
            with open('laps.csv', 'a') as self.laps:
                self.lap_writer = csv.writer(self.laps)
                self.lap_writer.writerow(self.lap_list)
                self.millisecondsString = '00'
                self.lap_secondsString = '00'
                self.lap_minutesString = '00'
                self.lap_hoursString = '00'

    def lap_reset(self) -> None:
        """
        Used to reset the lap stopwatch. Stops the timer and sets values to 0.
        """
        self.lapTimer.stop()
        self.lap_hours = 0
        self.lap_minutes = 0
        self.lap_seconds = 0
        self.lap_milliseconds = 0

    def lap_time_change(self) -> None:
        """
        The mathematical counter for the lap stopwatch. Runs the function every millisecond and updates the time
        variables defined in initialization. Also sets the current lap label to display the current lap.
        """
        if self.running:
            self.lapTimer.start(10)
            self.lap_milliseconds += 1

            # Updates the value of the string to display the correct values of the current lap. Similar statements
            # are repeated later on to ensure the values are updated every millisecond instead of in their own intervals
            self.lap_millisecondsString = f'{self.lap_milliseconds}' if \
                self.lap_milliseconds > 9 else f'0{self.lap_milliseconds}'
            if self.lap_milliseconds == 100:
                self.lap_seconds += 1
                self.lap_milliseconds = 0
                self.lap_secondsString = f'{self.lap_seconds}' if self.lap_seconds > 9 else f'0{self.lap_seconds}'
            if self.lap_seconds == 60:
                self.lap_minutes += 1
                self.lap_seconds = 0
                self.lap_minutesString = f'{self.lap_minutes}' if self.lap_minutes > 9 else f'0{self.lap_minutes}'
                self.lap_secondsString = f'{self.lap_seconds}' if self.lap_seconds > 9 else f'0{self.lap_seconds}'
            if self.lap_minutes == 60:
                self.lap_hours += 1
                self.lap_minutes = 0
                self.lap_hoursString = f'{self.lap_hours}' if self.lap_hours > 9 else f'0{self.lap_hours}'
                self.lap_minutesString = f'{self.lap_minutes}' if self.lap_minutes > 9 else f'0{self.lap_minutes}'
                self.lap_secondsString = f'{self.lap_seconds}' if self.lap_seconds > 9 else f'0{self.lap_seconds}'

            # Sets the text of the label to display the current lap
            self.lap1.setText(f'Lap {self.lap_count + 1}: {self.lap_hoursString}:{self.lap_minutesString}:'
                              f'{self.lap_secondsString}.{self.lap_millisecondsString}')

            # Updates the list used to write rows in the csv file and store lap time values
            self.lap_list = [f'Lap {self.lap_count}', self.lap_hoursString, self.lap_minutesString,
                             self.lap_secondsString, self.millisecondsString]
