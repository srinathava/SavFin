from PyQt4.QtCore import *
from PyQt4.QtGui import *
from AccountTreeModel import *
from ui.AccountInfo import Ui_AccountInfo
import re
import time
from OfxUtils import importOfxTransactionsFromWeb

def importTransactions(db, account):
    if account.scraperClass:
        mod = __import__(account.scraperClass)
        klass = mod.__dict__[account.scraperClass]
        obj = klass(db, account)
        obj.exec_()

    elif account.hasOfxInfo():
        importOfxTransactionsFromWeb(db, account)

    else:
        msgBox = QMessageBox()
        msgBox.setText('No Ofx information or Scraper for this account')
        msgBox.setInformativeText('You need to first edit this account and add all details (except password) to be able to import automatically')
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

class AccountInfoEdit(QDialog, Ui_AccountInfo):
    def __init__(self, account):
        super(AccountInfoEdit, self).__init__()
        self.setupUi(self)
        self.account = account
        self.getAccountInfo()
        self.accepted.connect(self.setAccountInfo)

    def getAccountInfo(self):
        self.accountIdLineEdit.setText(self.account.accountId)
        self.userNameLineEdit.setText(self.account.userName)
        self.passwordLineEdit.setText(self.account.password)
        self.oFXFidLineEdit.setText(self.account.ofx_fid)
        self.oFXFiorgLineEdit.setText(self.account.ofx_fiorg)
        self.oFXURLLineEdit.setText(self.account.ofx_url)
        self.oFXBankIDLineEdit.setText(self.account.ofx_bankid)
        self.oFXAccountTypeComboBox.setCurrentIndex(self.account.ofx_acctTypeIdx)
        self.scraperClassLineEdit.setText(self.account.scraperClass)

    def setAccountInfo(self):
        self.account.accountId       = str(self.accountIdLineEdit.text())
        self.account.userName        = str(self.userNameLineEdit.text())
        self.account.password        = str(self.passwordLineEdit.text())
        self.account.ofx_fid         = str(self.oFXFidLineEdit.text())
        self.account.ofx_fiorg       = str(self.oFXFiorgLineEdit.text())
        self.account.ofx_url         = str(self.oFXURLLineEdit.text())
        self.account.ofx_bankid      = str(self.oFXBankIDLineEdit.text())
        self.account.ofx_acctTypeIdx = self.oFXAccountTypeComboBox.currentIndex()
        self.account.scraperClass    = str(self.scraperClassLineEdit.text())

class AccountTreeView(QTreeView):
    def __init__(self, parent=None):
        QTreeView.__init__(self, parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def initDb(self, db):
        self.db = db
        m = AccountTreeModel(db)
        self.setModel(m)
        self.expandToDepth(0)
        m.dataChanged.connect(db.emitter.dataChanged)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            idx = self.selectionModel().selectedIndexes()[0]
            self.model().remove(idx)

        elif event.key() == Qt.Key_N and event.modifiers() == Qt.ControlModifier:
            idx = self.selectionModel().selectedIndexes()[0]
            self.model().appendRow(idx)
            nRows = self.model().rowCount(idx)
            newAccountIdx = self.model().index(nRows-1, 0, idx)
            self.expand(idx)
            self.setCurrentIndex(newAccountIdx)
            self.edit(newAccountIdx)

        elif event.key() == Qt.Key_E:
            idx = self.selectionModel().selectedIndexes()[0]
            account = idx.internalPointer()
            accountEdit = AccountInfoEdit(account)
            accountEdit.exec_()

        elif event.key() == Qt.Key_I:
            idx = self.selectionModel().selectedIndexes()[0]
            account = idx.internalPointer()
            importTransactions(self.db, account)

        else:
            QTreeView.keyPressEvent(self, event)

if __name__ == "__main__":
    from SavfinData import SavfinData
    import sys

    app = QApplication(sys.argv)

    db = SavfinData()
    accountTreeView = AccountTreeView()
    accountTreeView.initDb(db)
    accountTreeView.show()

    app.exec_()

