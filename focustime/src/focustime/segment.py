import datetime
from datetime import datetime, timedelta

class Segment:
    """A single focusing time segment, with a start, duration, and break
    duration

    This class assumes that the break commences as soon as the focus time ends.
    """
            
    def __init__(self, start, duration, break_duration):
        """Initialise the segment with a starting date/time, a duration, and a
        break duration.
        """
        self.start = start
        self.duration = duration
        self.break_duration = break_duration

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
        time)"""
        return self.end_focus_time

    @property
    def end_break_time(self):
        """Calculate the end of the break time
                
        `None` is returned if either the `start_break_time` or the `duration`
        are `Nones.
        """
        if self.start_break_time and self.break_duration:
            return self.start_break_time + self.break_duration
        else:
            return None

    def start_now(self,
            duration=timedelta(minutes=25),
            break_duration=timedelta(minutes=5)):
        """Set the attributes of the segment to begin at the current, with
        standard durations
        
        TODO: Make focus and break durations come from config
        """

        self.start = datetime.now()
        self.duration = duration
        self.break_duration = break_duration
