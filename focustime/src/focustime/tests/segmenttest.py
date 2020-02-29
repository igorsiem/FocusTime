"""
Test the FocusDay class.
"""

import unittest
from datetime import datetime, timedelta
from focustime.segment import Segment

class TestSegment(unittest.TestCase):
    """Verify the functionality of the Segment class."""

    def test_segment(self):
        """Verify initialisation and basic calcs"""

        # A single focus time segment, commencing on 2020-Feb-01 at 09:00:00,
        # with a standard 25 minute duration plus a 5 minute break.
        seg = Segment(
            datetime(2020, 2, 1, 9, 0, 0),
            timedelta(minutes=25),
            timedelta(minutes=5))

        self.assertEqual(seg.end_focus_time(), datetime(2020, 2, 1, 9, 25, 0))
        self.assertEqual(seg.start_break_time(), datetime(2020, 2, 1, 9, 25, 0))
        self.assertEqual(seg.end_break_time(), datetime(2020, 2, 1, 9, 30))
