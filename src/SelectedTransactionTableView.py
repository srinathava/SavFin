from PyQt4.QtCore import Qt
from SelectedTransactionTableModel import SelectedTransactionTableModel
from TransactionTableView import TransactionTableView

class SelectedTransactionTableView(TransactionTableView):
    def initDb(self, db, expenseReportTab):
        self.db = db
        self.setModel(SelectedTransactionTableModel())
        self.model().initDb(db, expenseReportTab.summaryView)
        self.setColumnWidths()
        self.sortByColumn(0, Qt.DescendingOrder)

