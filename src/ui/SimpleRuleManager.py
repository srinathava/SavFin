# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SimpleRuleManager.ui'
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

class Ui_SimpleRuleManager(object):
    def setupUi(self, SimpleRuleManager):
        SimpleRuleManager.setObjectName(_fromUtf8("SimpleRuleManager"))
        SimpleRuleManager.resize(702, 628)
        self.horizontalLayout = QtGui.QHBoxLayout(SimpleRuleManager)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.rulesTableView = SimpleRuleTableView(SimpleRuleManager)
        self.rulesTableView.setObjectName(_fromUtf8("rulesTableView"))
        self.horizontalLayout.addWidget(self.rulesTableView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addButton = QtGui.QPushButton(SimpleRuleManager)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout.addWidget(self.addButton)
        self.deleteButton = QtGui.QPushButton(SimpleRuleManager)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.verticalLayout.addWidget(self.deleteButton)
        self.moveUpButton = QtGui.QPushButton(SimpleRuleManager)
        self.moveUpButton.setObjectName(_fromUtf8("moveUpButton"))
        self.verticalLayout.addWidget(self.moveUpButton)
        self.moveDownButton = QtGui.QPushButton(SimpleRuleManager)
        self.moveDownButton.setObjectName(_fromUtf8("moveDownButton"))
        self.verticalLayout.addWidget(self.moveDownButton)
        self.runAllRulesButton = QtGui.QPushButton(SimpleRuleManager)
        self.runAllRulesButton.setObjectName(_fromUtf8("runAllRulesButton"))
        self.verticalLayout.addWidget(self.runAllRulesButton)
        self.exportButton = QtGui.QPushButton(SimpleRuleManager)
        self.exportButton.setObjectName(_fromUtf8("exportButton"))
        self.verticalLayout.addWidget(self.exportButton)
        self.importButton = QtGui.QPushButton(SimpleRuleManager)
        self.importButton.setObjectName(_fromUtf8("importButton"))
        self.verticalLayout.addWidget(self.importButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(SimpleRuleManager)
        QtCore.QMetaObject.connectSlotsByName(SimpleRuleManager)

    def retranslateUi(self, SimpleRuleManager):
        SimpleRuleManager.setWindowTitle(_translate("SimpleRuleManager", "Form", None))
        self.addButton.setText(_translate("SimpleRuleManager", "Add", None))
        self.deleteButton.setText(_translate("SimpleRuleManager", "Delete", None))
        self.moveUpButton.setText(_translate("SimpleRuleManager", "Up", None))
        self.moveDownButton.setText(_translate("SimpleRuleManager", "Down", None))
        self.runAllRulesButton.setText(_translate("SimpleRuleManager", "Run All Rules", None))
        self.exportButton.setText(_translate("SimpleRuleManager", "Export...", None))
        self.importButton.setText(_translate("SimpleRuleManager", "Import...", None))

from SimpleRuleTableView import SimpleRuleTableView
