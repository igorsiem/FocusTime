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

        self.assertEqual(seg.end_focus_time, datetime(2020, 2, 1, 9, 25, 0))
        self.assertEqual(seg.start_break_time, datetime(2020, 2, 1, 9, 25, 0))
        self.assertEqual(seg.end_break_time, datetime(2020, 2, 1, 9, 30))

    def test_null_attributes(self):
        """Verify segment behaviour when some of the attributes are None."""

        seg = Segment(None, None, None)
        self.assertIsNone(seg.end_focus_time)
        self.assertIsNone(seg.start_break_time)
        self.assertIsNone(seg.end_break_time)

        # When there's only a start time, everything is still None.
        seg.start = datetime(2020, 2, 1, 9, 0, 0)
        self.assertIsNone(seg.end_focus_time)
        self.assertIsNone(seg.start_break_time)
        self.assertIsNone(seg.end_break_time)

        # When there's a start time and a duration, there's an end focus time
        # and a start break time, but still no end break time.
        seg.duration = timedelta(minutes=25)
        self.assertIsNotNone(seg.end_focus_time)
        self.assertIsNotNone(seg.start_break_time)
        self.assertIsNone(seg.end_break_time)

        # When there's a break duration as well, all calculated values are not
        # None.
        seg.break_duration = timedelta(minutes=5)
        self.assertIsNotNone(seg.end_focus_time)
        self.assertIsNotNone(seg.start_break_time)
        self.assertIsNotNone(seg.end_break_time)
