#!/usr/bin/env python

import os
import sys
import signal
import logging
import logging.handlers

from PySide.QtGui import QApplication

from mainwindow import MainWindow

def set_logger():
    debug_file = os.path.expanduser('~/.blusage.debug.log')
    logger = logging.getLogger('BLUsage')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(debug_file, maxBytes=1000, backupCount=5)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


def main():
    logger = logging.getLogger('BLUsage')
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        os.mkdir(os.path.expanduser('~/.blusage'))
    except Exception as e:
        logger.debug(e)
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    if os.environ.get('DEBUG', '') == 'TRUE':
        set_logger()
    main()

