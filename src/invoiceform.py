import os

from PySide.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide.QtGui import QDialog, QHeaderView, QMessageBox, QAbstractItemView, QImage, QPainter
from PySide.QtCore import Qt, QUrl, QSize
from PySide.QtWebKit import QWebPage

from invoiceform_UI import Ui_InvoiceDialog

from invoice import Invoice

class InvoiceForm(QDialog, Ui_InvoiceDialog):

    def __init__(self, parent=None):
        super(InvoiceForm, self).__init__(parent)
        self.setupUi(self)
        self.progressBar.setHidden(True)
        self.webpage = QWebPage()

        self.invoice = Invoice(self)
        self.tableView.setModel(self.invoice)
        self.tableView.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.updateButton.clicked.connect(self.update_invoices)
        self.tableView.selectionModel().selectionChanged.connect(self.invoice_selected)
        self.webpage.loadFinished.connect(self.save_invoice)
        self.webpage.networkAccessManager().sslErrors.connect(self.allow_connection)

        self.network_access_manager = QNetworkAccessManager()
        self.network_access_manager.finished.connect(self.fetched_invoices)
        self.network_access_manager.sslErrors.connect(self.allow_connection)

    def invoice_selected(self, new, old):
        try:
            row = self.invoice.invoices[new.indexes()[0].row()]
        except IndexError:
            return
        if row[1].startswith('Invoice'):
            self.invoice_filename = os.path.expanduser('~/.blusage/%s.png' % row[1].lower())
            usage = self.parentWidget().usage_model
            url = '%s%s' % (usage.user_endpoint[:-5], self.invoice.invoices[new.indexes()[0].row()][0])
            self.webpage.mainFrame().load(QUrl(url))
            self.webpage.mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
            self.webpage.mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
            self.webpage.setViewportSize(QSize(800, 600))
            self.enable_ui(False)

    def update_invoices(self):
        usage = self.parentWidget().usage_model
        url = '%s?%s' % (usage.user_endpoint, self.invoice.post_data)
        request = QNetworkRequest(QUrl(url))
        self.network_access_manager.get(request)
        self.enable_ui(False)

    def enable_ui(self, value=True):
        self.updateButton.setEnabled(value)
        self.progressBar.setHidden(value)
        self.tableView.setEnabled(value)

    def save_invoice(self, ok):
        self.enable_ui()
        if ok:
            frame = self.webpage.mainFrame()
            image = QImage(frame.contentsSize(), QImage.Format_ARGB32_Premultiplied)
            image.fill(Qt.transparent);

            painter = QPainter(image)
            painter.setRenderHint(QPainter.Antialiasing, True);
            painter.setRenderHint(QPainter.TextAntialiasing, True);
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True);
            frame.documentElement().render(painter);
            painter.end();

            image.save(self.invoice_filename)
        else:
            title = "An error occured"
            message = "Could not load invoice." \
                    + "\nPlease check your internet connection."

            QMessageBox.critical(self, title, message)

    def fetched_invoices(self, reply):
        self.enable_ui()
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

