"""
Declare and implement the SegementTrackerBox class.
"""

import datetime

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
        self.segment = Segment(None, None, None)

        # Update the display items for the first time
        self.update()

    def on_start_btn_press(self, widget):
        """Start the current focus segment when the Start button is pressed."""
        self.start_segment()

    def update(self):
        """"Update the various UI elements based on the current time, and
        state of the `segment` attribute
        
        TODO: put the state-related logic calculating times into the `Segment`
        class
        """

        # Has the segment been started?
        if self.segment.start == None:

            self.stage_lbl.text = "Focus"
            self.countdown_lbl.text = "not started..."

            self.start_btn.enabled = True
            self.pause_btn.enabled = False
            self.complete_btn.enabled = False
            self.cancel_btn.enabled = False

        else:

            # Segment has been started - what stage are we at?
            now = datetime.datetime.now()
            if now >= self.segment.start and \
                    now < self.segment.end_focus_time():

                # Focus time
                self.stage_lbl.text = "Focusing..."

                time_to_go = self.segment.end_focus_time() - now
                mins = int(time_to_go.seconds / 60)
                secs = int(time_to_go.seconds % 60)
                self.countdown_lbl.text = "{}m {}s".format(mins, secs)

                self.start_btn.enabled = False
                self.pause_btn.enabled = True
                self.complete_btn.enabled = True
                self.cancel_btn.enabled = True

            elif now < self.segment.end_break_time():

                # Break time
                self.stage_lbl.text = "Break Time..."

                time_to_go = self.segment.end_break_time() - now
                mins = int(time_to_go.seconds / 60)
                secs = int(time_to_go.seconds % 60)
                self.countdown_lbl.text = "{}m {}s".format(mins, secs)

                self.start_btn.enabled = False
                self.pause_btn.enabled = True
                self.complete_btn.enabled = True
                self.cancel_btn.enabled = True

            else:

                # Done
                self.stage_lbl.text = "Done!"
                self.countdown_lbl.text = "0m 0s"

                self.start_btn.enabled = False
                self.pause_btn.enabled = False
                self.complete_btn.enabled = False
                self.cancel_btn.enabled = False

    def start_segment(self):
        """Start the focus segment by starting the `segment` object with the
        current time."""

        self.segment.start_now()
        self.update()
