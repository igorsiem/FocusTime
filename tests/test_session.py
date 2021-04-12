from datetime import timedelta

import sys
sys.path.insert(0, '../focustime')

from focustime.models.session import Session

def test_instantiation():
    """Test basic instantiation of the Session class

    1. A `Session` can be instantiated with a:

       a. Nominal number of Segments denoting how many Segments are *planned*
          for the Session

       b. A nominal long break duration, denoting the length of time that is
          *planned* for the longer break in between segments

    2. When a `Session` is instantiated, it has a `segments` member, which is
        a list with zero elements.
    """

    s = Session(nominal_number_of_segments=4,
       nominal_long_break_duration=timedelta(minutes=15))
    assert s != None
    assert len(s.segments) == 0
    assert s.nominal_number_of_segments == 4
    assert s.nominal_long_break_duration == timedelta(minutes=15)

def test_create_and_begin_next_segment():
    """Verify a Session's ability to create and being segments
    """
    pass
