import logging
import datetime
from datetime import datetime, timedelta

from focustime.models.segment import Segment

class Session:
    """A set of focus Segments, followed by a longer break

    This class encapsulates a set of (nominally four) focusing segments,
    with the 'short breaks', with the final session having a longer break.
    Default times for sessions and breaks are 25 minutes and 5 minutes,
    respectively, with the final session being followed by a longer break of
    15 minutes.
    """

    def __init__(self,
            nominal_number_of_segments = 4,
            nominal_long_break_duration = timedelta(minutes=15)):
        """Initialise the Session

        Args:
            nominal_number_of_segments (int, optional): The nominal number of
                focusing segments for the session; Defaults to 4.
            nominal_long_break_duration (timedelta, optional): The nominal
                length of a long break in this session; Defaults to
                timedelta(minutes=15).
        """

        self.segments = []

        if nominal_number_of_segments < 1:
            raise ValueError(("nominal number of segments set to {}; " + \
                "must have at least 1").format(nominal_number_of_segments))

        self.nominal_number_of_segments = nominal_number_of_segments
        self.nominal_long_break_duration = nominal_long_break_duration

    def create_and_begin_next_segment(self):
        """Create the 'next' Segment object for the session, and begin it

        The `begin` method of the Segment object is called. If this is
        'supposed' to be the last Segment in the Session, the Session is
        given the 'long break' duration.

        Returns:
            Segment: The newly created Segment object, which has been
                appended to the list of segments for this session, and begun
        """
        i = len(self.segments)

        # Use the standard break duration unless we are at the last Segment
        # of the session, in which case, we specify a long break duration.
        nbr = None
        if i >= (self.nominal_number_of_segments-1):
            nbr = self.nominal_long_break_duration

        s = Segment()
        self.segments.append(s)
        s.begin(nominal_break_duration = nbr)
        return s
