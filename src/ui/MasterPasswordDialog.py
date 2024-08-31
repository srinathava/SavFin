# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MasterPasswordDialog.ui'
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

class Ui_MasterPasswordDialog(object):
    def setupUi(self, MasterPasswordDialog):
        MasterPasswordDialog.setObjectName(_fromUtf8("MasterPasswordDialog"))
        MasterPasswordDialog.resize(400, 170)
        self.verticalLayout_2 = QtGui.QVBoxLayout(MasterPasswordDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(MasterPasswordDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.passwordLabel = QtGui.QLabel(MasterPasswordDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLineEdit = QtGui.QLineEdit(MasterPasswordDialog)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName(_fromUtf8("passwordLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.passwordLineEdit)
        self.confirmPasswordLabel = QtGui.QLabel(MasterPasswordDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.confirmPasswordLabel.setFont(font)
        self.confirmPasswordLabel.setObjectName(_fromUtf8("confirmPasswordLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.confirmPasswordLabel)
        self.confirmPasswordLineEdit = QtGui.QLineEdit(MasterPasswordDialog)
        self.confirmPasswordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.confirmPasswordLineEdit.setObjectName(_fromUtf8("confirmPasswordLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.confirmPasswordLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.statusLabel = QtGui.QLabel(MasterPasswordDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.statusLabel.setFont(font)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.verticalLayout.addWidget(self.statusLabel)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtGui.QSpacerItem(20, 39, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.okButton = QtGui.QPushButton(MasterPasswordDialog)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(MasterPasswordDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(MasterPasswordDialog)
        QtCore.QMetaObject.connectSlotsByName(MasterPasswordDialog)
        MasterPasswordDialog.setTabOrder(self.passwordLineEdit, self.confirmPasswordLineEdit)
        MasterPasswordDialog.setTabOrder(self.confirmPasswordLineEdit, self.okButton)
        MasterPasswordDialog.setTabOrder(self.okButton, self.cancelButton)

    def retranslateUi(self, MasterPasswordDialog):
        MasterPasswordDialog.setWindowTitle(_translate("MasterPasswordDialog", "Set Master Password", None))
        self.label.setText(_translate("MasterPasswordDialog", "You will be asked this password everytime you open the file", None))
        self.passwordLabel.setText(_translate("MasterPasswordDialog", "Password", None))
        self.confirmPasswordLabel.setText(_translate("MasterPasswordDialog", "Confirm Password", None))
        self.statusLabel.setText(_translate("MasterPasswordDialog", "Status:", None))
        self.okButton.setText(_translate("MasterPasswordDialog", "OK", None))
        self.cancelButton.setText(_translate("MasterPasswordDialog", "Cancel", None))

