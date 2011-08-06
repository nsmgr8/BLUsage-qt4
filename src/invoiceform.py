from PySide.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide.QtGui import QDialog, QHeaderView, QMessageBox, QAbstractItemView
from PySide.QtCore import QUrl

from invoiceform_UI import Ui_InvoiceDialog

from invoice import Invoice

class InvoiceForm(QDialog, Ui_InvoiceDialog):

    def __init__(self, parent=None):
        super(InvoiceForm, self).__init__(parent)
        self.setupUi(self)
        self.progressBar.setHidden(True)

        self.invoice = Invoice(self)
        self.tableView.setModel(self.invoice)
        self.tableView.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.updateButton.clicked.connect(self.updateInvoice)

        self.network_access_manager = QNetworkAccessManager()
        self.network_access_manager.finished.connect(self.fetched_invoices)
        self.network_access_manager.sslErrors.connect(self.allow_connection)

    def updateInvoice(self):
        usage = self.parentWidget().usage_model
        request = QNetworkRequest(QUrl('%s?%s' % (usage.user_endpoint, self.invoice.post_data)))
        self.network_access_manager.get(request)
        self.updateButton.setEnabled(False)
        self.progressBar.setHidden(False)

    def fetched_invoices(self, reply):
        self.updateButton.setEnabled(True)
        self.progressBar.setHidden(True)
        if reply.error() == QNetworkReply.NoError:
            html = unicode(reply.readAll())
            self.invoice.parse(html)
            self.invoice.reset()
        else:
            title = "An error occured"
            message = reply.errorString() \
                    + ".\nPlease check your internet connection."

            QMessageBox.critical(self, title, message)
        reply.deleteLater()

    def allow_connection(self, reply):
        reply.ignoreSslErrors()

