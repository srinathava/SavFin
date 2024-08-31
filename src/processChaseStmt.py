import re
from datetime import datetime
from PdfParser import PdfParser
from Transaction import Transaction
from ImportedInfo import ImportedAccountInfo, ImportedInfo

PAT_TRANS = re.compile(r'''\s*
        (?P<date>\d\d/\d\d)\s*
        (?P<desc>.*)\s{5,}
        (?P<amount>-?(\d+,)?(\d+)?\.(\d\d))''',
        re.VERBOSE)
PAT_DATE = re.compile(r'\s*(\d\d/\d\d)')
PAT_DATE_RANGE = re.compile(r'Opening/Closing Date\s*(?P<start>\d\d/\d\d/\d\d) - (?P<end>\d\d/\d\d/\d\d)')
PAT_TRANS_HEADER = re.compile(r'Transaction\s+Merchant Name or Transaction Description')
PAT_BOGUS_TRANS = re.compile(r'payment - thank you', re.I)
PAT_ACCOUNT_NUM = re.compile(r'\s*Account\sNumber:\s(?P<accountNum>((\d{4})\s?){4})', re.I)

PAT_PREV_BALANCE = re.compile(r'Previous Balance\s*\$(?P<amount>(\d+,)?(\d+))', re.I)
PAT_NEW_BALANCE = re.compile(r'New Balance\s*\$(?P<amount>(\d+,)?(\d+))', re.I)

class ChaseStmtPdfParser(PdfParser):
    def __init__(self, fileName):
        PdfParser.__init__(self, fileName)
        self.importedInfo = None
        self.transactions = []

    def processFile(self):
        try:
            self.processFileImpl()
        except EOFError:
            pass

    def processFileImpl(self):
        # self.skipToLineContaining('CARDMEMBER SERVICE')

        m = self.skipToLineMatching(PAT_ACCOUNT_NUM)
        accountNum = m.group('accountNum').replace(' ', '').strip()

        m = self.skipToLineMatching(PAT_PREV_BALANCE)
        beginBalance = -self.parseAmount(m.group('amount'))

        m = self.skipToLineMatching(PAT_NEW_BALANCE)
        endBalance = -self.parseAmount(m.group('amount'))

        m = self.skipToLineMatching(PAT_DATE_RANGE)
        startDate = datetime.strptime(m.group('start'), '%m/%d/%y')
        endDate = datetime.strptime(m.group('end'), '%m/%d/%y')

        self.month = startDate.month
        self.year = startDate.year

        try:
            while 1:
                self.skipToLineContaining('ACCOUNT ACTIVITY')
                self.processTransactions()
        except EOFError:
            pass

        for t in self.transactions:
            if t.date.month < self.month:
                t.date.replace(year=self.year+1)
            else:
                t.date.replace(year=self.year)

        self.importedInfo = ImportedInfo()
        accountInfo = self.importedInfo.addImportedAccount(accountNum)

        accountInfo.transactions = self.transactions
        accountInfo.beginBalance = (startDate, beginBalance)
        accountInfo.endBalance = (endDate, endBalance)

    def processTransactions(self):
        while 1:
            m = self.skipToLineMatching(PAT_TRANS)
            self.getTransFromMatch(m)

    def getTransFromMatch(self, m):
        # append year so that we can parse feb 29th dates.
        fulldate = '%d/%s' % (self.year, m.group('date'))
        date = datetime.strptime(fulldate, '%Y/%m/%d')
        if date.month < self.month:
            date = date.replace(year=self.year+1)
        else:
            date = date.replace(year=self.year)

        amount = self.parseAmount(m.group('amount'))

        desc = self.removeSpaces(m.group('desc'))

        trans = Transaction()
        trans.date = date
        trans.amount = amount
        trans.desc = desc

        if PAT_BOGUS_TRANS.search(trans.desc):
            trans.isDuplicate = True
        
        self.transactions.append(trans)

def getChaseTransactionsPdf(file):
    parser = ChaseStmtPdfParser(file)
    parser.processFile()
    return parser.importedInfo

def getChaseTransactionsQfx(file):
    return getQfxTransactions(file, PAT_BOGUS_TRANS)

if __name__ == "__main__":
    import sys

    transactions = []
    for filename in sys.argv[1:]:
        parser = ChaseStmtPdfParser(filename)
        parser.processFile()
        info = parser.importedInfo.importedAccountInfos[0]
        print "%s: %s" % (info.beginBalance[0], info.beginBalance[1])
        print "%s: %s" % (info.endBalance[0], info.endBalance[1])
        print info.transactions

