import datetime

class Segment:
    """A single focusing time segment, with a start, duration, and break
    duration

    This assumes that the break commences as soon as the focus time ends.
    """
            
    def __init__(self, start, duration, break_duration):
        """Initialise the segment with a starting date/time, a duration, and a
        break duration.
        """
        self.start = start
        self.duration = duration
        self.break_duration = break_duration

    def end_focus_time(self):
        """Calculate the end of the focusing period (without the break)."""
        return self.start + self.duration

    def start_break_time(self):
        """Calculate the begining of the break time (same as end of the focus
        time)
        """
        return self.end_focus_time()

    def end_break_time(self):
        """Calculate the end of the break time"""
        return self.start_break_time() + self.break_duration
