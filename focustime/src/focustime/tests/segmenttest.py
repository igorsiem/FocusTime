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

        # Everything is `None` when you first construct a segment
        seg = Segment()

        self.assertEqual(seg.end_focus_time, None)
        self.assertEqual(seg.start_break_time, None)
        self.assertEqual(seg.end_break_time, None)

        # 'start' the segment
        seg.begin(start=datetime(2020, 2, 1, 9, 0, 0),
            duration=timedelta(minutes=25),
            break_duration=timedelta(minutes=5))

        self.assertEqual(seg.end_focus_time, datetime(2020, 2, 1, 9, 25, 0))
        self.assertEqual(seg.start_break_time, datetime(2020, 2, 1, 9, 25, 0))
        self.assertEqual(seg.end_break_time, datetime(2020, 2, 1, 9, 30))

    def test_null_attributes(self):
        """Verify segment behaviour when some of the attributes are None."""

        seg = Segment()
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
