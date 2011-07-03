#!/usr/bin/env python

import sys

from PySide.QtGui import QApplication

from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

