"""
Test the FocusDay class.
"""

import unittest
from datetime import datetime, timedelta
from focustime.segment import Segment

class TestSegment(unittest.TestCase):
    """Verify the functionality of the Segment class."""

    def test_interval(self):
        """Verify the operation of the Segment.Interval class."""

        i = Segment.Interval(
            start=datetime(2020,1,1,9,0,0),
            duration=timedelta(minutes=10))

        self.assertEqual(i.end, datetime(2020,1,1,9,10,0))

    def test_instantiation(self):
        """Verify Segment instantiation"""
        s = Segment()

        self.assertEqual(s.state, Segment.State.NOT_STARTED)
        self.assertIsNone(s.current_interval)
        self.assertEqual(len(s.focus_intervals), 0)
        self.assertEqual(len(s.break_intervals), 0)
        self.assertIsNone(s.nominal_focus_duration)
        self.assertIsNone(s.nominal_break_duration)

    def test_begin(self):
        """Verify the working of the `begin` method."""

        # Create a Segment object, and "begin" it from a specified time
        s = Segment()
        s.begin(
            start=datetime(2020,1,1,9,0,0),
            nominal_focus_duration=timedelta(minutes=25),
            nominal_break_duration=timedelta(minutes=5))

        # State is "Started focus"
        self.assertEqual(s.state, Segment.State.STARTED_FOCUS)

        # The segment has a 'current time interval'
        self.assertIsNotNone(s.current_interval)

        # Arrays of focus and break intervals are still empty
        self.assertEqual(len(s.focus_intervals), 0)
        self.assertEqual(len(s.break_intervals), 0)

        # Nominal focus and break durations are valid
        self.assertEqual(s.nominal_focus_duration, timedelta(minutes=25))
        self.assertEqual(s.nominal_break_duration, timedelta(minutes=5))

    def test_actual_focus_duration(self):
        """Test the `actual_focus_duration` property."""

        # When a segment is first created, there is no focus time.
        s = Segment()
        self.assertEqual(s.actual_focus_duration, timedelta(seconds=0))

        # Now the segment is 'in progress', with just a current time interval
        s.state = Segment.State.STARTED_FOCUS
        s.current_interval = \
            Segment.Interval(
                datetime(2020, 1, 1, 9, 0, 0), timedelta(minutes=5))

        self.assertEqual(s.actual_focus_duration, timedelta(minutes=5))

        # Now the segment has some other focus intervals in its collection
        s.focus_intervals = [
            Segment.Interval(datetime(2020,1,1,9,0,0), timedelta(seconds=20)),
            Segment.Interval(datetime(2020,1,1,9,1,40), timedelta(seconds=20)),
            Segment.Interval(datetime(2020,1,1,9,2,0), timedelta(seconds=20)),
        ]

        s.current_interval = \
            Segment.Interval(
                datetime(2020, 1, 1, 9, 3, 0), timedelta(seconds=10))

        self.assertEqual(s.actual_focus_duration, timedelta(seconds=70))

    def test_actual_break_duration(self):
        """Test the `actual_break_duration` property."""

        # When a segment is first created, there is no break time.
        s = Segment()
        self.assertEqual(timedelta(seconds=0), s.actual_break_duration)

        # Now we're on a break, with just the current time interval
        s.state = Segment.State.STARTED_BREAK
        s.current_interval = Segment.Interval( \
            datetime(2020, 1, 1, 9, 0, 0), timedelta(minutes=5))

        self.assertEqual(s.actual_break_duration, timedelta(minutes=5))

        # Now the segment has some other focus intervals in its collection
        s.break_intervals = [
            Segment.Interval(datetime(2020,1,1,9,0,0), timedelta(seconds=20)),
            Segment.Interval(datetime(2020,1,1,9,1,40), timedelta(seconds=20)),
            Segment.Interval(datetime(2020,1,1,9,2,0), timedelta(seconds=20)),
        ]

        s.current_interval = \
            Segment.Interval(
                datetime(2020, 1, 1, 9, 3, 0), timedelta(seconds=10))

        self.assertEqual(s.actual_break_duration, timedelta(seconds=70))

    def test_update_sequence(self):
        self.assertTrue(False, "tests are incomplete")

    ###    def test_segment(self):
    ###        """Verify initialisation and basic calcs"""
    ###
    ###        # Everything is `None` when you first construct a segment
    ###        seg = Segment()
    ###
    ###        self.assertEqual(seg.end_focus_time, None)
    ###        self.assertEqual(seg.start_break_time, None)
    ###        self.assertEqual(seg.end_break_time, None)
    ###
    ###        # 'start' the segment
    ###        seg.begin(start=datetime(2020, 2, 1, 9, 0, 0),
    ###            duration=timedelta(minutes=25),
    ###            break_duration=timedelta(minutes=5))
    ###
    ###        self.assertEqual(seg.end_focus_time, datetime(2020, 2, 1, 9, 25, 0))
    ###        self.assertEqual(seg.start_break_time, datetime(2020, 2, 1, 9, 25, 0))
    ###        self.assertEqual(seg.end_break_time, datetime(2020, 2, 1, 9, 30))
    ###
    ###    def test_null_attributes(self):
    ###        """Verify segment behaviour when some of the attributes are None."""
    ###
    ###        seg = Segment()
    ###        self.assertIsNone(seg.end_focus_time)
    ###        self.assertIsNone(seg.start_break_time)
    ###        self.assertIsNone(seg.end_break_time)
    ###
    ###        # When there's only a start time, everything is still None.
    ###        seg.start = datetime(2020, 2, 1, 9, 0, 0)
    ###        self.assertIsNone(seg.end_focus_time)
    ###        self.assertIsNone(seg.start_break_time)
    ###        self.assertIsNone(seg.end_break_time)
    ###
    ###        # When there's a start time and a duration, there's an end focus time
    ###        # and a start break time, but still no end break time.
    ###        seg.duration = timedelta(minutes=25)
    ###        self.assertIsNotNone(seg.end_focus_time)
    ###        self.assertIsNotNone(seg.start_break_time)
    ###        self.assertIsNone(seg.end_break_time)
    ###
    ###        # When there's a break duration as well, all calculated values are not
    ###        # None.
    ###        seg.break_duration = timedelta(minutes=5)
    ###        self.assertIsNotNone(seg.end_focus_time)
    ###        self.assertIsNotNone(seg.start_break_time)
    ###        self.assertIsNotNone(seg.end_break_time)
