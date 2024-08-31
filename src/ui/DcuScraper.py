# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DcuScraper.ui'
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

class Ui_DcuScraper(object):
    def setupUi(self, DcuScraper):
        DcuScraper.setObjectName(_fromUtf8("DcuScraper"))
        DcuScraper.resize(396, 122)
        self.verticalLayout = QtGui.QVBoxLayout(DcuScraper)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(DcuScraper)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.userNumberEdit = QtGui.QLineEdit(DcuScraper)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.userNumberEdit.setFont(font)
        self.userNumberEdit.setObjectName(_fromUtf8("userNumberEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.userNumberEdit)
        self.label_2 = QtGui.QLabel(DcuScraper)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.passwordEdit = QtGui.QLineEdit(DcuScraper)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passwordEdit.setFont(font)
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordEdit.setObjectName(_fromUtf8("passwordEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.passwordEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.progressBar = QtGui.QProgressBar(DcuScraper)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.statusLabel = QtGui.QLabel(DcuScraper)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.statusLabel.setFont(font)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.verticalLayout.addWidget(self.statusLabel)

        self.retranslateUi(DcuScraper)
        QtCore.QMetaObject.connectSlotsByName(DcuScraper)

    def retranslateUi(self, DcuScraper):
        DcuScraper.setWindowTitle(_translate("DcuScraper", "DCU Scraper", None))
        self.label.setText(_translate("DcuScraper", "User Number", None))
        self.label_2.setText(_translate("DcuScraper", "Password", None))
        self.statusLabel.setText(_translate("DcuScraper", "Status", None))

