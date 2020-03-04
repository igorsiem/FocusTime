import datetime
from datetime import datetime, timedelta
from enum import Enum

class Segment:
    """A single focusing time segment, with a start, duration, and break
    duration

    This class assumes that the break commences as soon as the focus time ends.
    """

    class State(Enum):
        """The different states for the segment"""
        NOT_STARTED = 0
        STARTED_FOCUS = 1
        PAUSED_FOCUS = 2
        STARTED_BREAK = 3
        PAUSED_BREAK = 4
        COMPLETED = 5

    def __init__(self):
        """Initialise the segment with a starting date/time, a duration, and a
        break duration.
        """
        self.start = None
        self.duration = None
        self.break_duration = None

    @property
    def end_focus_time(self):
        """Calculate the end of the focusing period (without the break).
        
        Note that `None` is returned if either the `start` or `duration` are
        `None`.
        """
        if self.start and self.duration:
            return self.start + self.duration
        else:
            return None

    @property
    def start_break_time(self):
        """Calculate the begining of the break time (same as end of the focus
        time)."""
        return self.end_focus_time

    @property
    def end_break_time(self):
        """Calculate the end of the break time.
                
        `None` is returned if either the `start_break_time` or the `duration`
        are `Nones.
        """
        if self.start_break_time and self.break_duration:
            return self.start_break_time + self.break_duration
        else:
            return None

    @property
    def state(self):
        """Retrieve the state enumerator, based on the current time, and the
        time attributes of the segment object."""
            
        now = datetime.now()

        if self.start == None:
            return Segment.State.NOT_STARTED
        elif now < self.start:
            return Segment.State.NOT_STARTED
        elif now < self.end_focus_time:
            return Segment.State.STARTED_FOCUS
        elif now < self.end_break_time:
            return Segment.State.STARTED_BREAK
        else:
            return Segment.State.COMPLETED

    @property
    def time_remaining(self):
        """Calculate the time remaining in current stage

        If the segment has not started, then `None` is returned.

        If the segment is in the focus or break stages, then a timedelta
        object denoting the remaining focus or break time is returned.

        If the segment is paused (in either the focus or break stages), or if
        the segment is completed or cancelled, then a timedelta with zero time
        is returned.
        """
        if self.state == Segment.State.NOT_STARTED:
            return None
        elif self.state == Segment.State.STARTED_FOCUS:
            return self.end_focus_time - datetime.now()
        elif self.state == Segment.State.STARTED_BREAK:
            return self.end_break_time - datetime.now()
        else:
            return timedelta(seconds=0)

    @property
    def minutes_remaining(self):
        """The number of whole minutes in the `time_remaining` property, or
        `None` if `time_remaining` returns `None`."""
        rem = self.time_remaining
        if rem:
            return int(rem.seconds / 60)
        else:
            return None

    @property
    def seconds_of_minute_remaining(self):
        """The number of seconds in the `time_remaining` property after
        subtracting the whole minutes, or `None`, if `time_remaining` returns
        `None`"""
        rem = self.time_remaining
        if rem:
            return rem.seconds % 60
        else:
            return None

    def update(self):
        raise NotImplementedError("This method is not implemented yet")

    def begin(self,
            start = datetime.now(),
            duration=timedelta(minutes=25),
            break_duration=timedelta(minutes=5)):
        """Set the attributes of the segment to begin at the current, with
        standard durations
        
        TODO: Make focus and break durations come from config
        """
        self.start = start
        self.duration = duration
        self.break_duration = break_duration

    def pause(self):
        raise NotImplementedError("This method is not implemented yet")

    def complete(self):
        raise NotImplementedError("This method is not implemented yet")

    def cancel(self):
        raise NotImplementedError("This method is not implemented yet")    
