import re
from datetime import datetime
from Transaction import Transaction
from PdfParser import PdfParser
from QfxParser import getQfxTransactions
from ImportedInfo import ImportedInfo, ImportedAccountInfo

__all__ = ['getDcuTransactions', 'getDcuTransactionsQfx']

PAT_STMT_PERIOD = re.compile(r'THE DCU WAY\s*(?P<accountNum>\S+)\s*(?P<start>\d\d-\d\d-\d\d)\s*to\s*(?P<end>\d\d-\d\d-\d\d)')

PAT_TRANSACTION = re.compile(r'''\s*(?P<date>(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\d\d)
\s*
(?P<desc>.*)''', re.VERBOSE | re.IGNORECASE)

PAT_AMOUNTS = re.compile(r'''(?P<sign>-?)(?P<qty>(\d|\.|,)+)
\s+
(?P<bal>(\d|\.|,)+)
\s*$
''', re.VERBOSE)

PAT_DATE = re.compile(r'\s*(?P<date>(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\d\d)', re.IGNORECASE)

PAT_NEW_BALANCE = re.compile(r'NEW BALANCE')

PAT_BOGUS_TRANS = re.compile(r'TRANSFER')

PAT_ACCT_HEADER = re.compile(r'(primary savings|free checking)\s*acct# (?P<accountNum>\d+)', re.IGNORECASE)

class DcuStmtPdfParser(PdfParser):
    def __init__(self, fileName):
        PdfParser.__init__(self, fileName)
        self.importedInfo = None
        self.transactions = []
        self.accountNum = ''
        self.year = 0
        self.month = 0

    def processFile(self):
        try:
            self.getStatementPeriod()
            self.processTransactions()
            self.processTransactions()
        except EOFError:
            pass

    def getStatementPeriod(self):
        m = self.skipToLineMatching(PAT_STMT_PERIOD)
        self.accountNum = m.group('accountNum')
        self.importedInfo = ImportedInfo()

        startDate = datetime.strptime(m.group('start'), '%m-%d-%y')

        self.month = startDate.month
        self.year = startDate.year

    def processTransactions(self):
        m = self.skipToLineMatching(PAT_ACCT_HEADER)
        accountId = '%sS%s' % (self.accountNum, m.group('accountNum'))

        accountInfo = self.importedInfo.addImportedAccount(accountId)
        self.transactions = accountInfo.transactions

        self.skipToLineMatching(PAT_TRANSACTION)
        while 1:
            self.processTransaction()
            if PAT_NEW_BALANCE.search(self.line):
                return
            if self.isEmpty():
                return

    def beginsWithDate(self):
        return PAT_DATE.match(self.line)

    def getTransFromLine(self):
        self.line = self.line.strip()
        amts = PAT_AMOUNTS.search(self.line)
        qty = amts.group('qty')
        sign = amts.group('sign')
        restofline = self.line[:-len(amts.group(0))]

        m = PAT_TRANSACTION.match(restofline)
        trans = Transaction()

        fulldate = '%s%d' % (m.group('date'), self.year)
        date = datetime.strptime(fulldate, '%b%d%Y')
        if date.month < self.month:
            date = date.replace(year=self.year+1)
        else:
            date = date.replace(year=self.year)
        trans.date = date

        trans.amount = -float((sign + qty).replace(',', ''))

        trans.desc = self.removeSpaces(m.group('desc').strip())

        return trans

    def processTransaction(self):
        trans = self.getTransFromLine()

        while 1:
            self.nextLine()
            if self.beginsWithDate() or self.isEmpty():
                break
            else:
                trans.desc += ' ' + self.removeSpaces(self.line.strip())

        self.transactions.append(trans)

def getDcuTransactionsPdf(file):
    parser = DcuStmtPdfParser(file)
    parser.processFile()
    return parser.importedInfo

def getDcuTransactionsQfx(fileName):
    return getQfxTransactions(fileName, PAT_BOGUS_TRANS)

if __name__ == "__main__":
    import sys

    for file in sys.argv[1:]:
        parser = DcuStmtPdfParser(file)
        parser.processFile()
        print parser.transactions
