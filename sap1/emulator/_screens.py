from asciimatics.effects import Print
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import ManagedScreen
from asciimatics.widgets import Frame, Layout, Button, Label

from ._runtime import Computer


def run_menu_system():
    banner = FigletText("SAP-1 Emulator", font="doom")
    computer = Computer()
    with ManagedScreen() as screen:
        banner_frame = Print(screen, banner, 0, colour=screen.COLOUR_GREEN, attr=screen.A_BOLD)
        scenes = [
            Scene([
                banner_frame,
                Main(computer, screen, 35, 110, y=10),
            ], name="Main"),

            Scene([
                banner_frame,
                HardwareView(computer, screen, 35, 100, y=10),
            ],
                name="HardwareView"),
        ]

        screen.play(scenes)
        screen.refresh()


class Main(Frame):

    def __init__(self, computer: Computer, screen, height, width, data=None, on_load=None,
                 has_border=True,
                 hover_focus=False, name=None, title=None, x=None, y=None, has_shadow=False,
                 reduce_cpu=False, is_modal=False, can_scroll=True):
        super().__init__(screen, height, width, data, on_load, has_border, hover_focus, name, title, x,
                         y, has_shadow, reduce_cpu, is_modal, can_scroll)
        self._computer = computer
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

    @property
    def computer(self) -> Computer:
        return self._computer

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


class HardwareView(Frame):
    def __init__(self, computer: Computer, screen, height, width, data=None, on_load=None,
                 has_border=True,
                 hover_focus=False, name=None, title=None, x=None, y=None, has_shadow=False,
                 reduce_cpu=False, is_modal=False, can_scroll=True):
        super().__init__(screen, height, width, data, on_load, has_border, hover_focus, name, title, x,
                         y, has_shadow, reduce_cpu, is_modal, can_scroll)
        self._computer = computer

        layout = Layout([1, 3, 2, 4])
        self.add_layout(layout)
        layout.add_widget(Label("Address", align="^"), 0)
        layout.add_widget(Label("Value", align="^"), 1)
        layout.add_widget(Label("Component", align="^"), 2)
        layout.add_widget(Label("Value", align='^'), 3)

        for key in self.computer.ram.memory:
            layout.add_widget(Label(key, align='^'), 0)
            layout.add_widget(Label(self.computer.ram.memory[key], align='^'), 1)
        layout.add_widget(Button("go back", on_click=self.on_click))

        self.fix()

    @property
    def computer(self) -> Computer:
        return self._computer

    def on_click(self):
        raise NextScene("Main")

    ...
