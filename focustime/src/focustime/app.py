"""
Time-keeping for people who need to focus
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import datetime

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

        # Build a box for displaying the time
        time_box = toga.Box(style=Pack(direction=ROW))
        time_box.add(toga.Label("Time:"))
        self.time_lbl = toga.Label("<the time>")
        time_box.add(self.time_lbl)
        
        main_box.add(time_box)

        # Build the main application window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # Perform first time-related updates
        self.update_time()

        # Set up background processing
        self.add_background_task(self.process_in_background)

    def update_time(self):
        """Perform all actions associated with the progress of time."""
        now = datetime.datetime.now()

        self.time_lbl.text = "{}-{}-{} {}:{}:{}".format(
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second
        )

    def process_in_background(self, widget):
        """Perform background processing tasks
        
        This method is called for background processing functionality, like
        time updates.
        """
        while True:
            self.update_time()            
            yield 1

    @staticmethod
    def test():
        """Verify that static method can be called from test class.
        
        TODO: Remove this method when we have some real functionality to test.
        """
        return True


def main():
    """Instantiate the FocusTime application object."""
    return FocusTime()
