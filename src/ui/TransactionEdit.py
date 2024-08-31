# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TransactionEdit.ui'
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

class Ui_TransactionEdit(object):
    def setupUi(self, TransactionEdit):
        TransactionEdit.setObjectName(_fromUtf8("TransactionEdit"))
        TransactionEdit.resize(521, 170)
        self.verticalLayout = QtGui.QVBoxLayout(TransactionEdit)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.accountFromLabel = QtGui.QLabel(TransactionEdit)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.accountFromLabel.setFont(font)
        self.accountFromLabel.setObjectName(_fromUtf8("accountFromLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.accountFromLabel)
        self.accountFromLineEdit = CompleteLineEdit(TransactionEdit)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.accountFromLineEdit.setFont(font)
        self.accountFromLineEdit.setObjectName(_fromUtf8("accountFromLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.accountFromLineEdit)
        self.accountToLabel = QtGui.QLabel(TransactionEdit)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.accountToLabel.setFont(font)
        self.accountToLabel.setObjectName(_fromUtf8("accountToLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.accountToLabel)
        self.accountToLineEdit = CompleteLineEdit(TransactionEdit)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.accountToLineEdit.setFont(font)
        self.accountToLineEdit.setObjectName(_fromUtf8("accountToLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.accountToLineEdit)
        self.descriptionLabel = QtGui.QLabel(TransactionEdit)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.descriptionLabel.setFont(font)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.descriptionLabel)
        self.descriptionLineEdit = QtGui.QLineEdit(TransactionEdit)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.descriptionLineEdit.setFont(font)
        self.descriptionLineEdit.setObjectName(_fromUtf8("descriptionLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.descriptionLineEdit)
        self.duplicateLabel = QtGui.QLabel(TransactionEdit)
        self.duplicateLabel.setObjectName(_fromUtf8("duplicateLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.duplicateLabel)
        self.duplicateCheckBox = QtGui.QCheckBox(TransactionEdit)
        self.duplicateCheckBox.setTristate(True)
        self.duplicateCheckBox.setObjectName(_fromUtf8("duplicateCheckBox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.duplicateCheckBox)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtGui.QSpacerItem(20, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(TransactionEdit)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TransactionEdit)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TransactionEdit.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TransactionEdit.reject)
        QtCore.QMetaObject.connectSlotsByName(TransactionEdit)
        TransactionEdit.setTabOrder(self.accountToLineEdit, self.descriptionLineEdit)
        TransactionEdit.setTabOrder(self.descriptionLineEdit, self.duplicateCheckBox)
        TransactionEdit.setTabOrder(self.duplicateCheckBox, self.accountFromLineEdit)
        TransactionEdit.setTabOrder(self.accountFromLineEdit, self.buttonBox)

    def retranslateUi(self, TransactionEdit):
        TransactionEdit.setWindowTitle(_translate("TransactionEdit", "Dialog", None))
        self.accountFromLabel.setText(_translate("TransactionEdit", "Account From", None))
        self.accountToLabel.setText(_translate("TransactionEdit", "Account To", None))
        self.descriptionLabel.setText(_translate("TransactionEdit", "Description", None))
        self.duplicateLabel.setText(_translate("TransactionEdit", "Duplicate?", None))

from CompleteLineEdit import CompleteLineEdit
