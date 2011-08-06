#!/usr/bin/env python

import sys
import signal

from PySide.QtGui import QApplication

from mainwindow import MainWindow

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

