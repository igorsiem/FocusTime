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

    def test_normal_update_sequence(self):
        """Verify the 'normal' sequence of updates that a Segment can undergo.
        
        TODO: This test is a bit long - can we break it up?
        """

        # Segment is instantiated with nothing, and is then begun at 0900 on
        # 1 Jan, 2020. Nominal focus and break durations are 25 minutes and
        # 5 minutes respectively. We are now in the 'focusing' state
        s = Segment()

        s.begin(
            start=datetime(2020,1,1,9,0,0),
            nominal_focus_duration=timedelta(minutes=25),
            nominal_break_duration=timedelta(minutes=5)
        )

        self.assertEqual(Segment.State.STARTED_FOCUS, s.state)

        # Segment is updated 1 second later. At this point, we have focused for
        # a total of 1 second, and have 24m 59s focus time left. No break time
        # so far.
        s.update(datetime(2020,1,1,9,0,1))

        self.assertEqual(
            timedelta(seconds=1),
            s.actual_focus_duration)

        self.assertEqual(
            timedelta(minutes=24,seconds=59),
            s.remaining_focus_duration)

        self.assertEqual(
            timedelta(seconds=0),
            s.actual_break_duration)

        self.assertEqual(
            timedelta(minutes=5),
            s.remaining_break_duration)

        # Segment is updated after 10 minutes. Focus times have updated
        # accordingly.
        s.update(datetime(2020,1,1,9,10,0))

        self.assertEqual(
            timedelta(minutes=10),
            s.actual_focus_duration)

        self.assertEqual(
            timedelta(minutes=15),
            s.remaining_focus_duration)

        # Now we pause. Focus times have not changed.
        s.pause()

        self.assertEqual(Segment.State.PAUSED_FOCUS, s.state)

        self.assertEqual(
            timedelta(minutes=10),
            s.actual_focus_duration)

        self.assertEqual(
            timedelta(minutes=15),
            s.remaining_focus_duration)

        # Update after another minute (11 minutes). Focus times have not changed
        # because we are paused.
        s.update(datetime(2020,1,1,9,11,0))

        self.assertEqual(Segment.State.PAUSED_FOCUS, s.state)

        self.assertEqual(
            timedelta(minutes=10),
            s.actual_focus_duration)

        self.assertEqual(
            timedelta(minutes=15),
            s.remaining_focus_duration)

        # Now, unpause the Segment
        s.unpause(datetime(2020,1,1,9,11,0))

        self.assertEqual(Segment.State.STARTED_FOCUS, s.state)

        # Update after another minute
        s.update(datetime(2020,1,1,9,12,0))

        self.assertEqual(
            timedelta(minutes=11),
            s.actual_focus_duration)

        self.assertEqual(
            timedelta(minutes=14),
            s.remaining_focus_duration)

        # Update again, this time, we should be one second before the end of the
        # focus period.
        s.update(datetime(2020,1,1,9,25,59))

        self.assertEqual(Segment.State.STARTED_FOCUS, s.state)

        self.assertEqual(
            timedelta(minutes=24,seconds=59),
            s.actual_focus_duration)

        self.assertEqual(
            timedelta(minutes=0,seconds=1),
            s.remaining_focus_duration)

        # Update one second later - now we're in break time (just).
        s.update(datetime(2020,1,1,9,26,0))

        self.assertEqual(Segment.State.STARTED_BREAK, s.state)

        self.assertEqual(
            timedelta(minutes=25),
            s.actual_focus_duration)

        self.assertEqual(
            timedelta(minutes=0),
            s.remaining_focus_duration)

        self.assertEqual(
            timedelta(minutes=0),
            s.actual_break_duration)

        self.assertEqual(
            timedelta(minutes=5),
            s.remaining_break_duration)

        # Update 2m 30s into the break
        s.update(datetime(2020,1,1,9,28,30))

        self.assertEqual(Segment.State.STARTED_BREAK, s.state)

        self.assertEqual(
            timedelta(minutes=2,seconds=30),
            s.actual_break_duration)

        self.assertEqual(
            timedelta(minutes=2,seconds=30),
            s.remaining_break_duration)

        # Pause the break.
        s.pause()
        self.assertEqual(Segment.State.PAUSED_BREAK, s.state)

        # 2 minutes later, we still have the same durationss
        s.update(datetime(2020,1,1,9,30,30))

        self.assertEqual(Segment.State.PAUSED_BREAK, s.state)
        self.assertEqual(
            timedelta(minutes=2,seconds=30),
            s.actual_break_duration)

        self.assertEqual(
            timedelta(minutes=2,seconds=30),
            s.remaining_break_duration)

        # Un-pause and continue to one second before the end of the break.
        s.unpause(now=datetime(2020,1,1,9,30,30))

        s.update(datetime(2020,1,1,9,32,59))
        self.assertEqual(Segment.State.STARTED_BREAK, s.state)

        self.assertEqual(
            timedelta(minutes=4,seconds=59),
            s.actual_break_duration)

        self.assertEqual(
            timedelta(minutes=0,seconds=1),
            s.remaining_break_duration)

        # A second later, everything is finished
        s.update(now=datetime(2020,1,1,9,33,0))
        self.assertEqual(Segment.State.COMPLETED, s.state)

        self.assertEqual(
            timedelta(minutes=25),
            s.actual_focus_duration)

        self.assertEqual(
            timedelta(minutes=0),
            s.remaining_focus_duration)

        self.assertEqual(
            timedelta(minutes=5),
            s.actual_break_duration)

        self.assertEqual(
            timedelta(minutes=0),
            s.remaining_break_duration)

        ###self.assertTrue(False, "tests are incomplete")

    def test_premature_completion(self):
        """Test sequence where a Segment is 'manually' completed before it's
        nominal time."""

        # Segment can be completed before it is even begun.
        segment = Segment()
        segment.complete()

        self.assertEqual(Segment.State.COMPLETED, segment.state)

        # Segment can be manually completed after focus time has started but
        # not finished.
        segment = Segment()
        segment.begin(start=datetime(2020,1,1,9,0,0))
        segment.update(datetime(2020,1,1,9,1,0))
        segment.complete()

        self.assertEqual(Segment.State.COMPLETED, segment.state)
        self.assertEqual(timedelta(minutes=1), segment.actual_focus_duration)
        self.assertEqual(timedelta(seconds=0), segment.actual_break_duration)

        # Segment can be completed after the break has begun, but not finished.
        segment = Segment()
        segment.begin(start=datetime(2020,1,1,9,0,0))
        segment.update(datetime(2020,1,1,9,26,0))

        self.assertEqual(Segment.State.STARTED_BREAK, segment.state)

        segment.complete()

        self.assertEqual(Segment.State.COMPLETED, segment.state)
        self.assertEqual(timedelta(minutes=25), segment.actual_focus_duration)
        self.assertEqual(timedelta(minutes=1), segment.actual_break_duration)

    def test_cancellation(self):
        """Test sequence for a Segment being cancelled before it is
        completed."""

        # Segment can be manually cancelled after focus time has started but
        # not finished.
        segment = Segment()
        segment.begin(start=datetime(2020,1,1,9,0,0))
        segment.update(datetime(2020,1,1,9,1,0))

        segment.cancel()

        self.assertEqual(Segment.State.NOT_STARTED, segment.state)
        self.assertEqual(timedelta(seconds=0), segment.actual_focus_duration)
        self.assertEqual(timedelta(seconds=0), segment.actual_break_duration)

        # Segment can be cancelled after the break has begun, but not finished.
        segment = Segment()
        segment.begin(start=datetime(2020,1,1,9,0,0))
        segment.update(datetime(2020,1,1,9,26,0))

        self.assertEqual(Segment.State.STARTED_BREAK, segment.state)

        segment.cancel()

        self.assertEqual(Segment.State.NOT_STARTED, segment.state)
        self.assertEqual(timedelta(seconds=0), segment.actual_focus_duration)
        self.assertEqual(timedelta(seconds=0), segment.actual_break_duration)
