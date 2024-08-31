from ofxparse import OfxParser
from Transaction import Transaction

def getQfxTransactions(fileName, PAT_BOGUS_TRANS):
    ofxInfo = OfxParser.parse(file(fileName))
    ofxTransactions = ofxInfo.account.statement.transactions
    transactions = []
    for ofxTrans in ofxTransactions:
        if PAT_BOGUS_TRANS.search(ofxTrans.payee):
            continue

        t = Transaction()

        t.date = ofxTrans.date
        t.desc = (ofxTrans.payee + ' ' + ofxTrans.memo).strip()
        t.amount = -float(ofxTrans.amount)
        transactions.append(t)
    return transactions
