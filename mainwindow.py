import os
import urllib
import datetime

from PySide.QtCore import QUrl, QSettings
from PySide.QtGui import QMainWindow, QMessageBox, QIcon
from PySide.QtNetwork import (QNetworkAccessManager, QNetworkRequest,
                              QNetworkReply)

from blusage import BLUsage
from treemodel import TreeModel

from accountdialog import AccountDialog
from mainwindow_UI import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(':/blusage.png'))

        self.action_Account.triggered.connect(self.show_account_editor)
        self.action_Update.triggered.connect(self.update_usage)
        self.action_About.triggered.connect(self.about)

        self.network_access_manager = QNetworkAccessManager()
        self.network_access_manager.finished.connect(self.fetched_usages)
        self.network_access_manager.sslErrors.connect(self.allow_connection)

        self.settings = QSettings('Nasim', 'BLUsage')
        self.file_name = os.path.expanduser('~/.BLUsage.dat')

        self.usage_model = BLUsage()
        self.read_usage()
        self.tree_model = TreeModel(self.usage_model.usage)

        self.treeView.setModel(self.tree_model)
        self.treeView.resizeColumnToContents(0)

        if not self.usage_model.username:
            self.show_account_editor()

        self.treeView.setAlternatingRowColors(True)
        self.accountName.setText(self.usage_model.name)
        self.progressBar.setHidden(True)
        self.show_lastupdate()

    def show_account_editor(self):
        AccountDialog(self.usage_model, self).exec_()
        self.accountName.setText(self.usage_model.name)
        self.show_lastupdate()
        self.write_usage()

    def about(self):
        QMessageBox.about(self, "BLUsage", "Bangla Lion bandwidth usage viewer.\n\n\tVersion 1.0\n\nAuthor: M. Nasimul Haque\n\nemail: nasim.haque@gmail.com\n\nWeb: http://www.nasim.me.uk")

    def update_usage(self):
        if not all([self.usage_model.username, self.usage_model.password]):
            QMessageBox.critical(self, 'No account',
                                 'Please enter your account details first.')
            return

        url = QUrl("https://%s:%s@care.banglalionwimax.com/User" %
                   (self.usage_model.username, self.usage_model.password))
        post_data = urllib.urlencode({
            'Page': 'UsrSesHit',
            'Title': 'Session Calls',
            'UserID': self.usage_model.username,
            'StartDate': self.usage_model.start.toString("dd/MM/yyyy"),
            'EndDate': self.usage_model.end.toString("dd/MM/yyyy"),
            'Submit': 'Submit',
        })

        request = QNetworkRequest(url)
        self.network_access_manager.post(request, post_data)

        self.updateButton.setEnabled(False)
        self.progressBar.setHidden(False)
        self.progressBar.setValue(0)
        self.statusBar.showMessage("Please wait...")

    def fetched_usages(self, reply):
        self.updateButton.setEnabled(True)
        self.progressBar.setHidden(True)

        if reply.error() == QNetworkReply.NoError:
            if not self.usage_model.parse(str(reply.readAll())):
                title = "Parsing error"
                message = self.usage_model.error
            else:
                title = None
                self.tree_model.deleteLater()
                self.tree_model = TreeModel(self.usage_model.usage)
                self.treeView.setModel(self.tree_model)
                self.treeView.resizeColumnToContents(0)
                self.show_lastupdate()
                self.write_usage()
        elif reply.error() in [QNetworkReply.AuthenticationRequiredError,
                               QNetworkReply.ContentAccessDenied]:
            title = "Authentication error"
            message = "Please check your account credentials."
        else:
            title = "An error occured"
            message = reply.errorString() \
                    + ".\nPlease check your internet connection."

        if title:
            QMessageBox.critical(self, title, message)
        reply.deleteLater()

    def allow_connection(self, reply):
        reply.ignoreSslErrors()

    def read_usage(self):
        self.usage_model.name = self.settings.value('name')
        self.usage_model.username = self.settings.value('username')
        self.usage_model.password = self.settings.value('password')
        self.usage_model.last_update = self.settings.value('last_update')
        self.usage_model.capKB = int(self.settings.value('cap') or 0)
        self.usage_model.totalKB = int(self.settings.value('total') or 0)

        start = self.settings.value('start')
        if not start:
            today = datetime.date.today()
            start = datetime.date(year=today.year, month=today.month, day=1)
        self.usage_model.start = start
        end = self.settings.value('end')
        if not end:
            end = start + datetime.timedelta(days=29)
        self.usage_model.end = end

    def write_usage(self):
        self.settings.setValue('name', self.usage_model.name)
        self.settings.setValue('username', self.usage_model.username)
        self.settings.setValue('password', self.usage_model.password)
        self.settings.setValue('start', self.usage_model.start)
        self.settings.setValue('end', self.usage_model.end)
        self.settings.setValue('last_update', self.usage_model.last_update)
        self.settings.setValue('cap', self.usage_model.capKB)
        self.settings.setValue('total', self.usage_model.totalKB)

    def show_lastupdate(self):
        if not self.usage_model.last_update:
            self.statusBar.showMessage("Ready")
        else:
            self.totalLabel.setText("Totals usage: <b>%s</b>" %
                    (self.usage_model.smart_bytes(self.usage_model.totalKB),))
            remaining = self.usage_model.remaining()
            if isinstance(remaining, int):
                self.remainingLabel.setText("Remaining: <b>%s</b>" %
                        (self.usage_model.smart_bytes(remaining),))
            else:
                self.remainingLabel.setText("Remaining: <b>Unlimited</b>")

            self.statusBar.showMessage("Last updated on: " +
                    self.usage_model.last_update.strftime("%d %b %Y, %H:%M"))

import resources

