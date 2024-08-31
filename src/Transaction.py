class Transaction(object):
    Headers = ('Date', 'Description', 'From', 'To', 'Amount', 'ID')
    Fields = ('date', 'desc', 'accountFrom', 'accountTo', 'amount', 'ofxId')
    IdxFrom = 2
    IdxTo = 3
    IdxAmount = 4

    def __init__(self):
        self.date = None
        self.amount = None
        self.desc = None
        self.accountFrom = ''
        self.accountTo = ''
        self.ofxId = ''
        self.isNewTransaction = True
        self.isDuplicate = False

    @property
    def fromPath(self):
        return self.accountFrom.path if self.accountFrom else ''

    @property
    def toPath(self):
        return self.accountTo.path if self.accountTo else ''

    RENAME_RULES = {'amt': 'amount'}
    def __setstate__(self, state):
        self.__init__()
        for it in state:
            lhs = it
            rhs = it
            if it in self.RENAME_RULES:
                rhs = it
                lhs = self.RENAME_RULES[it]

            self.__dict__[lhs] = state[rhs]
        self.isNewTransaction = False

    def getValForIdx(self, idx):
        val = self.__dict__[self.Fields[idx]]
        return val

    def setValForIdx(self, idx, val):
        self.__dict__[self.Fields[idx]] = val

    def __str__(self):
        return '%s|\t%15s|\t%15s|\t%15s|\t%.2f$' % (self.date.strftime('%m/%d/%y'), self.desc[:15], self.accountFrom, self.accountTo, self.amount)

    def __repr__(self):
        return 'Transaction("%s","%15s",%.2f)' % (self.date.strftime('%m/%d/%y'), self.desc[:15], self.amount)
