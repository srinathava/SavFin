from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ui.TransactionFilterView import Ui_TransactionFilterView
from RuleParser import compilePattern
import pyparsing

LINKMAP = {}
LINKMAP[u'amountLink'] = 'amount > 400'
LINKMAP[u'dateLink'] = 'date > 3/25/11'
LINKMAP[u'descLink'] = 'desc contains "blah"'
LINKMAP[u'fromPathLink'] = 'from contains "bank"'
LINKMAP[u'toPathLink'] = 'to contains "bank"'
LINKMAP[u'orLink'] = '(  ) or (  )'
LINKMAP[u'andLink'] = '(  ) and (  )'

class FilteredTransactionView(QWidget, Ui_TransactionFilterView):
    def __init__(self):
        super(FilteredTransactionView, self).__init__()
        self.setupUi(self)

        self.rulesLabel.linkActivated.connect(self.onLinkClicked)
        self.applyButton.clicked.connect(self.applyFilter)
        self.resetButton.clicked.connect(self.resetFilter)
        self.ruleTextEdit.returnPressed.connect(self.applyFilter)
        self.db = None

    def getSelectedTransactions(self):
        return self.transactionTableView.getSelectedTransactions()

    def onLinkClicked(self, url):
        if (str(url) == 'orLink' or str(url) == 'andLink'):
            op = str(url).replace('Link', '')
            origText = str(self.ruleTextEdit.text())
            newTxt = '( %s ) %s (  )' % (origText, op)
            self.ruleTextEdit.setText(newTxt)
            pos = len(newTxt) - 2
            self.ruleTextEdit.setCursorPosition(pos)
        else:
            txt = LINKMAP[str(url)]
            self.ruleTextEdit.insert(txt)

    def setPallete(self, err):
        p = self.ruleTextEdit.palette();
        if err:
            col = QColor('#faa')
        else:
            col = QColor('#fff')
        p.setColor(QPalette.Active, QPalette.Base, col);
        p.setColor(QPalette.Inactive, QPalette.Base, col);
        self.ruleTextEdit.setPalette(p);

    def resetFilter(self):
        self.ruleTextEdit.setText('')
        self.transactionTableView.setFilterRule(None)
        self.setPallete(False)

    def applyFilter(self):
        err = False

        ruleText = str(self.ruleTextEdit.text())
        rule = None
        if ruleText.strip():
            try:
                rule = compilePattern(ruleText)
            except pyparsing.ParseException as e:
                err = True

        self.transactionTableView.setFilterRule(rule)
        self.setPallete(err)

    def detectDuplicates(self, detectDuplicatesFlag):
        self.transactionTableView.detectDuplicates(detectDuplicatesFlag)

    def initDb(self, db):
        self.db = db
        self.transactionTableView.initDb(self.db)

