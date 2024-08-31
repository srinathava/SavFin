from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from Transaction import Transaction
from TransactionTableModel import TransactionTableModel
from CompleteLineEdit import CompleteLineEdit
from ui.TransactionEdit import Ui_TransactionEdit
from AddRuleDialog import AddRuleDialog
from datetime import datetime, timedelta
import collections
import operator
import csv
import StringIO

class ChooseCategoryDialog(QDialog, Ui_TransactionEdit):
    def __init__(self, db, transactions):
        QDialog.__init__(self)
        self.setupUi(self)

        self.db = db
        self.transactions = transactions

        self.setupInitValues()

    def setupInitValues(self):
        # setup completion lists
        accountPaths = [a.path for a in self.db.accounts if len(a.children) == 0]
        accountPaths.append('NONE')
        self.accountFromLineEdit.words = accountPaths
        self.accountToLineEdit.words = accountPaths

        # value of checkbox
        dupVals = [t.isDuplicate for t in self.transactions]
        hasDups = any(dupVals)
        allDups = all(dupVals)
        if allDups:
            self.duplicateCheckBox.setCheckState(Qt.Checked)
        elif not hasDups:
            self.duplicateCheckBox.setCheckState(Qt.Unchecked)
        else:
            self.duplicateCheckBox.setCheckState(Qt.PartiallyChecked)

        if len(self.transactions) == 1:
            t = self.transactions[0]

            self.duplicateCheckBox.setTristate(False)

            if t.accountFrom:
                self.accountFromLineEdit.setText(t.accountFrom.path)

            if t.accountTo:
                self.accountToLineEdit.setText(t.accountTo.path)

            self.descriptionLineEdit.setText(t.desc)

    def accept(self):
        def getAccount(comboBox):
            txt = str(comboBox.text())
            if txt == 'NONE':
                account = None
            elif txt:
                account = self.db.getAccountFromName(txt)
            else:
                account = 'SAME'
            return account

        accountFrom = getAccount(self.accountFromLineEdit)
        accountTo = getAccount(self.accountToLineEdit)
        checkState = self.duplicateCheckBox.checkState()
        description = str(self.descriptionLineEdit.text())

        for transaction in self.transactions:
            if accountFrom != 'SAME':
                transaction.accountFrom = accountFrom
            if accountTo != 'SAME':
                transaction.accountTo = accountTo

            if checkState != Qt.PartiallyChecked:
                transaction.isDuplicate = True if checkState == Qt.Checked else False

            if description or len(self.transactions) == 1:
                if len(self.transactions) > 1:
                    transaction.desc += ' ' + description[1:].strip()
                else:
                    transaction.desc = description

        self.db.emitDataChanged()
        QDialog.accept(self)

class TransactionTableView(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.setSortingEnabled(True)
        # self.horizontalHeader().sectionClicked.connect(self.addSelectionColumn)
        self.verticalHeader().setDefaultSectionSize(16)
        self.setSelectionBehavior(self.SelectRows)
        self.rule = None
        self.detectDuplicatesFlag = False

    def setColumnWidths(self):
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(3, 200)

    def initDb(self, db):
        self.db = db
        self.categories = [acct.name for acct in db.accounts]

        self.setEditTriggers(self.AnyKeyPressed | self.EditKeyPressed |
                self.DoubleClicked)
        self.verticalHeader().setVisible(True)
        self.verticalHeader().setMinimumSize(QSize(10, 10))
        self.horizontalHeader().setStretchLastSection(True)

        self.setModel(TransactionTableModel(self.db.transactions))
        self.db.emitter.dataChanged.connect(self.onDbLayoutChanged)
        self.onDbLayoutChanged()

        self.sortByColumn(0, Qt.DescendingOrder)

        self.setColumnWidths()

    def onDbLayoutChanged(self):
        if self.rule:
            transactions = [t for t in self.db.transactions if self.rule.match(t)]
        else:
            transactions = self.db.transactions

        if self.detectDuplicatesFlag:
            transactions = self.getDuplicates(transactions)

        self.model().transactions = transactions
        self.model().sortTransactions()
        self.model().layoutChanged.emit()

    def getDuplicates(self, transactions):
        def closeInTime(d1, d2):
            return d1 - d2 <= timedelta(2)

        def onlyOneHasOfxId(t1, t2):
            return bool(t1.ofxId) != bool(t2.ofxId)

        transIdToTransMap = collections.defaultdict(list)
        for t in transactions:
            key = (t.accountFrom, t.amount)
            transIdToTransMap[key].append(t)

        duplicates = []

        for (tid, tid_transactions) in transIdToTransMap.items():
            if len(tid_transactions) == 1:
                continue

            tid_transactions.sort(key=operator.attrgetter('date'))

            last_date = datetime.min
            last_trans = None
            for t in tid_transactions:
                if closeInTime(t.date, last_date) and onlyOneHasOfxId(t, last_trans):
                    duplicates.append(last_trans)
                    duplicates.append(t)

                last_date = t.date
                last_trans = t

        return duplicates

    def detectDuplicates(self, detectDuplicatesFlag):
        self.detectDuplicatesFlag = detectDuplicatesFlag
        self.onDbLayoutChanged()

    def getSelectedTransactions(self):
        transactions = self.model().transactions
        rows = [index.row() for index in self.selectionModel().selectedIndexes()]
        rows = list(set(rows))
        return [transactions[row] for row in rows]

    def keyPressEvent(self, event):
        transactions = self.getSelectedTransactions()
        if not transactions:
            QTableView.keyPressEvent(self, event)
            return

        if event.key() == Qt.Key_E:
            chooseCat = ChooseCategoryDialog(self.db, transactions)
            chooseCat.exec_()

        elif event.key() == Qt.Key_Delete:
            if event.modifiers() & Qt.ShiftModifier:
                self.db.deleteTransactions(transactions)
            else:
                for transaction in transactions:
                    transaction.isDuplicate = True
                self.db.emitDataChanged()

        elif event.matches(QKeySequence.Copy):
            output = StringIO.StringIO()
            writer = csv.writer(output, dialect=csv.excel_tab)
            for t in transactions:
                row = [t.date.strftime('%m/%d/%y'), t.desc,
                        t.fromPath, t.toPath, t.amount, int(t.isDuplicate)]
                writer.writerow(row)

            txt = output.getvalue()
            clip = QApplication.clipboard()
            clip.setText(txt)

        elif event.key() == Qt.Key_R:
            addRuleDialog = AddRuleDialog(self.db, transactions[0])
            addRuleDialog.exec_()

        else:
            QTableView.keyPressEvent(self, event)

    def addSelectionColumn(self, index):
        print 'getting here'

    def setFilterRule(self, rule):
        self.rule = rule
        self.onDbLayoutChanged()

if __name__ == "__main__":
    import sys
    from testdata import getTestData

    db = getTestData()

    app = QApplication(sys.argv)

    window = TransactionTableView()
    window.initDb(db)
    model = TransactionTableModel(db.transactions)
    window.setModel(model)
    window.setMinimumSize(QSize(800,400))
    window.show()
    sys.exit(app.exec_())
