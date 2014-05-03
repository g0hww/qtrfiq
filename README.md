qtrfiq
======

A GRC flowgraph and its python script for a QT GUI with a gr-fosphor display 
that uses hamlib's rigctrl and an IQ audio input.

![Screenshot](https://raw.github.com/g0hww/qtrfiq/blob/master/qtrfiq_20140503094737.png)

qtrfiq, pronounced "q terrific", consists of a simple GRC flowgraph and its 
generated python script.  There's nothing at all complicated in the flowgraph,
other than a nifty bodge with a pair of function probe blocks that enables
qtrfiq to poll the radio's frequency using  hamlib's rigctl utility.
To use qtrfiq, you need to have gnuradio and gr-fosphor installed.

gnuradio: http://gnuradio.org/redmine/projects/gnuradio/wiki
gr-fosphor: http://sdr.osmocom.org/trac/wiki/fosphor

There is, however an issue with the generated python code, but it can be easily 
fixed with some editing and will hopefully be fixed in GRC. GRC generates 
invalid code, which then fails to run, for a FunctionProbe block when the
BlockID is empty.  The issue is described in this bug: 

http://gnuradio.org/redmine/issues/668

You can generate the Python script and edit it to remove the superfluous dot 
symbols from the function definitions of _SetSampleRateProbe_probe() and 
_SetRigFreqProbe_probe() that can be found towards the end of the qtrfiq class 
constructor.  I will have probably remembered to do have done this myself when I
have committed the generated python.

The invocation of rigctl is performed in the SetRigFreqProbe FunctionProbe 
block, and it's arguments can be modifed by changing the tuple passed into 
the invocation of subprocess.check() in the block's "Function Args" property.
By default, the arguments use a rig model of 2, corresponding to a rigctld 
server on the default port.

As there is no callback available from the QT fosphor sink, there is no 
click-to-tune capability, or any other means yet to control the radio's
frequency from qtrfiq.
