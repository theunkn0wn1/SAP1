from asciimatics.effects import Print
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import ManagedScreen
from asciimatics.widgets import Frame, Layout, Button, Label


def run_menu_system():
    banner = FigletText("SAP-1 Emulator", font="doom")
    with ManagedScreen() as screen:
        scenes = [
            Scene([
                Print(screen, banner, 0, colour=screen.COLOUR_GREEN, attr=screen.A_BOLD),
                Main(screen, 35, 110, y=10),
            ], name="Main"),

            Scene([
                Print(screen, banner, 0, colour=screen.COLOUR_GREEN, attr=screen.A_BOLD),
                HardwareView(screen, 35, 100, y=10),
            ],
                name="HardwareView")
        ]

        screen.play(scenes)
        screen.refresh()


class Main(Frame):

    def __init__(self, screen, height, width, data=None, on_load=None, has_border=True,
                 hover_focus=False, name=None, title=None, x=None, y=None, has_shadow=False,
                 reduce_cpu=False, is_modal=False, can_scroll=True):
        super().__init__(screen, height, width, data, on_load, has_border, hover_focus, name, title, x,
                         y, has_shadow, reduce_cpu, is_modal, can_scroll)

        # Create the form for displaying the list of contacts.
        layout = Layout([6], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("SAP-1 Emulator Version 0.0.0 by Joshua (Theunkn0wn1) Salzedo"))
        layout.add_widget(Button("Load Program...", on_click=self.on_view_memory))
        layout.add_widget(Button("View hardware...", on_click=self.on_view_hardware))
        layout.add_widget(Button("Advanced options...", on_click=...))
        layout.add_widget(Button("Execute program", on_click=...))
        layout.add_widget(Button("Reset", on_click=...))

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

    def on_view_hardware(self):
        raise NextScene("HardwareView")

    def _ok(self):
        self.save()
        raise StopApplication("goodbye")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


class MemoryView(Frame):

    def __init__(self, screen, height, width, data=None, on_load=None, has_border=True,
                 hover_focus=False, name=None, title=None, x=None, y=None, has_shadow=False,
                 reduce_cpu=False, is_modal=False, can_scroll=True):
        super().__init__(screen, height, width, data, on_load, has_border, hover_focus, name, title, x,
                         y, has_shadow, reduce_cpu, is_modal, can_scroll)
        self.fix()


class HardwareView(Frame):
    def __init__(self, screen, height, width, data=None, on_load=None, has_border=True,
                 hover_focus=False, name=None, title=None, x=None, y=None, has_shadow=False,
                 reduce_cpu=False, is_modal=False, can_scroll=True):
        super().__init__(screen, height, width, data, on_load, has_border, hover_focus, name, title, x,
                         y, has_shadow, reduce_cpu, is_modal, can_scroll)

        layout = Layout([2])
        self.add_layout(layout)

        layout.add_widget(Button("go back", on_click=self.on_click))
        self.fix()

    def on_click(self):
        raise NextScene("Main")

    ...


if __name__ == "__main__":
    run_memu_system()
