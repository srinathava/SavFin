from Account import Account
from Rule import SimpleRule
import datetime

# Accounts spec <<<
INCOME_ACCOUNTS_TREE = '''MathWorks
IBM
Interest
misc'''

EXPENSE_ACCOUNTS_TREE = '''rent
daycare
utilities
    electricity
    heat
    water
    sewage
    housekeeping
services
    phone
    cable
auto
    gas
    repairs
    insurance
groceries
    wholefoods
    shaws
    indian
    others
restaurants
    cafe
    mathworks
    other
entertainment
    books
    electronics
    movies
    netflix
    misc
misc
    nannaru
    gifts
    travel
    cash
    medical
    misc
baby
    toys
    diapers
    wipes
    misc
amazon'''

ASSET_ACCOUNTS_TREE = '''Bank of America (checking)
Bank of America (savings)
DCU (checking)
DCU (savings)'''

LIABILITY_ACCOUNTS_TREE = '''VISA'''
# >>>

from PyQt4.QtCore import QObject, pyqtSignal

def addMonth(t):
    t2 = t + datetime.timedelta(35)
    t2 = datetime.datetime(t2.year, t2.month, 1)
    return t2

def subMonth(t):
    m = t.month - 1
    y = t.year
    if m == 0:
        m = 12
        y = y - 1

    return datetime.datetime(y, m, 1)

def addWeek(t):
    if t.day >= 20:
        t2 = datetime.datetime(t.year, t.month, 1)
        t2 = addMonth(t2)
        t2 = t2 - datetime.timedelta(1)
    else:
        t2 = t + datetime.timedelta(7)

    return t2

class SavFinEmitter(QObject):
    dataChanged = pyqtSignal()
    rulesChanged = pyqtSignal()
    datesChanged = pyqtSignal()

    def __init__(self, db):
        QObject.__init__(self)
        self.db = db

class SavfinData:
    ITEMS_TO_SAVE = ['accounts', 'transactions', 'rules',
            'rootExpenseAccount', 'rootIncomeAccount', 'rootAssetAccount',
            'rootLiabilityAccount', 'datemin', 'datemax', 'masterPassword']

    def __init__(self):
        self.initDefaultProps()
        self.emitter = SavFinEmitter(self)
        self.getAccountTrees()
        self.setDuration(0)

    def initDefaultProps(self):
        self.accounts = []
        self.transactions = []
        self.rules = []
        self.rootExpenseAccount = None
        self.rootIncomeAccount = None
        self.rootAssetAccount = None
        self.rootLiabilityAccount = None
        self.rootOfAllAccounts = None
        self.datemin = None
        self.datemax = None
        self.minorStepFcn = None
        self.durationType = None
        self.masterPassword = ''
        self.stopNotifyCounter = 0

    def __getstate__(self):
        # Need to define this so that we can exclude the QObject stuff.
        # otherwise pickling this object doesn't work.
        dict = {}
        for it in self.ITEMS_TO_SAVE:
            dict[it] = self.__dict__[it]
        return dict

    def __setstate__(self, state):
        self.initDefaultProps()
        for it in self.ITEMS_TO_SAVE:
            if it in state:
                self.__dict__[it] = state[it]

        if not 'rootOfAllAccounts' in state:
            self.initRootOfAllAccounts()

        self.emitter = SavFinEmitter(self)

        self.setDurationType('Year To Date')

    DURATIONS = ['Year To Date', 'Yearly', 'Monthly', 'Past Year', 'All']

    def emitDataChanged(self):
        if self.stopNotifyCounter == 0:
            self.emitter.dataChanged.emit()

    def stopChangeNotifications(self):
        self.stopNotifyCounter += 1

    def startChangeNotifications(self):
        self.stopNotifyCounter -= 1
        if self.stopNotifyCounter == 0:
            self.emitDataChanged()

    @property
    def durationIndex(self):
        return self.DURATIONS.index(self.durationType)

    def setDuration(self, value):
        self.setDurationType(self.DURATIONS[value])

    def setDurationType(self, durationType):
        self.durationType = durationType
        oneDay = datetime.timedelta(1)

        durationType = self.durationType.lower()
        if durationType == 'all':
            self.datemin = min([t.date for t in self.transactions])
            self.datemax = max([t.date for t in self.transactions])
            self.minorStepFcn = addMonth

        elif durationType == 'yearly':
            today = datetime.datetime.today()
            year = self.datemin.year if self.datemin else today.year
            self.datemin = datetime.datetime(year, 1, 1)
            self.datemax = datetime.datetime(year, 12, 31)
            self.minorStepFcn = addMonth

        elif durationType == 'year to date':
            today = datetime.datetime.today()
            year = today.year
            self.datemin = datetime.datetime(year, 1, 1)
            self.datemax = today
            self.minorStepFcn = addMonth

        elif durationType == 'monthly':
            today = datetime.datetime.today()
            self.datemin = datetime.datetime(today.year, today.month, 1)
            self.datemax = addMonth(self.datemin) - oneDay
            self.minorStepFcn = addWeek

        elif durationType == 'past year':
            today = datetime.datetime.today()
            self.datemin = today.replace(year=today.year - 1)
            self.datemax = today
            self.minorStepFcn = addMonth

        self.emitter.datesChanged.emit()

    def setInterval(self, interval):
        (t1, t2) = interval
        self.datemin = t1
        self.datemax = t2
        if t2 - t1 > datetime.timedelta(35):
            self.durationType = 'Yearly'
            self.minorStepFcn = addMonth
        else:
            self.durationType = 'Monthly'
            self.minorStepFcn = addWeek

        self.emitter.datesChanged.emit()

    def setNextInterval(self):
        oneDay = datetime.timedelta(1)
        durationType = self.durationType.lower()

        if durationType == 'yearly':
            self.datemin = datetime.datetime(self.datemin.year+1, 1, 1)
            self.datemax = datetime.datetime(self.datemin.year+1, 1, 1)
            self.datemax = self.datemax - oneDay

        elif durationType in ['year to date', 'past year']:
            self.datemin = self.datemin.replace(year=self.datemin.year+1)
            self.datemax = self.datemax.replace(year=self.datemax.year+1)

        elif durationType == 'monthly':
            self.datemin = addMonth(self.datemin)
            self.datemax = addMonth(self.datemin) - oneDay

        self.emitter.datesChanged.emit()

    def setPrevInterval(self):
        oneDay = datetime.timedelta(1)
        durationType = self.durationType.lower()
        if durationType == 'yearly':
            self.datemin = datetime.datetime(self.datemin.year-1, 1, 1)
            self.datemax = datetime.datetime(self.datemin.year+1, 1, 1)
            self.datemax = self.datemax - oneDay

        elif durationType in ['year to date', 'past year']:
            self.datemin = self.datemin.replace(year=self.datemin.year-1)
            self.datemax = self.datemax.replace(year=self.datemax.year-1)

        elif durationType == 'monthly':
            self.datemin = subMonth(self.datemin)
            self.datemax = addMonth(self.datemin) - oneDay

        self.emitter.datesChanged.emit()

    def parseTree(self, rootName, spec, type):
        lines = spec.splitlines()
        root = Account(rootName, type)
        self.accounts.append(root)

        accountStack = [root]
        levelStack = [-1]
        for line in lines:
            name = line.lstrip()
            acct = Account(name, type)
            self.accounts.append(acct)
            curLevel = len(line) - len(name)

            # pop all accounts which are at the same or greater level of
            # indentation.
            while levelStack[-1] >= curLevel:
                levelStack.pop()
                accountStack.pop()

            accountStack[-1].addChild(acct)

            accountStack.append(acct)
            levelStack.append(curLevel)

        root.setPath()
        return root

    def initRootOfAllAccounts(self):
        self.rootOfAllAccounts = Account('All Accounts')
        self.rootOfAllAccounts.addChild(self.rootIncomeAccount)
        self.rootOfAllAccounts.addChild(self.rootExpenseAccount)
        self.rootOfAllAccounts.addChild(self.rootAssetAccount)
        self.rootOfAllAccounts.addChild(self.rootLiabilityAccount)

    def getAccountTrees(self):
        self.rootIncomeAccount = self.parseTree('Incomes', INCOME_ACCOUNTS_TREE, Account.Income)
        self.rootExpenseAccount = self.parseTree('Expenses', EXPENSE_ACCOUNTS_TREE, Account.Expense)
        self.rootAssetAccount = self.parseTree('Assets', ASSET_ACCOUNTS_TREE, Account.Asset)
        self.rootLiabilityAccount = self.parseTree('Liabilities', LIABILITY_ACCOUNTS_TREE, Account.Liability)
        self.initRootOfAllAccounts()

    def getAccountFromName(self, name, exact=False):
        if exact:
            accts_match = [acct for acct in self.accounts if name == acct.path]
        else:
            accts_match = [acct for acct in self.accounts if name in acct.path]
        if len(accts_match) == 0:
            return None
        elif len(accts_match) > 1:
            raise ValueError, "Too many accounts match this pattern"
        else:
            return accts_match[0]

    def addAccount(self, parent, name):
        newAcct = Account(name, parent.type)
        self.accounts.append(newAcct)
        parent.addChild(newAcct)
        self.emitDataChanged()
        return newAcct

    def removeAccount(self, account):
        self.accounts.remove(account)
        account.parent.removeChild(account)
        for t in self.transactions:
            if t.accountFrom == account:
                t.accountFrom = None
            if t.accountTo == account:
                t.accountTo = None

        self.emitDataChanged()

    def transactionExists(self, trans):
        for t in self.transactions:
            if ((t.accountFrom == trans.accountFrom) and
                    (t.amount == trans.amount) and 
                    abs((t.date.date() - trans.date.date()).days) <= 1):
                return True

        return False

    def adjustStartAmount(self, account, balance, endDate):
        b = 0
        for t in self.transactions:
            if t.date > endDate or t.isDuplicate:
                continue

            if t.accountFrom == account:
                b -= t.amount

            if t.accountTo == account:
                b += t.amount

        if b != 0:
            account.initialAmount = balance - b

    def addTransactions(self, transactions, account=None, balance=None, endDate=None):
        duplicates = 0

        newTransactions = []
        for trans in transactions:
            if not self.transactionExists(trans):
                newTransactions.append(trans)
            else:
                duplicates += 1

        for trans in newTransactions:
            for rule in self.rules:
                match = rule.run(trans)
                if match:
                    break

        self.transactions += newTransactions

        if account:
            account.balanceSnapshots.append((endDate, balance))

        self.emitDataChanged()
        return (len(newTransactions), duplicates)

    def deleteTransactions(self, transactions):
        delSet = set(transactions)
        self.transactions = [t for t in self.transactions if t not in delSet]
        self.emitDataChanged()

    def addSimpleRule(self, pattern, accountFromPath, accountToPath, setDuplicate):
        if accountFromPath:
            accountFrom = self.getAccountFromName(accountFromPath)
        else:
            accountFrom = None

        if accountToPath:
            accountTo = self.getAccountFromName(accountToPath)
        else:
            accountTo = None

        rule = SimpleRule(pattern, accountFrom, accountTo, setDuplicate)

        self.rules.append(rule)
        for t in self.transactions:
            rule.run(t)

        self.emitDataChanged()
        self.emitter.rulesChanged.emit()

    def deleteRule(self, rule):
        self.rules.remove(rule)
        self.emitter.rulesChanged.emit()

    def moveRule(self, index, dir):
        oldIndex = index
        newIndex = index + dir

        def outOfRange(idx):
            return (idx < 0 or idx >= len(self.rules))

        if outOfRange(oldIndex) or outOfRange(newIndex):
            return

        oldRule = self.rules[oldIndex]
        newRule = self.rules[newIndex]

        self.rules[oldIndex] = newRule
        self.rules[newIndex] = oldRule

        self.emitter.rulesChanged.emit()

    def runAllRules(self):
        for t in self.transactions:
            for r in self.rules:
                if r.run(t):
                    break

        self.emitDataChanged()

    def canReparent(self, child, newParent):
        if newParent.path.startswith(child.path + '/'):
            return False

        if child.parent == newParent:
            return False

        if child.type != newParent.type:
            return False

        return True

    def reparentAccount(self, child, newParent):
        if not self.canReparent(child, newParent):
            return

        # Make sure that newParent is not originally a descendent of child!
        origParent = child.parent
        origParent.removeChild(child)
        newParent.addChild(child)

        self.emitDataChanged()

    def addBalanceSnapshot(self, account, date, amt):
        account.addBalanceSnapshot(date, amt)
        self.emitDataChanged()
