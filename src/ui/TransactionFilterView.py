# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TransactionFilterView.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TransactionFilterView(object):
    def setupUi(self, TransactionFilterView):
        TransactionFilterView.setObjectName(_fromUtf8("TransactionFilterView"))
        TransactionFilterView.resize(880, 653)
        self.verticalLayout_3 = QtGui.QVBoxLayout(TransactionFilterView)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.transactionTableView = TransactionTableView(TransactionFilterView)
        self.transactionTableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.transactionTableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.transactionTableView.setObjectName(_fromUtf8("transactionTableView"))
        self.verticalLayout_3.addWidget(self.transactionTableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ruleTextEdit = QtGui.QLineEdit(TransactionFilterView)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(10)
        self.ruleTextEdit.setFont(font)
        self.ruleTextEdit.setObjectName(_fromUtf8("ruleTextEdit"))
        self.verticalLayout.addWidget(self.ruleTextEdit)
        self.rulesLabel = QtGui.QLabel(TransactionFilterView)
        self.rulesLabel.setObjectName(_fromUtf8("rulesLabel"))
        self.verticalLayout.addWidget(self.rulesLabel)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.applyButton = QtGui.QPushButton(TransactionFilterView)
        self.applyButton.setObjectName(_fromUtf8("applyButton"))
        self.verticalLayout_2.addWidget(self.applyButton)
        self.resetButton = QtGui.QPushButton(TransactionFilterView)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.verticalLayout_2.addWidget(self.resetButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(TransactionFilterView)
        QtCore.QMetaObject.connectSlotsByName(TransactionFilterView)

    def retranslateUi(self, TransactionFilterView):
        TransactionFilterView.setWindowTitle(_translate("TransactionFilterView", "Form", None))
        self.rulesLabel.setText(_translate("TransactionFilterView", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Insert</span><span style=\" font-size:8pt;\">   </span><a href=\"amountLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">amount &gt; 400</span></a><span style=\" font-size:10pt;\">    </span><a href=\"dateLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">date &gt; 3/25/11</span></a><span style=\" font-size:10pt;\">   </span><a href=\"fromPathLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">from contains &quot;bank&quot;</span></a><span style=\" font-size:10pt;\">    </span><a href=\"toPathLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">to contains &quot;bank&quot;</span></a><span style=\" font-size:10pt;\">   </span><a href=\"descLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">desc contains &quot;blah&quot;</span></a><span style=\" font-size:10pt;\">   </span><a href=\"orLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">() or ()</span></a><span style=\" font-size:10pt;\">   </span><a href=\"andLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">() and ()</span></a></p></body></html>", None))
        self.applyButton.setText(_translate("TransactionFilterView", "Apply", None))
        self.resetButton.setText(_translate("TransactionFilterView", "Reset", None))

from TransactionTableView import TransactionTableView
