import time

from asciimatics.effects import Print
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import ManagedScreen
from asciimatics.widgets import Frame, Layout, Button


def demo():
    banner = FigletText("SAP-1 Emulator", font="doom")
    with ManagedScreen() as screen:
        effects = [
            Print(screen, banner, 0, colour=screen.COLOUR_GREEN, attr=screen.A_BOLD),
            Main(screen, 35, 120,y=10)
        ]
        screen.play([Scene(effects)])
        screen.refresh()
        time.sleep(2)


class Main(Frame):

    def __init__(self, screen, height, width, data=None, on_load=None, has_border=True,
                 hover_focus=False, name=None, title=None, x=None, y=None, has_shadow=False,
                 reduce_cpu=False, is_modal=False, can_scroll=True):
        super().__init__(screen, height, width, data, on_load, has_border, hover_focus, name, title, x,
                         y, has_shadow, reduce_cpu, is_modal, can_scroll)

        # Create the form for displaying the list of contacts.
        layout = Layout([4,2], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Button("View Memory", on_click=self.on_view_memory))
        layout.add_widget(Button("View hardware", on_click=self.on_view_memory))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("QUIT", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super().reset()

    def on_view_memory(self):
        raise NextScene("MemoryView")

    def _ok(self):
        self.save()
        raise StopApplication("goodbye")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


class MemoryView(Frame):
    ...


demo()
