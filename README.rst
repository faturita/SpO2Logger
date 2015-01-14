SpO2Logger
==============

|docs|

A Python program for gathering and viewing data from the CMS50 Pulse Oximeter

Installation
------------

::

    Not yet finished 


Usage
-----

::

Connect the Pulse Oximeter and this program will generate dump files.

Protocol
--------

::

Communication protocol(V5.0A)
1.1 Communication settings(for Comm port)：
Data format：
 1 Start bit + 8 data bits + 1 stop bit， odd；
Baudrate ：
 4800 baud (this is the documentation's value, but it is actually 19200)

1.2 Real time data sent to PC from Pulse Oximeter：

  DATA：5 bytes in 1 package，60 packages/second，bit 7 stand for synchronization。 

byte bit content
1
0～3 Signal strength for pulsate(0～8)
4 1＝searching too long，0=OK
5 1＝dropping of SpO2，0=OK
6 1＝beep flag
7 Synchronization,always be 1

2
0～6 pulse waveform data
7 synchronization，always be 0

3
0～3 bar gragh (stand for pulsate case)
4 1＝probe error，0=OK
5 1＝searching，0=OK
6 bit 7 for Pulse Rate
7 synchronization，always be 0


4
0～6 bit 0~bit 6 for Pulse Rate
7 synchronization，always be 0


5
0～6 bit 0~bit 6 for SpO2
7 synchronization，always be 0