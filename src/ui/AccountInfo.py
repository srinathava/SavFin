# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AccountInfo.ui'
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

class Ui_AccountInfo(object):
    def setupUi(self, AccountInfo):
        AccountInfo.setObjectName(_fromUtf8("AccountInfo"))
        AccountInfo.resize(383, 412)
        self.verticalLayout = QtGui.QVBoxLayout(AccountInfo)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.accountIdLabel = QtGui.QLabel(AccountInfo)
        self.accountIdLabel.setObjectName(_fromUtf8("accountIdLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.accountIdLabel)
        self.accountIdLineEdit = QtGui.QLineEdit(AccountInfo)
        self.accountIdLineEdit.setObjectName(_fromUtf8("accountIdLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.accountIdLineEdit)
        self.userNameLabel = QtGui.QLabel(AccountInfo)
        self.userNameLabel.setObjectName(_fromUtf8("userNameLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.userNameLabel)
        self.userNameLineEdit = QtGui.QLineEdit(AccountInfo)
        self.userNameLineEdit.setObjectName(_fromUtf8("userNameLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.userNameLineEdit)
        self.passwordLabel = QtGui.QLabel(AccountInfo)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLineEdit = QtGui.QLineEdit(AccountInfo)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName(_fromUtf8("passwordLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.passwordLineEdit)
        self.oFXFidLabel = QtGui.QLabel(AccountInfo)
        self.oFXFidLabel.setObjectName(_fromUtf8("oFXFidLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.oFXFidLabel)
        self.oFXFidLineEdit = QtGui.QLineEdit(AccountInfo)
        self.oFXFidLineEdit.setObjectName(_fromUtf8("oFXFidLineEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.oFXFidLineEdit)
        self.oFXFiorgLabel = QtGui.QLabel(AccountInfo)
        self.oFXFiorgLabel.setObjectName(_fromUtf8("oFXFiorgLabel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.oFXFiorgLabel)
        self.oFXFiorgLineEdit = QtGui.QLineEdit(AccountInfo)
        self.oFXFiorgLineEdit.setObjectName(_fromUtf8("oFXFiorgLineEdit"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.oFXFiorgLineEdit)
        self.oFXBankIDLabel = QtGui.QLabel(AccountInfo)
        self.oFXBankIDLabel.setObjectName(_fromUtf8("oFXBankIDLabel"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.oFXBankIDLabel)
        self.oFXBankIDLineEdit = QtGui.QLineEdit(AccountInfo)
        self.oFXBankIDLineEdit.setObjectName(_fromUtf8("oFXBankIDLineEdit"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.oFXBankIDLineEdit)
        self.oFXURLLabel = QtGui.QLabel(AccountInfo)
        self.oFXURLLabel.setObjectName(_fromUtf8("oFXURLLabel"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.oFXURLLabel)
        self.oFXURLLineEdit = QtGui.QLineEdit(AccountInfo)
        self.oFXURLLineEdit.setObjectName(_fromUtf8("oFXURLLineEdit"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.oFXURLLineEdit)
        self.oFXAccountTypeLabel = QtGui.QLabel(AccountInfo)
        self.oFXAccountTypeLabel.setObjectName(_fromUtf8("oFXAccountTypeLabel"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.oFXAccountTypeLabel)
        self.oFXAccountTypeComboBox = QtGui.QComboBox(AccountInfo)
        self.oFXAccountTypeComboBox.setObjectName(_fromUtf8("oFXAccountTypeComboBox"))
        self.oFXAccountTypeComboBox.addItem(_fromUtf8(""))
        self.oFXAccountTypeComboBox.addItem(_fromUtf8(""))
        self.oFXAccountTypeComboBox.addItem(_fromUtf8(""))
        self.oFXAccountTypeComboBox.addItem(_fromUtf8(""))
        self.oFXAccountTypeComboBox.addItem(_fromUtf8(""))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.oFXAccountTypeComboBox)
        self.scraperClassLabel = QtGui.QLabel(AccountInfo)
        self.scraperClassLabel.setObjectName(_fromUtf8("scraperClassLabel"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.scraperClassLabel)
        self.scraperClassLineEdit = QtGui.QLineEdit(AccountInfo)
        self.scraperClassLineEdit.setObjectName(_fromUtf8("scraperClassLineEdit"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.scraperClassLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 45, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(AccountInfo)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AccountInfo)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AccountInfo.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AccountInfo.reject)
        QtCore.QMetaObject.connectSlotsByName(AccountInfo)

    def retranslateUi(self, AccountInfo):
        AccountInfo.setWindowTitle(_translate("AccountInfo", "Account Info", None))
        self.accountIdLabel.setText(_translate("AccountInfo", "Account ID", None))
        self.userNameLabel.setText(_translate("AccountInfo", "User Name", None))
        self.passwordLabel.setText(_translate("AccountInfo", "Password", None))
        self.oFXFidLabel.setText(_translate("AccountInfo", "OFX fid", None))
        self.oFXFiorgLabel.setText(_translate("AccountInfo", "OFX fiorg", None))
        self.oFXBankIDLabel.setText(_translate("AccountInfo", "OFX Bank ID", None))
        self.oFXURLLabel.setText(_translate("AccountInfo", "OFX URL", None))
        self.oFXAccountTypeLabel.setText(_translate("AccountInfo", "OFX Account Type", None))
        self.oFXAccountTypeComboBox.setItemText(0, _translate("AccountInfo", "Credit Card", None))
        self.oFXAccountTypeComboBox.setItemText(1, _translate("AccountInfo", "Checking", None))
        self.oFXAccountTypeComboBox.setItemText(2, _translate("AccountInfo", "Savings", None))
        self.oFXAccountTypeComboBox.setItemText(3, _translate("AccountInfo", "Money Market", None))
        self.oFXAccountTypeComboBox.setItemText(4, _translate("AccountInfo", "Credit Line", None))
        self.scraperClassLabel.setText(_translate("AccountInfo", "scraperClass", None))

