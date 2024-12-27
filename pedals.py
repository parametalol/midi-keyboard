import mido
from evdev import UInput, ecodes as e

VALUE_PUSH = 127
KEY_DOWN = 1
KEY_UP = 0

CONTROL_PEDAL_SOSTENUTO = 67
CONTROL_PEDAL_SOFT = 66


def run(midi_input_name, mapping):
    ui = UInput()

    midi_port = mido.open_input(midi_input_name)
    try:
        while True:
            for msg in midi_port.iter_pending():
                if (
                    msg.type == "control_change"
                    and msg.value == VALUE_PUSH
                    and msg.control in mapping
                ):
                    key = mapping[msg.control]
                    ui.write(e.EV_KEY, key, KEY_DOWN)
                    ui.write(e.EV_KEY, key, KEY_UP)
                    ui.syn()

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        midi_port.close()
        ui.close()


def select_midi_port():
    print("Available MIDI Input Ports:")
    ports = mido.get_input_names()
    for i, port in enumerate(ports):
        print(f"{i+1}. {port}")

    n = 0
    while not (0 < n <= len(ports)):
        try:
            n = int(input("Select the port: "))
        except ValueError:
            pass

    return ports[n - 1]


run(
    select_midi_port(),
    {CONTROL_PEDAL_SOSTENUTO: e.KEY_PAGEUP, CONTROL_PEDAL_SOFT: e.KEY_PAGEDOWN},
)
