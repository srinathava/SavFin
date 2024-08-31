from SavfinData import SavfinData
from Transaction import Transaction
from Account import Account
from datetime import datetime
import csv
from os import path

def getTestData():
    reader = csv.reader(open(r'chase-jan-2010-to-jun-2011.csv'))
    rows = [r for r in reader]

    toNames = set([r[-1] for r in rows])
    accounts = []
    acctNameToAcctMap = {}

    paths = set([r[-1] for r in rows])
    compound_paths = [p for p in paths if '/' in p]
    for p in compound_paths:
        while 1:
            (p, name) = path.split(p)
            if not p:
                break
            paths.add(p)

    for tn in paths:
        acct = Account(tn, Account.Expense)
        acctNameToAcctMap[tn] = acct
        accounts.append(acct)

    for p in paths:
        acct = acctNameToAcctMap[p]
        (parentPath, name) = path.split(p)
        if parentPath:
            parentAcct = acctNameToAcctMap[parentPath]
            parentAcct.addChild(acct)

    rootExpenseAccount = Account('All Expenses', Account.Expense)

    for acct in accounts:
        if not acct.parent:
            rootExpenseAccount.addChild(acct)

    rootExpenseAccount.setPath()
    accounts.append(rootExpenseAccount)

    chase_visa = Account('Chase VISA', Account.Liability)
    accounts.append(chase_visa)

    transactions = []
    for r in rows:
        t = Transaction()
        t.date = datetime.strptime(r[0], '%m/%d/%y')
        t.desc = r[1]
        t.accountFrom = chase_visa
        t.accountTo = acctNameToAcctMap[r[3]]

        amtstr = r[2]
        amtstr = amtstr.replace('$', '')
        t.amount = float(amtstr)

        transactions.append(t)

    # for t in transactions:
    #     print t

    db = SavfinData()
    db.transactions = transactions
    db.accounts = accounts
    db.rules = []

    db.rootExpenseAccount = rootExpenseAccount

    return db

def saveTestData():
    import pickle
    db = getTestData()
    pickle.dump(db, open('sample.savfin', 'w'))

if __name__ == "__main__":
    saveTestData()
