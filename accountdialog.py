from PySide.QtGui import QDialog, QIntValidator

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
        self.model.username = self.usernameEdit.text()
        self.model.password = self.passwordEdit.text()

        self.model.capKB = self.capEdit.text()
        self.model.start = self.fromDate.date()
        self.model.end = self.toDate.date()

        super(AccountDialog, self).accept()

