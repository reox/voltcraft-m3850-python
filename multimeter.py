#!/usr/bin/env python3
"""
Copyright (C) 2020 Sebastian Bachmann <hello@reox.at>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import serial
import time
from struct import unpack
import math
import sys

with serial.Serial('/dev/ttyUSB0',
                   # Settings according to manual
                   baudrate=1200,
                   bytesize=serial.SEVENBITS,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_TWO,
                   # Extra timeout setting, otherwise blocking
                   timeout=1) as ser:

    # From https://github.com/Ostheer/Voltcraft_ME-32_RS-232
    # Must set those two lines, for powering the optocouplers:
    ser.setRTS(False)  # Set RTS to -12V
    ser.setDTR(True)   # Set DTR to +12V

    # Assume the meter is in COM mode. In that mode, it will send stuff automatically.

    # Skip the first maybe garbled stuff
    x = None
    # FIXME: Sometimes there is no \r...
    # This seems to be the case in the temperature modes!
    while x != '\r':
        x = ser.read(size=1).decode('ascii')
        print(x, end='')
        sys.stdout.flush()
    print()

    last = 0
    while True:
        line = ser.read(size=14).decode('ascii')
        if len(line) != 14:
            print("not read a full line?", file=sys.stderr)
            continue

        mode = line[0:3].strip(' ')
        if 'L' in line[3:9]:
            # Value 0.L --> infinite ohm reading
            value = math.inf
        else:
            try:
                value = float(line[3:9])
            except ValueError:
                # Might happen on error or if in LOGIC mode
                value = math.nan
        unit = line[9:13].strip(' ')
        if line[-1] != '\r':
            print('uh oh!', file=sys.stderr)

        print(time.time(), mode, value, unit)


