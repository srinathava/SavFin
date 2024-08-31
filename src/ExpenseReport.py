from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from AccountSummary import getAccountSummary
from TreeModel import TreeModel
from PieChart import PieChart
from datetime import timedelta, date
from HistogramView import Histogram
import locale
from config import *
from ui.ExpenseReportWidget import Ui_ExpenseReport

def getHistogramBins(db, rootAccount, datemin, datemax, stepFcn):
    labels = []
    amounts = []
    intervals = []

    t1 = datemin
    t2 = stepFcn(t1) - timedelta(1)
    while 1:
        rootNode = getAccountSummary(db, datemin=t1, datemax=t2, rootAccount=rootAccount)
        amount = rootNode.total

        labels.append(t1.strftime('%b %y'))
        amounts.append(amount)
        intervals.append([t1, t2])

        t1 = t2 + timedelta(1)
        t2 = stepFcn(t1) - timedelta(1)
        if t1 >= datemax:
            break

    return (labels, amounts, intervals)

class ExpenseReport(QWidget, Ui_ExpenseReport):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.summaryView.rootNodeChanged.connect(self.onSummaryRootNodeChanged)
        self.histogram.doubleClicked.connect(self.setInterval)
        self.doneLayout = False
        self.intervals = []

        self.rootAccount = None
        self.rootIncomeAccount = None

    def setRootNodes(self):
        self.rootNode = getAccountSummary(self.db, rootAccount=self.rootAccount)
        self.rootIncomeNode = getAccountSummary(self.db, 
                rootAccount=self.rootIncomeAccount, 
                signTo=-1,
                gatherUncategorized=False)

    def initDb(self, db):
        self.db = db
        self.db.emitter.dataChanged.connect(self.refresh)
        self.db.emitter.datesChanged.connect(self.refresh)

        self.rootAccount = self.db.rootExpenseAccount
        self.rootIncomeAccount = self.db.rootIncomeAccount
        self.refresh()

        self.summaryView.model().accountEnableChanged.connect(self.refresh)

    def onSummaryRootNodeChanged(self):
        self.rootAccount = self.summaryView.rootExpenseAccount
        self.rootIncomeAccount = self.summaryView.rootIncomeAccount
        self.refresh()

    def refresh(self):
        self.setRootNodes()
        self.setData()
        self.summaryView.setRootNodes(self.rootNode, self.rootIncomeNode)
        self.expensesPie.draw()
        self.histogram.draw()

    def setInterval(self, idx):
        self.db.setInterval(self.intervals[idx])

    def setData(self):
        nodes = self.rootNode.children
        nodes.sort(key = lambda node: -node.total)
        self.expensesPie.labels = [node.acct.name for node in nodes if node.enabled]
        self.expensesPie.data = [node.total for node in nodes if node.enabled]

        (labels, amounts, self.intervals) = getHistogramBins(self.db, self.rootNode.acct, 
                self.db.datemin, self.db.datemax, self.db.minorStepFcn)
        self.histogram.xTickLabels = labels
        self.histogram.posData = amounts

if __name__ == '__main__':
    from testdata import getTestData
    db = getTestData()

    app = QApplication(sys.argv)
    view = ExpenseReport()
    view.initDb(db)
    view.show()

    app.exec_()
