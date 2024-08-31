from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import csv
from Transaction import Transaction
from TransactionTableModel import TransactionTableModel
from TransactionTableView import TransactionTableView
from datetime import datetime

DATE_FORMATS = ['%m/%d/%y', '%m/%d/%Y']
def parseDateStr(datestr):
    for fmt in DATE_FORMATS:
        try:
            d = datetime.strptime(datestr, fmt)
            return d
        except ValueError:
            pass

    return None

class CsvTableModel(QAbstractTableModel):
    def __init__(self, fileName):
        QAbstractTableModel.__init__(self)
        reader = csv.reader(open(fileName))
        self.rows = []
        for row in reader:
            self.rows.append(row)

        self.headers = ['None']*len(self.rows[0])

    def rowCount(self, parent):
        return len(self.rows)

    def columnCount(self, parent):
        return len(self.rows[0])

    def data(self, index, role):
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 

        return QVariant(self.rows[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headers[col])
        return QVariant()

    def setSectionTitle(self, index, title):
        self.headers[index] = title
        self.emit(SIGNAL('headerDataChanged()'))

class CsvTableView(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        header = self.horizontalHeader()
        self.connect(header, SIGNAL('sectionClicked(int)'), self.headerClicked)

        self.setSelectionMode(QAbstractItemView.NoSelection)

    def initialize(self, fileName):
        model = CsvTableModel(fileName)
        self.setModel(model)

    def headerClicked(self, index):
        menu = QMenu()
        menu.addAction('Date', lambda: self.setColumnTitle(index, 'Date'))
        menu.addAction('Description', lambda: self.setColumnTitle(index, 'Description'))
        menu.addAction('Amount', lambda: self.setColumnTitle(index, 'Amount'))
        menu.exec_(QCursor.pos())

    def setColumnTitle(self, index, title):
        self.model().setSectionTitle(index, title)

class FileLineEdit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)

    def focusInEvent(self, event):
        QLineEdit.focusInEvent(self, event)
        files = QFileDialog.getOpenFileNames(self,
                'Choose a CSV file', '',
                'CSV files (*.csv)')
        if files:
            self.setText(files[0])

class CsvImporter(QWizard):
    def __init__(self, db, fileName, account, parent=None):
        self.db = db
        self.csvFileName = fileName
        self.account = account
        self.accounts = ['', 'Bank of America (savings)', 'Bank of America (checking)']
        self.transactions = []

        self.reverseAmounts = False

        QWizard.__init__(self, parent)
        self.addChooseFilePage()
        self.addChooseColumnsPage()
        self.addChooseCategoriesPage()
        self.setWindowTitle('Import a CSV file')

        if self.csvFileName and self.account:
            self.setupNextPage(1)
            self.setStartId(1)

    def addChooseFilePage(self):
        page = QWizardPage()
        page.setTitle('Select account and CSV file')
        layout = QGridLayout()

        accountLabel = QLabel('Account:')
        accountChooser = QComboBox()
        [accountChooser.addItem(it) for it in self.accounts]

        self.connect(accountChooser, SIGNAL('activated(int)'), self.chooseAccount)

        fileLabel = QLabel('File:')
        self.fileNameEdit = QLineEdit()
        self.fileBrowserButton = QPushButton('...')

        self.connect(self.fileBrowserButton, SIGNAL('clicked()'), self.onFileBrowserClicked)

        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(self.fileNameEdit, 1)
        hboxLayout.addWidget(self.fileBrowserButton)

        layout.addWidget(accountLabel, 0, 0)
        layout.addWidget(accountChooser, 0, 1)
        layout.addWidget(fileLabel, 1, 0)
        layout.addLayout(hboxLayout, 1, 1)

        page.setLayout(layout)
        self.addPage(page)

        self.connect(self, SIGNAL('currentIdChanged(int)'), self.setupNextPage)

    def chooseAccount(self, idx):
        self.account = self.accounts[idx]

    def setupNextPage(self, id):
        if id == 1:
            self.csvTableView.initialize(self.csvFileName)
        elif id == 2:
            self.setupChooseCategoryPage()

    def onFileBrowserClicked(self):
        files = QFileDialog.getOpenFileNames(self,
                'Choose a CSV file', '',
                'CSV files (*.csv)')
        if files:
            self.csvFileName = files[0]
            self.fileNameEdit.setText(self.csvFileName)

    def addChooseColumnsPage(self):
        page = QWizardPage()
        page.setTitle("Step 2: Select columns")

        label = QLabel("Click on the column headers and choose column meanings")
        label.setWordWrap(True)

        reverseAmountsCheck = QCheckBox('Reverse amounts')
        reverseAmountsCheck.stateChanged.connect(self.onReverseAmountsChecked)

        self.csvTableView = CsvTableView()
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(reverseAmountsCheck)
        layout.addWidget(self.csvTableView)

        page.setLayout(layout)
        self.addPage(page)

    def onReverseAmountsChecked(self, state):
        self.reverseAmounts = state

    def addChooseCategoriesPage(self):
        page = QWizardPage()
        page.setTitle("Step 3: Choose categories")

        label = QLabel("Choose categories for the transactions")
        label.setWordWrap(True)

        self.transTableView = TransactionTableView()
        self.transTableView.initDb(self.db)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.transTableView)

        page.setLayout(layout)

        self.addPage(page)
        self.chooseCatPage = page

    def getTransactions(self):
        csvModel = self.csvTableView.model()
        rows = csvModel.rows
        headers = csvModel.headers

        idx_amount = headers.index('Amount')
        idx_desc = headers.index('Description')
        idx_date = headers.index('Date')

        self.transactions = []
        for r in rows:
            date = parseDateStr(r[idx_date])
            if not date:
                continue

            t = Transaction()
            self.transactions.append(t)

            amt_str = r[idx_amount]
            amt_str = amt_str.replace('$', '')
            amt_str = amt_str.replace(',', '')

            amount = float(amt_str)
            if self.reverseAmounts:
                amount = -amount

            t.date = date
            t.desc = r[idx_desc]
            t.amount = amount
            t.accountFrom = self.account

    def setupChooseCategoryPage(self):
        self.getTransactions()
        self.transModel = TransactionTableModel(self.transactions)
        print 'setting up stuff...'
        self.transTableView.setModel(self.transModel)

if __name__ == "__main__":
    from testdata import getTestData
    app = QApplication(sys.argv)

    db = getTestData()

    window = CsvImporter(db, None, None)
    window.show()
    sys.exit(app.exec_())
