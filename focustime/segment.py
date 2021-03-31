import logging
import datetime
from datetime import datetime, timedelta
from enum import Enum
import threading

class Segment:
    """A single session of focusing time

    This class encapsulates all the information recorded about a single
    session of focusing, along with the break that occurs afterwards. It
    maintains collections of `Interval` objects, which are contiguous time
    segments (`start` and `duration`)
    """

    class Interval:
        """A simple time interval, with a starting time and a duration
        """

        def __init__(self, start=None,duration=None):
            """Initialise the Interval object

            Args:
                start (datetime, optional): The starting time for the
                    Interval. Defaults to None.
                duration (timedelta, optional): The duration of the Interval.
                    Defaults to None.
            """
            self.start = start
            self.duration = duration

        @property
        def end(self):
            """Retrieve the end time of the Interval

            Returns:
                datetime: The end time of the Interval
            """
            return self.start + self.duration

    class State(Enum):
        """The different states for the segment
        """
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
        """Initialise the Segment to null values

        Note that items like nominal durations are set when `begin` is called.
        """
        self.state = Segment.State.NOT_STARTED
        self.current_interval = None        # Interval currently in progress
        self.focus_intervals = []           # Actual focus intervals
        self.break_intervals = []           # Actual break intervals
        self.nominal_focus_duration = None  # How long we want to focus
        self.nominal_break_duration = None  # How long we want for a break

    def begin(self,
            start = datetime.now(),
            nominal_focus_duration=timedelta(minutes=25),
            nominal_break_duration=timedelta(minutes=5)):
        """Commence the focusing segment

        Args:
            start (datetime, optional): The starting time of the segment.
                Defaults to datetime.now().
            nominal_focus_duration (timedelta, optional): How long we want to
                focus for. Defaults to timedelta(minutes=25).
            nominal_break_duration (timedelta, optional): How long we want to
                take for a break. Defaults to timedelta(minutes=5).
        """

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
        
        This is the sum of the Durations of all Focus Intervals in the
        Segment, as well as the Current Interval if the current status is
        Focusing or Paused Focusing.
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
        
        This is the sum of the Durations of all Break Intervals in the
        Segment, as well as the Current Interval, if the current status is
        Break or Paused Break.
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
        """Calculate the remaining duration of focus time in this segment.
        """
        return self.nominal_focus_duration - self.actual_focus_duration

    @property
    def remaining_break_duration(self):
        """Calculate the remaining duration of break time in this segment.
        """
        return self.nominal_break_duration - self.actual_break_duration

    def update(self, now=None):
        """Update the segment state, based on the current time

        TODO: Expand this document

        TODO: This method is kinda long... consider refactoring and breaking up
        this method into some smaller ones.
        """
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

                # How far into the break are we? Take that difference off the
                # current interval (which is then added to the pool of focus
                # intervals), and use it for the first part of the break.
                diff = self.actual_focus_duration - self.nominal_focus_duration
                self.current_interval.duration -= diff
                self.focus_intervals.append(self.current_interval)

                self.current_interval = Segment.Interval(
                    start=now-diff,duration=diff)
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

                # How far past the end of the break are we? Subtract that from
                # the duration of the current interval.
                diff = self.actual_break_duration - self.nominal_break_duration
                self.current_interval.duration -= diff

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
        """Trigger a pause in the focusing Segment

        This method may be invoked when either the focusing time or the break
        time has been started. Internally, it closes off the current Interval
        object, and adds it to the relevant intervals collection.
        """
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

    def unpause(self, now=None):
        """Continue the Segment after pausing (either in focusing time, or
        break time)

        Args:
            now (datetime, optional): The current time. Defaults to None.
        """

        if now == None:
            now = datetime.now()

        if self.state == Segment.State.PAUSED_FOCUS:
            self.state = Segment.State.STARTED_FOCUS
        elif self.state == Segment.State.PAUSED_BREAK:
            self.state = Segment.State.STARTED_BREAK
        else:
            logging.warning(
                "attempting to un-pause from state \"{}\"".format(self.state))

        self.current_interval = Segment.Interval(now, timedelta(seconds=0))

    def complete(self):
        """Signal early completion of a Segment

        This method moves the Segment straight to the `COMPLETED` state, no
        matter what. It makes sure any current Interval object will be
        properly added to the right collection.
        """
        # We want to complete 'early' - what stage are we in right now?
        if self.state == Segment.State.STARTED_FOCUS:
            if self.current_interval:
                self.focus_intervals.append(self.current_interval)
                self.current_interval = None
        elif self.state == Segment.State.STARTED_BREAK:
            if self.current_interval:
                self.break_intervals.append(self.current_interval)
                self.current_interval = None

        self.state = Segment.State.COMPLETED

    def cancel(self):
        """This method aborts the Segment no matter what

        All information is discarded and cleared.
        """
        # We want to abort - don't care what state we're in

        self.state = Segment.State.NOT_STARTED

        # Clear everything
        self.current_interval = None
        self.focus_intervals = []
        self.break_intervals = []
        self.nominal_focus_duration = None
        self.nominal_break_duration = None
