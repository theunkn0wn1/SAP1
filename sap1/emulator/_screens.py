import pathlib

from asciimatics.effects import Print
from asciimatics.exceptions import NextScene, StopApplication
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import ManagedScreen
from asciimatics.widgets import Frame, Layout, Button, Label, Divider, FileBrowser

from ._runtime import Computer, load_memory_from_buffer

ADDRESS_COL = 0
RAM_VAL_COL = 1
COMPONENT_LABEL_COL = 2
COMPONENT_VAL_COL = 3
ALLIGN = "^"


def run_menu_system(computer: Computer):
    banner = FigletText("SAP-1 Emulator", font="doom")
    with ManagedScreen() as screen:
        banner_frame = Print(screen, banner, 0, colour=screen.COLOUR_GREEN, attr=screen.A_BOLD)
        scenes = [
            Scene([
                banner_frame,
                Main(computer, screen, 35, 110, y=10),
            ], name="Main"),

            Scene([
                banner_frame,
                HardwareView(computer, screen, 35, 110, y=10),
            ],
                name="HardwareView"),
            Scene([
                banner_frame,
                LoadMemory(computer, screen, 35, 110, y=10)
            ], name="LoadMemory")
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
        layout.add_widget(Button("Load Program...", on_click=self.on_load_memory))
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

    def on_load_memory(self):
        raise NextScene("LoadMemory")

    def on_view_hardware(self):
        raise NextScene("HardwareView")

    def _ok(self):
        self.save()
        raise StopApplication("goodbye")

    @staticmethod
    def _cancel():
        raise StopApplication("cancel")


class HardwareView(Frame):
    def __init__(self, computer: Computer, screen, height, width, data=None, on_load=None,
                 has_border=True,
                 hover_focus=False, name=None, title=None, x=None, y=None, has_shadow=False,
                 reduce_cpu=False, is_modal=False, can_scroll=True):
        super().__init__(screen, height, width, data, self.on_load, has_border, hover_focus, name,
                         title, x,
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

        layout2 = Layout([5, 5])
        self.add_layout(layout2)
        layout2.add_widget(Divider(), 0)

        self.add_label(layout2, "Control Word", 0)
        self.add_label(layout2, self.computer.program_counter.control_word, 0)

        layout2.add_widget(Button("go back", on_click=self.on_click), 0)
        layout2.add_widget(Button("refresh", on_click=self.on_refresh), 1)

        self.fix()

    @staticmethod
    def add_label(layout, value, col):
        layout.add_widget(Label(value, align=ALLIGN), col)

    @property
    def computer(self) -> Computer:
        return self._computer

    def on_click(self):
        raise NextScene("Main")

    def on_load(self):
        print(f"{self.on_load} called!")
        self.on_refresh()

    def on_refresh(self):
        print(f"{self.on_refresh} called!")
        self.__init__(self.computer, self.screen, 35, 110, y=20)

    ...


class LoadMemory(Frame):
    """
    Memory loading
    """

    def __init__(self, computer, screen, height, width, data=None, on_load=None, has_border=True,
                 hover_focus=False, name=None, title=None, x=None, y=None, has_shadow=False,
                 reduce_cpu=False, is_modal=False, can_scroll=True):
        super().__init__(screen, height, width, data, on_load, has_border, hover_focus, name, title, x,
                         y, has_shadow, reduce_cpu, is_modal, can_scroll)

        self._computer = computer

        main_layout = Layout([1])
        self.add_layout(main_layout)

        main_layout.add_widget(FileBrowser(10, ".", file_filter=r".*.sap1$",
                                           name="fileSelector", on_select=self.on_select
                                           ))

        self.fix()

    @property
    def computer(self) -> Computer:
        return self._computer

    def on_select(self):
        widget = self.find_widget("fileSelector")
        target = pathlib.Path(widget.value)
        target.resolve(strict=True)
        load_memory_from_buffer(target.read_text().rstrip("\n"), self.computer.mar, self.computer.ram)
        raise NextScene("Main")
