"""Time-keeping for people who need to focus
"""

import logging
import datetime
import threading
import time

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from focustime.models.segment import Segment
from focustime.views.segmenttrackerbox import SegmentTrackerBox

# TODO: set logging level from some kind of runtime config
logging.basicConfig(level=logging.DEBUG)

class FocusTime(toga.App):
    """The main FocusTime application class
    """

    def startup(self):
        """Construct and show the Toga application.
        """

        # Build the main content box
        main_box = toga.Box(style=Pack(direction=COLUMN))

        # The box that tracks the progress of the current focus segment
        self.segment_tracker_box = SegmentTrackerBox()
        main_box.add(self.segment_tracker_box)

        # Build the main application window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # Perform first time-related updates
        self.update_time()

        # Set up background processing with a timer.
        self.timer = threading.Timer(1.0, self.process_in_background)
        self.timer.start()

        logging.debug("FocusTime application started")

    def update_time(self):
        """Perform all actions associated with the progress of time.
        """
        self.segment_tracker_box.update()

    def process_in_background(self):
        """Perform background processing tasks
        
        This method is called when `self.timer` fires, and is used for
        background processing functionality, like time updates. In the
        current iteration, it only calls `update_time`. It also re-creates
        `self.timer`.
        """
        self.update_time()

        self.timer = threading.Timer(1.0, self.process_in_background)
        self.timer.start()

def main():
    """Instantiate the FocusTime application object."""
    return FocusTime('FocusTime', "com.technopraxia.focustime")

if __name__ == '__main__':
    main().main_loop()
