#!/usr/bin/env python

import os
import sys
import signal
import logging

from PySide.QtGui import QApplication

from mainwindow import MainWindow

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        os.mkdir(os.path.expanduser('~/.blusage'))
    except Exception as e:
        logging.debug(e)
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

