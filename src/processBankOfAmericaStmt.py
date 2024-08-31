import re
from datetime import datetime
from Transaction import Transaction
from PdfParser import PdfParser
from QfxParser import getQfxTransactions
from ImportedInfo import ImportedInfo, ImportedAccountInfo

PAT_TRANS = re.compile(r'''\s*
        (?P<date>\d\d/\d\d/\d\d)\s*
        (?P<desc>\S.*)\s{3,}
        (?P<amount>-?(\d+,)?(\d+).(\d+))
        ''',
        re.VERBOSE)

PAT_CHECK = re.compile(r'''
(?P<check>\s*
    (?P<date>\d\d/\d\d/\d\d)\s+
    (?P<checkNum>\d+\*?)\s+
    (?P<amount>-?(\d+,)?(\d+)\.(\d+))
)
''', re.VERBOSE)

PAT_ACCOUNT_HEADER = re.compile(r'''\s*
Account\snumber:\s*(?P<accountNum>(\d|\s)+)
''', re.VERBOSE | re.I)

PAT_STMT_PERIOD = re.compile(r'for (?P<begin>\w+ \d{2}, \d{4}) to (?P<end>\w+ \d{2}, \d{4})')
PAT_DATE = re.compile(r'\s*(\d\d-\d\d)')

class BankOfAmericaStmtPdfParser(PdfParser):
    def __init__(self, fileName):
        PdfParser.__init__(self, fileName)
        self.transactions = None
        self.importedInfo = None

    def processFile(self):
        try:
            self.processFileImpl()
        except EOFError:
            pass

    def processFileImpl(self):
        self.skipToLineContaining('bankofamerica.com')
        self.importedInfo = ImportedInfo()
        while 1:
            if self.processHeader():
                pass
            elif self.processCheck():
                pass
            elif self.processTransaction():
                pass

            self.nextLine()

    def processHeader(self):
        m = PAT_ACCOUNT_HEADER.match(self.line.strip())
        if not m:
            return False
        
        accountId = m.group('accountNum').replace(' ', '')

        importedAccountInfo = self.importedInfo.addImportedAccount(accountId)
        self.transactions = importedAccountInfo.transactions

        return True

    def processCheck(self):
        m = None
        for m in PAT_CHECK.finditer(self.line):
            self.addTransaction(m.group('date'), 'Check %s' % m.group('checkNum'), m.group('amount'))

        return m is not None

    def processTransaction(self):
        m = PAT_TRANS.match(self.line)
        if not m:
            return False

        self.addTransaction(m.group('date'), m.group('desc'), m.group('amount'))
        return True

    def addTransaction(self, dateStr, descStr, amountStr):
        t = Transaction()
        t.date = datetime.strptime(dateStr, '%m/%d/%y')

        amount = amountStr.replace(',', '')
        amount = float(amount)

        t.amount = -amount
        t.desc = descStr

        self.transactions.append(t)

def getBankOfAmericaTransactionsPdf(fileName):
    parser = BankOfAmericaStmtPdfParser(fileName)
    parser.processFile()
    return parser.importedInfo

if __name__ == "__main__":
    import sys

    for file in sys.argv[1:]:
        parser = BankOfAmericaStmtPdfParser(file)
        parser.processFile()
        for accountInfo in parser.importedInfo.importedAccountInfos:
            print 'Account %s' % accountInfo.accountId
            for t in accountInfo.transactions:
                print "   %s" % t

