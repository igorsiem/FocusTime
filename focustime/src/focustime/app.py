"""
Time-keeping for people who need to focus
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class FocusTime(toga.App):
    """The main FocusTime application class"""

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    @staticmethod
    def test():
        """Verify that static method can be called from test class.
        
        TODO: Remove this method when we have some real functionality to test.
        """
        return True


def main():
    """Instantiate the FocusTime application object."""
    return FocusTime()
