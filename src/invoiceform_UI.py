# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/invoiceform.ui'
#
# Created: Sun Aug  7 04:14:38 2011
#      by: pyside-uic 0.2.9 running on PySide 1.0.5
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_InvoiceDialog(object):
    def setupUi(self, InvoiceDialog):
        InvoiceDialog.setObjectName("InvoiceDialog")
        InvoiceDialog.resize(533, 455)
        self.gridLayout = QtGui.QGridLayout(InvoiceDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView = QtGui.QTableView(InvoiceDialog)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 3)
        self.progressBar = QtGui.QProgressBar(InvoiceDialog)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(206, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.updateButton = QtGui.QPushButton(InvoiceDialog)
        self.updateButton.setObjectName("updateButton")
        self.gridLayout.addWidget(self.updateButton, 1, 2, 1, 1)

        self.retranslateUi(InvoiceDialog)
        QtCore.QMetaObject.connectSlotsByName(InvoiceDialog)

    def retranslateUi(self, InvoiceDialog):
        InvoiceDialog.setWindowTitle(QtGui.QApplication.translate("InvoiceDialog", "Invoice", None, QtGui.QApplication.UnicodeUTF8))
        self.updateButton.setText(QtGui.QApplication.translate("InvoiceDialog", "&Update", None, QtGui.QApplication.UnicodeUTF8))

