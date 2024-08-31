from TransactionTableModel import TransactionTableModel

class SelectedTransactionTableModel(TransactionTableModel):
    def __init__(self):
        TransactionTableModel.__init__(self, [])

        self.db = None
        self.accountSummaryView = None

    def refreshTransactions(self):
        def toPath(t):
            if t.accountTo:
                return t.accountTo.path
            else:
                return self.db.rootExpenseAccount.path + '/<uncategorized>'

        rootExpenseAccount = self.accountSummaryView.rootExpenseAccount
        rootIncomeAccount = self.accountSummaryView.rootIncomeAccount

        rootExpensePath = rootExpenseAccount.path
        rootIncomePath = rootIncomeAccount.path

        def shouldShowTransaction(t):
            tp = toPath(t)
            return tp.startswith(rootExpensePath) or tp.startswith(rootIncomePath)

        self.transactions = [t for t in self.db.transactions if shouldShowTransaction(t)]

        self.transactions = [t for t in self.transactions if t.date >= self.db.datemin and t.date <= self.db.datemax]
        self.transactions = [t for t in self.transactions if (not t.accountTo) or t.accountTo.enabled]

        self.sortTransactions()
        self.layoutChanged.emit()

    def initDb(self, db, accountSummaryView):
        self.db = db
        self.accountSummaryView = accountSummaryView

        self.refreshTransactions()

        self.db.emitter.dataChanged.connect(self.refreshTransactions)
        self.db.emitter.datesChanged.connect(self.refreshTransactions)

        accountSummaryView.rootNodeChanged.connect(self.refreshTransactions)
        accountSummaryView.model().accountEnableChanged.connect(self.refreshTransactions)
