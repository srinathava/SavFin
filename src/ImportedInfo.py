class ImportedAccountInfo:
    def __init__(self):
        self.accountId = ''
        self.beginBalance = None
        self.endBalance = None
        self.transactions = []

class ImportedInfo:
    def __init__(self):
        self.importedAccountInfos = []
        self.accountIdToAccountInfoMap = {}

    def addImportedAccount(self, accountId):
        if accountId not in self.accountIdToAccountInfoMap:
            accountInfo = ImportedAccountInfo()
            accountInfo.accountId = accountId

            self.accountIdToAccountInfoMap[accountId] = accountInfo
            self.importedAccountInfos.append(accountInfo)

        return self.accountIdToAccountInfoMap[accountId]

    
