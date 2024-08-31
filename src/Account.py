from operator import itemgetter

# This needs to be in sync with the UI
OFX_ACCT_TYPES = ['CCSTMT', 'CHECKING', 'SAVINGS', 'MONEYMRKT', 'CREDITLINE']

class Account:
    Asset = 0
    Liability = 1
    Income = 2
    Expense = 3

    def __init__(self, name='', type=Expense):
        self.name = name
        self.type = type
        self.initialAmount = 0
        self.children = []
        self.parent = None
        self.path = ''

        # Used when reading OFX files
        self.accountId = ''
        self.userName = ''
        self.password = ''

        # Used to automatically pull data using ofx-ba.py
        self.ofx_fid = ''
        self.ofx_fiorg = ''
        self.ofx_url = ''
        self.ofx_bankid = ''

        self.ofx_acctTypeIdx = 1

        # This is a string which is the name of the scraper.
        self.scraperClass = ''

        # When using web-scraping, we need to enable cookies otherwise
        # banks ask us annoying questions everytime. This is basically the
        # serialized cookie information.
        self.webCookieJar = ''

        # These is a list of (date, balance) tuples which is the snapshot
        # of the available balance of this account at various time points.
        # This only makes sense to use for asset/liability accounts.
        self.balanceSnapshots = []

        self.enabled = 1

    @property
    def ofx_acctType(self):
        return OFX_ACCT_TYPES[self.ofx_acctTypeIdx]

    def __setstate__(self, state):
        # calling __init__ ensures that newly added properties since the
        # pickle was saved also exist.
        self.__init__()
        for it in state:
            self.__dict__[it] = state[it]

        self.balanceSnapshots = [b for b in self.balanceSnapshots if b[0]]

        self.enabled = 1

    def addChild(self, ch):
        self.children.append(ch)
        ch.parent = self
        ch.setPath()

    def setPath(self):
        if self.parent:
            self.path = self.parent.path + '/' + self.name
        else:
            self.path = '/' + self.name

        for ch in self.children:
            ch.setPath()

    def removeChild(self, ch):
        self.children.remove(ch)
        ch.parent = None

    def __repr__(self):
        return 'Account(%s)' % self.name

    @property
    def data(self):
        return [self.name]

    def hasOfxInfo(self):
        if ( ( self.accountId == '' ) or
             ( self.userName == '' ) or
             ( self.ofx_fid == '' ) or
             ( self.ofx_fiorg == '' ) or
             ( self.ofx_url == '' ) or
             ( self.ofx_acctType == '' ) or
             ( self.ofx_bankid == '' ) ):
            return False
        else:
            return True

    def addBalanceSnapshot(self, date, amt):
        if self.balanceSnapshots and self.balanceSnapshots[-1][0] == date:
            return

        self.balanceSnapshots.append([date, amt])
        self.balanceSnapshots.sort(key=itemgetter(0))
