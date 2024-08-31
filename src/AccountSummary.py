from datetime import datetime, timedelta
from Account import *

class AccountSummaryNode(object):
    def __init__(self, acct):
        self.acct = acct
        self.amount = 0

        self.children = []
        self.parent = None
        self.total = 0

    def addChild(self, ch):
        self.children.append(ch)
        ch.parent = self

    @property
    def enabled(self):
        return self.acct.enabled

    @enabled.setter
    def enabled(self, value):
        self.acct.enabled = value

    @property
    def data(self):
        return [self.acct.name, self.total, self.enabled]

    def propagateTotals(self):
        for ch in self.children:
            ch.propagateTotals()

        self.total = self.amount
        for ch in self.children:
            if ch.enabled:
                self.total += ch.total

        self.children.sort(key=lambda n: -n.total)

def getAccountSummary(db, datemin=None, datemax=None, rootAccount=None, gatherUncategorized=True, signTo=1):
    if not datemin:
        datemin = db.datemin 

    if not datemax:
        datemax = db.datemax

    miscAcct = Account('<uncategorized>')

    miscAcct.parent = db.rootExpenseAccount
    miscAcct.setPath()

    miscNode = AccountSummaryNode(miscAcct)

    acct2node = {}
    for acct in db.accounts:
        n = AccountSummaryNode(acct)
        acct2node[acct] = n

    for acct in db.accounts:
        n = acct2node[acct]
        for ch in acct.children:
            nch = acct2node[ch]
            n.addChild(nch)

    acct2node[miscAcct] = miscNode

    acct2node[db.rootExpenseAccount].addChild(miscNode)

    for trans in db.transactions:
        if (not trans.isDuplicate and 
                trans.date.date() >= datemin.date() and 
                trans.date.date() <= datemax.date()):
            if trans.accountFrom:
                nfrom = acct2node[trans.accountFrom]
                nfrom.amount -= signTo*trans.amount
            if trans.accountTo:
                nto = acct2node[trans.accountTo]
                nto.amount += signTo*trans.amount

            if not trans.accountTo:
                miscNode.amount += signTo*trans.amount

    if not rootAccount:
        rootAccount = db.rootExpenseAccount

    if rootAccount in acct2node:
        rootNode = acct2node[rootAccount]
    else:
        rootNode = miscNode

    rootNode.propagateTotals()

    return rootNode
