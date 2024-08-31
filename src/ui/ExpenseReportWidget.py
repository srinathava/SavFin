# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExpenseReportWidget.ui'
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

class Ui_ExpenseReport(object):
    def setupUi(self, ExpenseReport):
        ExpenseReport.setObjectName(_fromUtf8("ExpenseReport"))
        ExpenseReport.resize(825, 739)
        ExpenseReport.setStyleSheet(_fromUtf8("background-color: white;"))
        self.horizontalLayout = QtGui.QHBoxLayout(ExpenseReport)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.summaryView = AccountSummaryView(ExpenseReport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.summaryView.sizePolicy().hasHeightForWidth())
        self.summaryView.setSizePolicy(sizePolicy)
        self.summaryView.setMinimumSize(QtCore.QSize(300, 100))
        self.summaryView.setMaximumSize(QtCore.QSize(300, 16777215))
        self.summaryView.setObjectName(_fromUtf8("summaryView"))
        self.horizontalLayout.addWidget(self.summaryView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.expensesPie = PieChart(ExpenseReport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.expensesPie.sizePolicy().hasHeightForWidth())
        self.expensesPie.setSizePolicy(sizePolicy)
        self.expensesPie.setStyleSheet(_fromUtf8("border: 0px;"))
        self.expensesPie.setObjectName(_fromUtf8("expensesPie"))
        self.verticalLayout.addWidget(self.expensesPie)
        self.histogram = Histogram(ExpenseReport)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histogram.sizePolicy().hasHeightForWidth())
        self.histogram.setSizePolicy(sizePolicy)
        self.histogram.setStyleSheet(_fromUtf8("border: 0px;"))
        self.histogram.setObjectName(_fromUtf8("histogram"))
        self.verticalLayout.addWidget(self.histogram)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(ExpenseReport)
        QtCore.QMetaObject.connectSlotsByName(ExpenseReport)

    def retranslateUi(self, ExpenseReport):
        ExpenseReport.setWindowTitle(_translate("ExpenseReport", "Form", None))

from AccountSummaryTableModel import AccountSummaryView
from HistogramView import Histogram
from PieChart import PieChart
