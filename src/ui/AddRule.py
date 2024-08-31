# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddRule.ui'
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

class Ui_AddRule(object):
    def setupUi(self, AddRule):
        AddRule.setObjectName(_fromUtf8("AddRule"))
        AddRule.resize(421, 210)
        self.verticalLayout_2 = QtGui.QVBoxLayout(AddRule)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(AddRule)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.fromEdit = CompleteLineEdit(self.groupBox)
        self.fromEdit.setObjectName(_fromUtf8("fromEdit"))
        self.gridLayout.addWidget(self.fromEdit, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.patternEdit = QtGui.QLineEdit(self.groupBox)
        self.patternEdit.setObjectName(_fromUtf8("patternEdit"))
        self.gridLayout.addWidget(self.patternEdit, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(AddRule)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.toEdit = CompleteLineEdit(self.groupBox_2)
        self.toEdit.setObjectName(_fromUtf8("toEdit"))
        self.horizontalLayout.addWidget(self.toEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setDuplicateCheck = QtGui.QCheckBox(self.groupBox_2)
        self.setDuplicateCheck.setObjectName(_fromUtf8("setDuplicateCheck"))
        self.verticalLayout.addWidget(self.setDuplicateCheck)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.buttonBox = QtGui.QDialogButtonBox(AddRule)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(AddRule)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddRule.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddRule.reject)
        QtCore.QMetaObject.connectSlotsByName(AddRule)
        AddRule.setTabOrder(self.patternEdit, self.toEdit)
        AddRule.setTabOrder(self.toEdit, self.setDuplicateCheck)
        AddRule.setTabOrder(self.setDuplicateCheck, self.fromEdit)
        AddRule.setTabOrder(self.fromEdit, self.buttonBox)

    def retranslateUi(self, AddRule):
        AddRule.setWindowTitle(_translate("AddRule", "Add a rule...", None))
        self.groupBox.setTitle(_translate("AddRule", "If", None))
        self.label_2.setText(_translate("AddRule", "Source account is", None))
        self.label.setText(_translate("AddRule", "Description has", None))
        self.groupBox_2.setTitle(_translate("AddRule", "Then", None))
        self.label_3.setText(_translate("AddRule", "Set destination account", None))
        self.setDuplicateCheck.setText(_translate("AddRule", "Mark as duplicate", None))

from CompleteLineEdit import CompleteLineEdit
