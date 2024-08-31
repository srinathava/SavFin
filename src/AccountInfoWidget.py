from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re

PAT_NONNUM_CHARS = re.compile('[^0-9.-]')

import locale

from ui.AccountInfoWidgetBase import Ui_AccountInfoWidgetBase
from AccountTreeView import importTransactions
from datetime import datetime

class AccountBalancesTableModel(QAbstractTableModel):
    Headers = ['Date', 'Amount']

    def __init__(self, account):
        super(AccountBalancesTableModel, self).__init__()
        self.account = account

    def rowCount(self, parent):
        return len(self.account.balanceSnapshots)

    def columnCount(self, parent):
        return 2

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.Headers[col])
        return QVariant()

    def qtRowIndexToSnapshotRowIndex(self, qtRow):
        return len(self.account.balanceSnapshots) - qtRow - 1

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            p = self.account.balanceSnapshots[self.qtRowIndexToSnapshotRowIndex(index.row())]
            date = p[0].strftime('%m/%d/%Y')
            amount = locale.currency(p[1], '$', True)

            return [date, amount][index.column()]

        return QVariant()

class AccountInfoWidget(QWidget, Ui_AccountInfoWidgetBase):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.account = None
        self.db = None

        self.setupUi(self)

        self.textEditMap = {}

        self.mapLineEdit('accountIdLineEdit', 'accountId')
        self.mapLineEdit('userNameLineEdit', 'userName')
        self.mapLineEdit('passwordLineEdit', 'password')
        self.mapLineEdit('oFXFidLineEdit', 'ofx_fid')
        self.mapLineEdit('oFXFiorgLineEdit', 'ofx_fiorg')
        self.mapLineEdit('oFXURLLineEdit', 'ofx_url')
        self.mapLineEdit('oFXBankIDLineEdit', 'ofx_bankid')
        self.mapLineEdit('scraperClassLineEdit', 'scraperClass')

        self.saveButton.clicked.connect(self.setAccountInfo)
        self.discardButton.clicked.connect(self.getAccountInfo)
        self.importButton.clicked.connect(self.importAccountTransactions)
        self.balanceAddButton.clicked.connect(self.addBalance)

        self.balanceDateEdit.setDate(datetime.today())
        self.balanceTableModel = None

    def initDb(self, db):
        self.db = db
        self.db.emitter.dataChanged.connect(self.refresh)

    def mapLineEdit(self, lineEditName, propName):
        self.textEditMap[lineEditName] = propName

    def setAccountInfo(self):
        for (lineEditName, propName) in self.textEditMap.items():
            value = str(getattr(self, lineEditName).text())
            setattr(self.account, propName, value)

        self.account.ofx_acctTypeIdx = self.oFXAccountTypeComboBox.currentIndex()

    def getAccountInfo(self):
        self.balanceTableModel = AccountBalancesTableModel(self.account)
        self.balanceTableView.setModel(self.balanceTableModel)

        for (lineEditName, propName) in self.textEditMap.items():
            getattr(self, lineEditName).setText(getattr(self.account, propName))

        self.oFXAccountTypeComboBox.setCurrentIndex(self.account.ofx_acctTypeIdx)

    def selectAccount(self, index):
        self.account = index.internalPointer()
        self.getAccountInfo()

    def keyPressEvent(self, event):
        if not self.account:
            return

        indices = self.balanceTableView.selectionModel().selectedIndexes()
        rows = [self.balanceTableModel.qtRowIndexToSnapshotRowIndex(index.row()) for index in indices]
        if not rows:
            return

        rows = list(set(rows))
        rows.sort(reverse=True)

        for r in rows:
            del self.account.balanceSnapshots[r]

        self.db.emitDataChanged()

    def importAccountTransactions(self):
        importTransactions(self.db, self.account)

    def addBalance(self):
        if not self.account:
            return

        date = QDateTime(self.balanceDateEdit.date()).toPyDateTime()
        txt = self.balanceAmountLineEdit.text()
        txt = PAT_NONNUM_CHARS.sub('', txt)
        balance = float(txt)

        self.db.addBalanceSnapshot(self.account, date, balance)

    def refresh(self):
        self.balanceTableModel.layoutChanged.emit()

