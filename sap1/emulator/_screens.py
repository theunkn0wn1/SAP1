from asciimatics.effects import Print
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import ManagedScreen
from asciimatics.widgets import Frame, Layout, Button, Label, Divider

from ._runtime import Computer

ADDRESS_COL = 0
RAM_VAL_COL = 1
COMPONENT_LABEL_COL = 2
COMPONENT_VAL_COL = 3
ALLIGN = "^"


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

        component_layout = Layout(
            [RAM_VAL_COL, COMPONENT_VAL_COL, COMPONENT_LABEL_COL, COMPONENT_VAL_COL])
        self.add_layout(component_layout)
        component_layout.add_widget(Label("Address", align=ALLIGN), ADDRESS_COL)
        component_layout.add_widget(Label("Value", align=ALLIGN), RAM_VAL_COL)
        component_layout.add_widget(Label("Component", align=ALLIGN), COMPONENT_LABEL_COL)
        component_layout.add_widget(Label("Value", align=ALLIGN), COMPONENT_VAL_COL)

        for key in self.computer.ram.memory:
            self.add_label(component_layout, key, ADDRESS_COL)
            self.add_label(component_layout, self.computer.ram.memory[key], RAM_VAL_COL)

        self.add_label(component_layout, "Program Counter", COMPONENT_LABEL_COL)
        self.add_label(component_layout, self.computer.program_counter.count, COMPONENT_VAL_COL)

        self.add_label(component_layout, "A Register", COMPONENT_LABEL_COL)
        self.add_label(component_layout, self.computer.register_a.memory, COMPONENT_VAL_COL)

        self.add_label(component_layout, "B Register", COMPONENT_LABEL_COL)
        self.add_label(component_layout, self.computer.register_b.memory, COMPONENT_VAL_COL)

        self.add_label(component_layout, "Output Register", COMPONENT_LABEL_COL)
        self.add_label(component_layout, self.computer.output_register.memory, COMPONENT_VAL_COL)

        self.add_label(component_layout, "ALU", COMPONENT_LABEL_COL)
        self.add_label(component_layout, self.computer.alu.value, COMPONENT_VAL_COL)

        self.add_label(component_layout, "IR raw", COMPONENT_LABEL_COL)
        self.add_label(component_layout, self.computer.instruction_register.memory, COMPONENT_VAL_COL)

        self.add_label(component_layout, "IR opcode", COMPONENT_LABEL_COL)
        self.add_label(component_layout, self.computer.instruction_register.opcode, COMPONENT_VAL_COL)

        self.add_label(component_layout, "IR operand", COMPONENT_LABEL_COL)
        self.add_label(component_layout, self.computer.instruction_register.operand, COMPONENT_VAL_COL)
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Divider(), 0)
        layout2.add_widget(Divider(), 1)

        layout2.add_widget(Button("go back", on_click=self.on_click))

        self.fix()

    def add_label(self, layout, value, col):
        layout.add_widget(Label(value, align=ALLIGN), col)

    @property
    def computer(self) -> Computer:
        return self._computer

    def on_click(self):
        raise NextScene("Main")

    ...
