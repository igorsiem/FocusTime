"""
Time-keeping for people who need to focus
"""
import logging
import datetime

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from focustime.segment import Segment
from focustime.segmenttrackerbox import SegmentTrackerBox

# TODO: set logging level from some kind of runtime config
logging.basicConfig(level=logging.DEBUG)

class FocusTime(toga.App):
    """The main FocusTime application class"""

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
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

        # Set up background processing
        self.add_background_task(self.process_in_background)

        logging.debug("FocusTime application started")

    def update_time(self):
        """Perform all actions associated with the progress of time."""
        self.segment_tracker_box.update()

    def process_in_background(self, widget):
        """Perform background processing tasks
        
        This method is called for background processing functionality, like
        time updates.
        """
        while True:
            self.update_time()            
            yield 1

def main():
    """Instantiate the FocusTime application object."""
    return FocusTime()
