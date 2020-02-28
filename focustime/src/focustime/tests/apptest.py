"""
Test the main FocusTime application class
"""

import unittest
from focustime.app import FocusTime

class TestFocusTime(unittest.TestCase):
    """Verify the functionality of the main FocusTime application class."""

    def test(self):
        """Verify that we can simply call a static method of the application
        class.

        TODO: Replace this with some real tests when the application class has
        some real functionality.
        """
        self.assertTrue(FocusTime.test())
