from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from datetime import datetime
from Transaction import Transaction
from Account import Account

class TransactionTableModel(QAbstractTableModel): 
    def __init__(self, transactions, parent=None, *args): 
        QAbstractTableModel.__init__(self, parent, *args) 
        self.transactions = transactions

        self.sortColumn = 0
        self.sortOrder = None
 
    def rowCount(self, parent): 
        return len(self.transactions) 
 
    def columnCount(self, parent): 
        return len(Transaction.Headers)

    @staticmethod
    def getTransactionColumn(t, col, forDisp):
        val = t.getValForIdx(col)
        if isinstance(val, Account):
            val = val.path
        if not forDisp:
            return val

        if isinstance(val, float):
            val = '%.2f' % val
        elif isinstance(val, datetime):
            val = val.strftime('%m/%d/%y')

        return val

    def data(self, index, role): 
        if not index.isValid(): 
            return QVariant() 

        t = self.transactions[index.row()]
        if role == Qt.DisplayRole: 
            col = index.column()
            return self.getTransactionColumn(t, col, True)
        elif role == Qt.FontRole:
            f = QFont()
            if t.isNewTransaction: 
                f.setItalic(True)
            if t.isDuplicate:
                f.setStrikeOut(True)
            return f
        elif role == Qt.ForegroundRole:
            if t.isNewTransaction:
                return QBrush(QColor('blue'))

        return QVariant() 

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(Transaction.Headers[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.sortColumn = Ncol
        self.sortOrder = order

        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.sortTransactions()
        self.emit(SIGNAL("layoutChanged()"))

    def cmpFcn(self, left, right):
        lval = self.getTransactionColumn(left, self.sortColumn, False)
        rval = self.getTransactionColumn(right, self.sortColumn, False)
        result = cmp(lval, rval)
        if self.sortOrder == Qt.DescendingOrder:
            result = -result
        if result:
            return result
        return -cmp(left.date, right.date)

    def sortTransactions(self):
        self.transactions.sort(cmp=self.cmpFcn)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled

        return QAbstractTableModel.flags(self, index)# | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            t = self.transactions[index.row()]
            t.setValForIdx(index.column(), value)

            self.emit(SIGNAL('dataChanged'), index, index)
            return True

        return False
