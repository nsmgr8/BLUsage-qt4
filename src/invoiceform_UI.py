# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/invoiceform.ui'
#
# Created: Sun Aug  7 16:21:41 2011
#      by: pyside-uic 0.2.9 running on PySide 1.0.5
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_InvoiceDialog(object):
    def setupUi(self, InvoiceDialog):
        InvoiceDialog.setObjectName("InvoiceDialog")
        InvoiceDialog.resize(550, 460)
        InvoiceDialog.setMinimumSize(QtCore.QSize(550, 460))
        InvoiceDialog.setMaximumSize(QtCore.QSize(900, 16777215))
        self.gridLayout = QtGui.QGridLayout(InvoiceDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(InvoiceDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.tableView = QtGui.QTableView(self.splitter)
        self.tableView.setObjectName("tableView")
        self.scrollArea = QtGui.QScrollArea(self.splitter)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 530, 117))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.invoiceLabel = QtGui.QLabel(self.scrollAreaWidgetContents_2)
        self.invoiceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.invoiceLabel.setObjectName("invoiceLabel")
        self.gridLayout_2.addWidget(self.invoiceLabel, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 3)
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
        self.invoiceLabel.setText(QtGui.QApplication.translate("InvoiceDialog", "Invoice view", None, QtGui.QApplication.UnicodeUTF8))
        self.updateButton.setText(QtGui.QApplication.translate("InvoiceDialog", "&Update", None, QtGui.QApplication.UnicodeUTF8))

