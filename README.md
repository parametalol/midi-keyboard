# MIDI to Keyboard event mapper

The hardcoded mapping translates the Una Corda (Soft) and Sostenuto (Sustain) pedal pushes to Page Up and Page Down events accordingly.

## Requirements
* Python
* mido
* evdev

## Usage

```console
sh$ python pedals.py 
Available MIDI Input Ports:
1. Midi Through:Midi Through Port-0 14:0
2. Clavinova:Clavinova MIDI 1 32:0
Select the port: 2
^C
```
