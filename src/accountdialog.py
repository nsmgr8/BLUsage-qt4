from PySide.QtGui import QDialog, QIntValidator, QMessageBox

from accountdialog_UI import Ui_AccountDialog

class AccountDialog(QDialog, Ui_AccountDialog):

    def __init__(self, model, parent=None):
        super(AccountDialog, self).__init__(parent)
        self.setupUi(self)

        self.capEdit.setValidator(QIntValidator(0, 100000000, self))

        self.accountNameEdit.setText(model.name)
        self.usernameEdit.setText(model.username)
        self.passwordEdit.setText(model.password)

        self.capEdit.setText(str(model.capKB))
        self.fromDate.setDate(model.start)
        self.toDate.setDate(model.end)

        self.model = model

    def accept(self):
        self.model.name = self.accountNameEdit.text()
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        if not all([username, password]):
            QMessageBox.critical(self, "Username & Password",
                                "Both the username and password are required.")
            if not username:
                self.usernameEdit.setFocus()
            else:
                self.passwordEdit.setFocus()
            return
        self.model.username = username
        self.model.password = password

        try:
            self.model.capKB = int(self.capEdit.text() or 0)
        except ValueError:
            QMessageBox.critical(self, "Invalid value",
                                 "Please enter a number in KB for the capacity.")
            self.capEdit.setFocus()
            return

        self.model.start = self.fromDate.date()
        self.model.end = self.toDate.date()

        super(AccountDialog, self).accept()

