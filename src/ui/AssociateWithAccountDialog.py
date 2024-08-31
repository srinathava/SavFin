# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AssociateWithAccountDialog.ui'
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

class Ui_AssociateWithAccountDialog(object):
    def setupUi(self, AssociateWithAccountDialog):
        AssociateWithAccountDialog.setObjectName(_fromUtf8("AssociateWithAccountDialog"))
        AssociateWithAccountDialog.resize(398, 166)
        self.verticalLayout = QtGui.QVBoxLayout(AssociateWithAccountDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(AssociateWithAccountDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(375, 89))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.groupBox)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.accountLineEdit = CompleteLineEdit(AssociateWithAccountDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.accountLineEdit.setFont(font)
        self.accountLineEdit.setObjectName(_fromUtf8("accountLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.accountLineEdit)
        self.accountLabel = QtGui.QLabel(AssociateWithAccountDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.accountLabel.setFont(font)
        self.accountLabel.setObjectName(_fromUtf8("accountLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.accountLabel)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(AssociateWithAccountDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.raise_()
        self.groupBox.raise_()
        self.accountLineEdit.raise_()
        self.accountLabel.raise_()

        self.retranslateUi(AssociateWithAccountDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AssociateWithAccountDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AssociateWithAccountDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AssociateWithAccountDialog)

    def retranslateUi(self, AssociateWithAccountDialog):
        AssociateWithAccountDialog.setWindowTitle(_translate("AssociateWithAccountDialog", "Dialog", None))
        self.groupBox.setTitle(_translate("AssociateWithAccountDialog", "Information", None))
        self.label.setText(_translate("AssociateWithAccountDialog", "The account ID \"...\" in this download is not yet associated with any of your accounts. Please choose an account below and press \"OK\"", None))
        self.accountLabel.setText(_translate("AssociateWithAccountDialog", "Account", None))

from CompleteLineEdit import CompleteLineEdit
