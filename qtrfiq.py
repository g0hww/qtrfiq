#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: qtrfiq.py
# Author: Darren Long, G0HWW
# Description: QT GUI with rigctrl, fosphor and I?Q audio input
# Generated: Wed Oct  7 20:22:32 2015
##################################################

from PyQt4 import Qt
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import fosphor
from gnuradio import gr
from gnuradio import iqbalance
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import subprocess
import sys
import threading
import time

from distutils.version import StrictVersion
class qtrfiq(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "qtrfiq.py")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("qtrfiq.py")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "qtrfiq")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.rig_freq = rig_freq = float(subprocess.check_output(['/usr/bin/rigctl', '-m', '2', 'f']).strip())
        self.samp_rate = samp_rate = 96000
        self.freq = freq = rig_freq
        self.SetSampleRateProbe = SetSampleRateProbe = 1
        self.SetRigFreqProbe = SetRigFreqProbe = 0

        ##################################################
        # Blocks
        ##################################################
        self.iqbalance_optimize_c_0 = iqbalance.optimize_c(1024)
        self.iqbalance_fix_cc_0 = iqbalance.fix_cc(0, 0)
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel("Frequency"+": "))
        self._freq_line_edit = Qt.QLineEdit(str(self.freq))
        self._freq_tool_bar.addWidget(self._freq_line_edit)
        self._freq_line_edit.returnPressed.connect(
        	lambda: self.set_freq(eng_notation.str_to_num(self._freq_line_edit.text().toAscii())))
        self.top_grid_layout.addWidget(self._freq_tool_bar, 0,0,1,1)
        self.fosphor_qt_sink_c_0 = fosphor.qt_sink_c()
        self.fosphor_qt_sink_c_0.set_fft_window(window.WIN_BLACKMAN_hARRIS)
        self.fosphor_qt_sink_c_0.set_frequency_range(rig_freq, samp_rate)
        self._fosphor_qt_sink_c_0_win = sip.wrapinstance(self.fosphor_qt_sink_c_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._fosphor_qt_sink_c_0_win)
        self.dc_blocker_xx_1 = filter.dc_blocker_cc(1024, True)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.audio_source_0 = audio.source(samp_rate, "hw:4,1", True)
        def _SetSampleRateProbe_probe():
            while True:
                val = self.set_samp_rate(self.samp_rate)
                try:
                    self.set_SetSampleRateProbe(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (20))
        _SetSampleRateProbe_thread = threading.Thread(target=_SetSampleRateProbe_probe)
        _SetSampleRateProbe_thread.daemon = True
        _SetSampleRateProbe_thread.start()
        def _SetRigFreqProbe_probe():
            while True:
                val = self.set_rig_freq(float(subprocess.check_output(['/usr/bin/rigctl','-m','2','f']).strip()))
                try:
                    self.set_SetRigFreqProbe(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (5))
        _SetRigFreqProbe_thread = threading.Thread(target=_SetRigFreqProbe_probe)
        _SetRigFreqProbe_thread.daemon = True
        _SetRigFreqProbe_thread.start()

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.iqbalance_optimize_c_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.iqbalance_fix_cc_0, 0))
        self.connect((self.iqbalance_fix_cc_0, 0), (self.dc_blocker_xx_1, 0))
        self.connect((self.dc_blocker_xx_1, 0), (self.fosphor_qt_sink_c_0, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.audio_source_0, 1), (self.blocks_float_to_complex_0, 0))

        ##################################################
        # Asynch Message Connections
        ##################################################
        self.msg_connect(self.iqbalance_optimize_c_0, "iqbal_corr", self.iqbalance_fix_cc_0, "iqbal_corr")

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "qtrfiq")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_rig_freq(self):
        return self.rig_freq

    def set_rig_freq(self, rig_freq):
        self.rig_freq = rig_freq
        self.set_freq(self.rig_freq)
        self.fosphor_qt_sink_c_0.set_frequency_range(self.rig_freq, self.samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.fosphor_qt_sink_c_0.set_frequency_range(self.rig_freq, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        Qt.QMetaObject.invokeMethod(self._freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq)))

    def get_SetSampleRateProbe(self):
        return self.SetSampleRateProbe

    def set_SetSampleRateProbe(self, SetSampleRateProbe):
        self.SetSampleRateProbe = SetSampleRateProbe

    def get_SetRigFreqProbe(self):
        return self.SetRigFreqProbe

    def set_SetRigFreqProbe(self, SetRigFreqProbe):
        self.SetRigFreqProbe = SetRigFreqProbe

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = qtrfiq()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
