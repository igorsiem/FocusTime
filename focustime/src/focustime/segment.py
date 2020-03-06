import logging
import datetime
from datetime import datetime, timedelta
from enum import Enum

class Segment:
    """A single focusing time segment, with a start, duration, and break
    duration

    This class assumes that the break commences as soon as the focus time ends.

    TODO: Update this
    """

    class Interval:
        """A simple time interval, with a starting time and a duration"""
        def __init__(self, start=None,duration=None):
            self.start = start
            self.duration = duration

        @property
        def end(self):
            """Retrieve the end time of the Interval, which is the start plus
            the duration"""
            return self.start + self.duration

    class State(Enum):
        """The different states for the segment"""
        NOT_STARTED = 0
        STARTED_FOCUS = 1
        PAUSED_FOCUS = 2
        STARTED_BREAK = 3
        PAUSED_BREAK = 4
        COMPLETED = 5

        def __str__(self):
            """Convert state enumeration to human-readable string

            TODO: Sort out internationalisation
            """
            if self == Segment.State.NOT_STARTED:
                return "Not started"
            elif self == Segment.State.STARTED_FOCUS:
                return "Started focus"
            elif self == Segment.State.PAUSED_FOCUS:
                return "Paused focus"
            elif self == Segment.State.STARTED_BREAK:
                return "Started break"
            elif self == Segment.State.PAUSED_BREAK:
                return "Paused break"
            elif self == Segment.State.COMPLETED:
                return "Completed"
            else:
                return "Unrecognised state enumeration: {}".format(self.value)

    def __init__(self):
        """Initialise the segment with a starting date/time, a duration, and a
        break duration.

        TODO: Update this
        """
        ###self.start = None
        ###self.duration = None
        ###self.break_duration = None

        self.state = Segment.State.NOT_STARTED
        self.current_interval = None        # Interval currently in progress
        self.focus_intervals = []           # Actual focus intervals
        self.break_intervals = []           # Actual break intervals
        self.nominal_focus_duration = None  # How long we want to focus
        self.nominal_break_duration = None  # How long we want for a break

    ###@property
    ###def end_focus_time(self):
    ###    """Calculate the end of the focusing period (without the break).
    ###    
    ###    Note that `None` is returned if either the `start` or `duration` are
    ###    `None`.
    ###    """
    ###    if self.start and self.duration:
    ###        return self.start + self.duration
    ###    else:
    ###        return None

    ###@property
    ###def start_break_time(self):
    ###    """Calculate the begining of the break time (same as end of the focus
    ###    time)."""
    ###    return self.end_focus_time

    ###@property
    ###def end_break_time(self):
    ###    """Calculate the end of the break time.
    ###            
    ###    `None` is returned if either the `start_break_time` or the `duration`
    ###    are `Nones.
    ###    """
    ###    if self.start_break_time and self.break_duration:
    ###        return self.start_break_time + self.break_duration
    ###    else:
    ###        return None

    def begin(self,
            start = datetime.now(),
            nominal_focus_duration=timedelta(minutes=25),
            nominal_break_duration=timedelta(minutes=5)):

        if self.state != Segment.State.NOT_STARTED:
            logging.warning("called `begin` on `Segment` object when state " \
                "is \"{}\" (should be \"{}\")".format( 
                    self.state,
                    Segment.State.NOT_STARTED))

        self.state = Segment.State.STARTED_FOCUS
        self.current_interval = Segment.Interval(
            start=start, duration=timedelta(seconds=0))
        self.focus_intervals = []
        self.break_intervals = []
        self.nominal_focus_duration = nominal_focus_duration
        self.nominal_break_duration = nominal_break_duration

    @property
    def actual_focus_duration(self):
        """Retrieve the total Focus Time Duration for the Segment
        
        This is the sum of the Durations of all Focus Intervals in the Segment,
        as well as the Current Interval if the current status is Focusing or
        Paused Focusing.
        """

        t = timedelta(seconds=0)
        for i in self.focus_intervals:
            t += i.duration

        # Include the current interval if we are in focus time (or paused focus
        # time)
        if self.current_interval:
            if self.state == Segment.State.STARTED_FOCUS or \
                    self.state == Segment.State.PAUSED_FOCUS:
                t += self.current_interval.duration

        return t

    @property
    def actual_break_duration(self):
        """Retrieve the total Break Time Duration for the Segment
        
        This is the sum of the Durations of all Break Intervals in the Segment,
        as well as the Current Interval, if the current status is Break or
        Paused Break.
        """

        t = timedelta(seconds=0)

        for i in self.break_intervals:
            t += i.duration

        # Include current duration if we are on a break (or break paused) right
        # now
        if self.current_interval:
            if self.state == Segment.State.STARTED_BREAK or \
                    self.state == Segment.State.PAUSED_BREAK:
                t += self.current_interval.duration

        return t

    @property
    def remaining_focus_duration(self):
        """Calculate the remaining duration of focus time in this segment."""
        return self.nominal_focus_duration - self.actual_focus_duration

    @property
    def remaining_break_duration(self):
        """Calculate the remaining duration of break time in this segment."""
        return self.nominal_break_duration - self.actual_break_duration

    ###@property
    ###def time_remaining(self):
    ###    if self.state == Segment.State.NOT_STARTED:
    ###        return None
    ###    elif self.state == Segment.State.STARTED_FOCUS:
    ###        return self.end_focus_time - datetime.now()
    ###    elif self.state == Segment.State.STARTED_BREAK:
    ###        return self.end_break_time - datetime.now()
    ###    else:
    ###        return timedelta(seconds=0)

    ###@property
    ###def minutes_remaining(self):
    ###    """The number of whole minutes in the `time_remaining` property, or
    ###    `None` if `time_remaining` returns `None`."""
    ###    rem = self.time_remaining
    ###    if rem:
    ###        return int(rem.seconds / 60)
    ###    else:
    ###        return None

    ###@property
    ###def seconds_of_minute_remaining(self):
    ###    """The number of seconds in the `time_remaining` property after
    ###    subtracting the whole minutes, or `None`, if `time_remaining` returns
    ###    `None`"""
    ###    rem = self.time_remaining
    ###    if rem:
    ###        return rem.seconds % 60
    ###    else:
    ###        return None

    def update(self, now=None):
        if now == None:
            now = datetime.now()

        logging.debug("updated with now={}".format(now))

        # What phase are we in?
        if self.state == Segment.State.NOT_STARTED:
            # We haven't started focusing - nothing to see here...
            pass

        elif self.state == Segment.State.STARTED_FOCUS:
            # We've started focusing. If there isn't a 'current interval', then
            # create one - otherwise, just update the duration of the current
            # interval
            if self.current_interval == None:
                self.current_interval = \
                    Segment.Interval(now, timedelta(seconds=0))
            else:
                self.current_interval.duration = now-self.current_interval.start

            # Have we reached the end of focus time? If so, move to our break
            # time...
            if self.actual_focus_duration >= self.nominal_focus_duration:
                self.focus_intervals.append(self.current_interval)
                self.current_interval = None
                self.state = Segment.State.STARTED_BREAK

            # TODO Consider a 'focus time finished' callback

        elif self.state == Segment.State.PAUSED_FOCUS:
            # We're in 'paused focus' mode. Nothing to do...
            pass

        elif self.state == Segment.State.STARTED_BREAK:
            # We're on a break. If there isn't a 'current interval', then
            # create one. Otherwise, just update the duration of the current
            # interval.
            if self.current_interval == None:
                self.current_interval = \
                    Segment.Interval(now, timedelta(seconds=0))
            else:
                self.current_interval.duration = now-self.current_interval.start

            # Have we reached the end of our break time? If so, move to
            # the 'completed' status.
            if self.actual_break_duration >= self.nominal_break_duration:
                self.break_intervals.append(self.current_interval)
                self.current_interval = None
                self.state = Segment.State.COMPLETED

            # TOOD Consider a 'break time finished' callback

        elif self.state == Segment.State.PAUSED_BREAK:
            # We're on a break, but the break is paused. If there's a 'current
            # interval, then move it to the focus intervals collection.
            if self.current_interval:
                self.break_intervals.append(self.current_interval)
                self.current_interval = None

        elif self.state == Segment.State.COMPLETED:
            # We're done - there's nothing to do
            pass

        else:
            # Whoops, not sure what we're doing
            logging.warning("unrecognised state: {}".format(self.state))

    def pause(self):
        # We want to pause - what state are we in?
        if self.state == Segment.State.STARTED_FOCUS:
            # We've been (trying to) focus, so pause that.
            self.state = Segment.State.PAUSED_FOCUS
            if self.current_interval:
                self.focus_intervals.append(self.current_interval)
                self.current_interval = None
            else:
                logging.warning("pausing a focus interval, but there is no " \
                    "current interval object")
            
        elif self.state == Segment.State.STARTED_BREAK:
            # We were on a break, so pause that.
            self.state = Segment.State.PAUSED_BREAK
            if self.current_interval:
                self.break_intervals.append(self.current_interval)
                self.current_interval = None
            else:
                logging.warning("pausing a break interval, but there is no " \
                    "current interval object")

        else:
            # We're not actually doing anything that can be paused - issue a
            # warning.
            logging.warning(
                "attempting to pause from state \"{}\"".format(self.state))

    def complete(self):
        #### We want to complete 'early' - what stage are we in right now?
        ###if self.state == Segment.State.STARTED_FOCUS:
        ###    if self.current_interval:
        ###        self.focus_intervals.append(self.current_interval)
        ###        self.current_interval = None
        ###elif self.state == Segment.State.STARTED_BREAK:

                
        raise NotImplementedError("This method is not implemented yet")

    def cancel(self):
        raise NotImplementedError("This method is not implemented yet")    
