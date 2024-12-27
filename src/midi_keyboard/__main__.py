import contextlib
import sys

import mido
from evdev import UInput
from evdev import ecodes as e

VALUE_PUSH = 127
KEY_DOWN = 1
KEY_UP = 0


CONTROL_PEDAL_SOSTENUTO = 67
CONTROL_PEDAL_SOFT = 66


class Mapper:
    def __init__(self, midi_input_name, mapping):
        self.ui = UInput()
        self.mapping = mapping
        self.midi_port = mido.open_input(midi_input_name)

    def _key_press(self, key):
        self.ui.write(e.EV_KEY, key, KEY_DOWN)
        self.ui.write(e.EV_KEY, key, KEY_UP)
        self.ui.syn()

    def run(self):
        while True:
            for msg in self.midi_port.iter_pending():
                if msg.type == 'control_change' and msg.value == VALUE_PUSH and msg.control in self.mapping:
                    self._key_press(self.mapping[msg.control])

    def stop(self):
        self.midi_port.close()
        self.ui.close()


def select_midi_port():
    print('Available MIDI Input Ports:')
    ports = mido.get_input_names()
    for i, port in enumerate(ports):
        print(f'{i+1}. {port}')

    n = 0
    while not (0 < n <= len(ports)):
        with contextlib.suppress(ValueError):
            n = int(input('Select the port: '))

    return ports[n - 1]


if __name__ == '__main__':
    m = Mapper(
        select_midi_port(),
        {CONTROL_PEDAL_SOSTENUTO: e.KEY_PAGEUP, CONTROL_PEDAL_SOFT: e.KEY_PAGEDOWN},
    )
    with contextlib.suppress(KeyboardInterrupt):
        m.run()
    m.stop()
    sys.exit(0)
