# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddAdvancedRule.ui'
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

class Ui_AddAdvancedRule(object):
    def setupUi(self, AddAdvancedRule):
        AddAdvancedRule.setObjectName(_fromUtf8("AddAdvancedRule"))
        AddAdvancedRule.resize(754, 233)
        self.verticalLayout_2 = QtGui.QVBoxLayout(AddAdvancedRule)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(AddAdvancedRule)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.lineEdit)
        self.rulesLabel = QtGui.QLabel(self.groupBox)
        self.rulesLabel.setObjectName(_fromUtf8("rulesLabel"))
        self.verticalLayout.addWidget(self.rulesLabel)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(AddAdvancedRule)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.accountFromEdit = CompleteLineEdit(self.groupBox_2)
        self.accountFromEdit.setObjectName(_fromUtf8("accountFromEdit"))
        self.gridLayout.addWidget(self.accountFromEdit, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.accountToEdit = CompleteLineEdit(self.groupBox_2)
        self.accountToEdit.setObjectName(_fromUtf8("accountToEdit"))
        self.gridLayout.addWidget(self.accountToEdit, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.groupBox_2)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox, 2, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.buttonBox = QtGui.QDialogButtonBox(AddAdvancedRule)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(AddAdvancedRule)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddAdvancedRule.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddAdvancedRule.reject)
        QtCore.QMetaObject.connectSlotsByName(AddAdvancedRule)

    def retranslateUi(self, AddAdvancedRule):
        AddAdvancedRule.setWindowTitle(_translate("AddAdvancedRule", "Add Advanced Rule", None))
        self.groupBox.setTitle(_translate("AddAdvancedRule", "Pattern", None))
        self.rulesLabel.setText(_translate("AddAdvancedRule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Insert</span><span style=\" font-size:8pt;\">   </span><a href=\"amountLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">amount &gt; 400</span></a><span style=\" font-size:10pt;\">    </span><a href=\"dateLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">date &gt; 3/25/11</span></a><span style=\" font-size:10pt;\">   </span><a href=\"fromPathLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">from contains &quot;bank&quot;</span></a><span style=\" font-size:10pt;\">    </span><a href=\"toPathLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">to contains &quot;bank&quot;</span></a><span style=\" font-size:10pt;\">   </span><a href=\"descLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">desc contains &quot;blah&quot;</span></a><span style=\" font-size:10pt;\">   </span><a href=\"orLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">() or ()</span></a><span style=\" font-size:10pt;\">   </span><a href=\"andLink\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">() and ()</span></a></p></body></html>", None))
        self.groupBox_2.setTitle(_translate("AddAdvancedRule", "Actions", None))
        self.label.setText(_translate("AddAdvancedRule", "Account From", None))
        self.label_2.setText(_translate("AddAdvancedRule", "AccountTo", None))
        self.label_3.setText(_translate("AddAdvancedRule", "Duplicate", None))
        self.comboBox.setItemText(0, _translate("AddAdvancedRule", "No change", None))
        self.comboBox.setItemText(1, _translate("AddAdvancedRule", "Yes", None))
        self.comboBox.setItemText(2, _translate("AddAdvancedRule", "No", None))

from CompleteLineEdit import CompleteLineEdit
