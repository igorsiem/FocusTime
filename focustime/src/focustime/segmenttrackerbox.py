"""
Declare and implement the SegementTrackerBox class.
"""

import datetime
from datetime import timedelta

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from focustime.segment import Segment

class SegmentTrackerBox(toga.Box):
    """A Toga Box class with UI elements for running a single focus segment
    
    This class includes several UI attributes for displaying the information
    we want, as well as a `segment` attribute (class `Segement`) containing the
    business logic.
    """

    def __init__(self):
        """Set up the UI of the segment tracker box"""

        super(SegmentTrackerBox, self).__init__(style=Pack(direction=COLUMN))
        
        # Label for the phase or stage of the focus segement (focus or break)
        self.stage_lbl = toga.Label("[Focus|Break] Time")
        self.add(self.stage_lbl)
        
        # The countdown time of the current stage
        countdown_box = toga.Box(style=Pack(direction=ROW))
        countdown_box.add(toga.Label("Time left:"))
        self.countdown_lbl = toga.Label("<NN min SS sec>")
        countdown_box.add(self.countdown_lbl)
        self.add(countdown_box)

        # Buttons for starting, pausing, completing (early) or cancelling the
        # current segment
        button_box = toga.Box(style=Pack(direction=ROW))
        self.start_btn = toga.Button("Start", enabled=False,
            on_press=self.on_start_btn_press)
        self.pause_btn = toga.Button("Pause", enabled=False)
        self.complete_btn = toga.Button("Complete", enabled=False)
        self.cancel_btn = toga.Button("Cancel", enabled=False)
        button_box.add(self.start_btn)
        button_box.add(self.pause_btn)
        button_box.add(self.complete_btn)
        button_box.add(self.cancel_btn)
        self.add(button_box)

        # The segment object itself
        self.segment = Segment()

        # Update the display items for the first time
        self.update()

    def on_start_btn_press(self, widget):
        """Start the current focus segment when the Start button is pressed."""
        self.start_segment()

    def set_stage_label_text(self):
        """Set the 'stage' label with a human-readable description of the
        state of the segment"""

        # What state is the segment in?
        if self.segment.state == Segment.State.NOT_STARTED:
            self.stage_lbl.text = "Time to Focus!"
        elif self.segment.state == Segment.State.STARTED_FOCUS:
            self.stage_lbl.text = "Focusing..."
        elif self.segment.state == Segment.State.PAUSED_FOCUS:
            self.stage_lbl.text = "Focusing - Paused"
        elif self.segment.state == Segment.State.STARTED_BREAK:
            self.stage_lbl.text = "On a break..."
        elif self.segment.state == Segment.State.PAUSED_BREAK:
            self.stage_lbl.text = "Break time - Paused"
        elif self.segment.state == Segment.State.COMPLETED:
            self.stage_lbl.text = "Done!"
        else:
            raise ValueError("unrecognised segment state")

    def set_countdown_label_text(self):
        """Set the countdown label with the time remaining in the current stage
        of the segment."""

        if self.segment.state == Segment.State.NOT_STARTED:
            self.countdown_lbl.text = "Not Started"
        elif self.segment.state == Segment.State.STARTED_FOCUS or \
                self.segment.state == Segment.State.STARTED_BREAK:
            self.countdown_lbl.text = "{}m {}s".format( \
                self.segment.minutes_remaining,
                self.segment.seconds_of_minute_remaining)
        elif self.segment.state == Segment.State.PAUSED_FOCUS or \
                self.segment.state == Segment.State.PAUSED_BREAK:
            NotImplementedError("support for pausing is not implemented yet")
        elif self.segment.state == Segment.State.COMPLETED:
            self.countdown_lbl.text = ""
        else:
            raise ValueError("unrecognised segment state")

    def set_button_enablement(self):
        """Set the enablement state of the buttons, depending on the state of
        the segment."""
        if self.segment.state == Segment.State.NOT_STARTED:
            self.start_btn.enabled = True
            self.pause_btn.enabled = False
            self.complete_btn.enabled = False
            self.cancel_btn.enabled = False

        elif self.segment.state == Segment.State.STARTED_FOCUS:
            self.start_btn.enabled = False
            self.pause_btn.enabled = False
            self.complete_btn.enabled = False
            self.cancel_btn.enabled = False

        elif self.segment.state == Segment.State.PAUSED_FOCUS:
            self.start_btn.enabled = False
            self.pause_btn.enabled = False
            self.complete_btn.enabled = False
            self.cancel_btn.enabled = False

        elif self.segment.state == Segment.State.STARTED_BREAK:
            self.start_btn.enabled = False
            self.pause_btn.enabled = False
            self.complete_btn.enabled = False
            self.cancel_btn.enabled = False

        elif self.segment.state == Segment.State.PAUSED_BREAK:
            self.start_btn.enabled = False
            self.pause_btn.enabled = False
            self.complete_btn.enabled = False
            self.cancel_btn.enabled = False

        elif self.segment.state == Segment.State.COMPLETED:
            self.start_btn.enabled = False
            self.pause_btn.enabled = False
            self.complete_btn.enabled = False
            self.cancel_btn.enabled = False

        else:
            raise ValueError("unrecognised segment state")

    def update(self):
        """"Update the various UI elements based on the current time, and
        state of the segment."""

        self.set_stage_label_text()
        self.set_countdown_label_text()
        self.set_button_enablement()

    def start_segment(self):
        """Start the focus segment by starting the `segment` object with the
        current time."""

        #self.segment.begin(
        #    duration=timedelta(seconds=20),
        #    break_duration=timedelta(seconds=5))
        self.segment.begin()
        self.update()
