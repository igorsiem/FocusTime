import logging
from focustime.models.segment import Segment

class Session:
    """A set of focus Segments, followed by a longer break

    This class encapsulates a set of (nominally four) focusing segments,
    with the 'short breaks', with the final session having a longer break.
    Default times for sessions and breaks are 25 minutes and 5 minutes,
    respectively, with the final session being followed by a longer break of
    15 minutes.
    """

    def __init__(self):
        """Initialise the Session
        """

        self.segments = []

    