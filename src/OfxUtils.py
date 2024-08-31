from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Transaction import Transaction
from ofxparse import OfxParser
import re
from datetime import datetime, timedelta
from cStringIO import StringIO
from OfxBa import getOfxResponse

from AssociateWithAccountDialog import AssociateWithAccountDialog
from ImportedInfo import ImportedInfo, ImportedAccountInfo

from xml.sax.saxutils import unescape as _unescape
def unescape(str):
    return _unescape(str, {'&#39;': "'", '&#039;': "'", '&quot;': '"', '&QUOT;': '"'})

PAT_MULT_SPACE = re.compile(r'\s+')
def removeSpaces(instr):
    return PAT_MULT_SPACE.sub(' ', instr.strip())

def getOfxTransactionsFromInfo(ofxInfo):
    ofxTransactions = ofxInfo.account.statement.transactions
    transactions = []
    for ofxTrans in ofxTransactions:
        t = Transaction()

        t.date = ofxTrans.date
        t.desc = unescape(removeSpaces(ofxTrans.payee + ' ' + ofxTrans.memo))
        t.desc = unescape(t.desc)
        t.amount = -float(ofxTrans.amount)
        t.ofxId = ofxTrans.id

        transactions.append(t)

    balance = float(ofxInfo.account.statement.balance)
    endDate = ofxInfo.account.statement.end_date

    return (transactions, (endDate, balance))

def importOfxTransactionsFromFile(db, ofxFile):
    if type(ofxFile) is str:
        with open(ofxFile) as f:
            ofxInfo = OfxParser.parse(f)
    else:
        ofxInfo = OfxParser.parse(ofxFile)

    accountId = ofxInfo.account.number
    importedInfo = ImportedInfo()
    accountInfo = importedInfo.addImportedAccount(accountId)

    (accountInfo.transactions, accountInfo.endBalance) = getOfxTransactionsFromInfo(ofxInfo)

    return importedInfo

    foundAccount = None
    for account in db.accounts:
        if account.accountId == accountId:
            foundAccount = account
            break

    if not foundAccount:
        d = AssociateWithAccountDialog(db, accountId)
        if not d.exec_():
            return

        foundAccount = db.getAccountFromName(d.accountPath)
        foundAccount.accountId = accountId

    (numNew, numDups) = db.addTransactions(transactions, foundAccount, balance, endDate)

    title = 'Import status'
    msg = 'Imported %d transactions, discarded %d duplicates' % (numNew, numDups)
    msgBox = QMessageBox(QMessageBox.Information, title, msg)
    msgBox.exec_()

class OfxImportThread(QThread):
    def __init__(self, config, fromdate):
        QThread.__init__(self)
        self.config = config
        self.fromdate = fromdate
        self.response = ''

    def run(self):
        self.response = getOfxResponse(self.config, self.fromdate)

def importOfxTransactionsFromWeb(db, account):
    password = account.password
    if not password:
        (password, ok) = QInputDialog.getText(None, 'Enter password',
                'Password', QLineEdit.Password)
        if not ok:
            return

        password = str(password)

    if not password:
        return

    config = {
                'acctId': account.accountId,
                'user': account.userName,
                'password' : password,
                'fid': account.ofx_fid,
                'fiorg': account.ofx_fiorg,
                'url': account.ofx_url,
                'bankid': account.ofx_bankid,
                'acctType': account.ofx_acctType
            }

    # Import for the last 6 months or so by default
    fromdate = datetime.today() - timedelta(180)
    for t in db.transactions:
        if t.accountFrom == account:
            if t.date > fromdate:
                fromdate = t.date

    ofxImporter = OfxImportThread(config, fromdate - timedelta(30))
    ofxImporter.start()

    progressDialog = QProgressDialog('Importing OFX transactions', '&Cancel', 0, 0)
    progressDialog.setWindowModality(Qt.WindowModal)

    ofxImporter.finished.connect(progressDialog.close)

    progressDialog.exec_()

    if not ofxImporter.isFinished():
        return

    ofxTxt = ofxImporter.response
    try:
        importOfxTransactionsFromFile(db, StringIO(ofxTxt))
    except:
        print '!'*80
        print 'Error importing OFX transactions from the web. This is what was scraped from the web: '
        print '='*80
        print ofxTxt
        print '='*80
        raise

