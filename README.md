Voltcraft/Metex M-3850 Serial Communication
-------------------------------------------

This is a proof of concept for serial communication with a Voltcraft/METEX M-3850 DMM.

The original manufacturer of the multimeter is METEX.
(you can see the manufacturer name on the PCB as well as on photos in the original Voltraft manual)

Serial configuration as follows:


    +---------------------+
    | VOLTCRAFT    M-3850 |
    | ################### |
    | ################### |
    | ################### |
    |                     |
    | [  ] [  ] [  ] [  ] |
    |                     |
    | [  ] [  ] ()    %%  |
    |                 %%  |
    |      D  F  CAP      |
    |    O      /  hFE    |
    |   A      /     TEMP |
    |  mA     /       TEMP|
    |  V     /       LOGI |
    | mV    /             |           On the Serial Port (Pin on DB9 connector)
    | []                  |
    | []                  |x -------> RXD (2)
    | []                  |x -------> DTR (4)
    |                     |
    |  O    O    O    O   |x -------> RTS (7)
    |                     |x -------> TXD (3)
    |                     |x -------> GND (5)
    +---------------------+

You do not need the serial adapter, as you can build one yourself:
Use 0.6mm thick wire and arange them in 100mil distance, like a 6pin plug.
However leave the third pin empty.
The wire should be about 12mm long to reach into the housing.

In order to communicate with the DMM, switch the multimeter into "COM" mode,
by pressing the FUNCTION button several times.

Then, start this script to start the reading.


It looks like, that the temperature mode sends a wrong format. The CR is missing there,
instead a space is send.
That is bad, as we need to synchronize the reading first, in order to always read a full line.

The manual is wrong for several things.
First of all, a line is not "14 bit" but 14 bytes long.

The dataforamt according to the manual looks like this:
3 bytes Mode name (ASCII)
6 byte Value (ASCII), might contain trailing zeros, or read 0.L, or string (Logic mode)
4 byte Unit (ASCII)
1 byte CR (\r)

However, it looks like that the mode name is only 2 bytes plus a space.
For example, the manual says that the Ohms range will print OHM,
however my meter only prints OH.
The question is if there shall be the space or if the value is actually 7 bytes.

Could find the following Names:

* DC --> mV, V, mA, A Ranges
* AC --> mV, V, mA, A Ranges
* OH --> Ohms Range / Beeper
* DI --> Diode measurement
* FR --> Frequency
* CA --> Capacitor
* HF --> Transistor
* TM --> Temperature
* LO --> Logic Mode (contains strings in the value... also not very useful mode)

The settings for the serial port seems to be correct.
But you need to take special care with the RTS and DTS lines, as seen below in the code.
The hint comes from another script which can read this multimeter.
The reason is, that apparently the optocouplers used in the meter are powered via the serial
line, and thus DTR shall have +12V and RTS -12V.
My USB to serial converter uses +-9.6V, which seems to be fine too.
I'm not sure what other voltages might work, but maybe you could even make it work using a cheap
5V serial to USB converter.

The DMM can not deliver values very fast though.
It looks like it will write a new value to the serial line every ~600 to 750ms.
Even if the measurement is much faster shown on the display.
The manual says it can do up to 10 measurements per second, but the serial seems to be slower.
The time depends on the mode, it looks like that temperature measurement is slowest.


There seems to be two different methods how to get values from the meter:
1) send the D command every time
2) use the COM mode and send it once.

However, it looks like the meter is not very consistent. I could make it work to retrieve a value
without being in the COM mode by sending "D", but that seemed to work only once.
In the COM mode it looks like to be sufficient to send the "D" only one time in the beginning.
But the meter seems to send you values even if you do not send a "D". Maybe you have to activate it
only once for each powering up.
I.e. it works to start the script, read some values, then switch the mode, go back on COM and it will
read more values. However, for the new mode no "D" has been send!
I'm not sure how this works to be honest and the manual does not tell you either...

The meter also has a small bug when switching modes when in COM mode.
As the COM mode is disabled on mode switch, the meter will stop sending lines for the new mode.
However, it might send you one line in the new mode before switching off the COM mode!
Hence, better turn of the serial line before switching modes, if you want to be on the safe side.

