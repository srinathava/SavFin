from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from AccountSummary import getAccountSummary, AccountSummaryNode
from Account import *
import locale
from config import *

class NodeInfo:
    def __init__(self):
        self.labels = ['', '']
        self.account = None
        self.checked = None
        self.font = None

def currency(amt):
    return locale.currency(amt, '$', True)

def nodesForNode(rootNode):
    nodes = []
    for n in rootNode.children:
        node = NodeInfo()
        label = n.acct.name
        if n.children:
            label = '+ ' + label

        if not n.enabled:
            f = QFont()
            f.setItalic(True)
            node.font = f

        node.checked = Qt.Checked if n.enabled else Qt.Unchecked
        node.labels = [label, currency(n.total)]
        node.account = n.acct

        nodes.append(node)

    return nodes

def upNode(rootNode):
    node = NodeInfo()
    node.labels = ['..', '']
    node.account = rootNode.acct.parent
    return node

def totalNode(rootNode):
    node = NodeInfo()
    label = 'Total'
    if rootNode.parent:
        label = '%s (%s)' % (label, rootNode.acct.name)

    node.labels = [label, currency(rootNode.total)]

    f = QFont()
    f.setItalic(True)
    f.setBold(True)
    node.font = f

    node.account = rootNode.acct

    return node

def getNodesForSummary(rootExpenseNode, rootIncomeNode):
    nodes = []

    if rootExpenseNode.parent:
        nodes.append(upNode(rootExpenseNode))

    nodes += nodesForNode(rootExpenseNode)
    nodes.append(totalNode(rootExpenseNode))

    nodes.append(NodeInfo())

    if rootIncomeNode.parent:
        nodes.append(upNode(rootIncomeNode))

    nodes += nodesForNode(rootIncomeNode)
    nodes.append(totalNode(rootIncomeNode))

    nodes.append(NodeInfo())

    return nodes

class AccountSummaryTableModel(QAbstractTableModel):
    HEADERS = ('Account', 'Total')
    accountEnableChanged = pyqtSignal()

    def __init__(self, rootExpenseNode, rootIncomeNode):
        QAbstractTableModel.__init__(self)
        self.initNodes(rootExpenseNode, rootIncomeNode)

    def initNodes(self, rootExpenseNode, rootIncomeNode):
        self.rootExpenseNode = rootExpenseNode
        self.rootIncomeNode = rootIncomeNode
        self.nodes = getNodesForSummary(rootExpenseNode, rootIncomeNode)
        node = NodeInfo()
        node.labels = [self.getTotalName(), currency(self.getTotal())]
        self.nodes.append(node)

    def getTotal(self):
        tot = self.rootIncomeNode.total - self.rootExpenseNode.total
        return tot

    def getTotalName(self):
        return 'Savings'

    def data(self, index, role):
        if not index.isValid() or index.row() > len(self.nodes): 
            return QVariant() 

        node = self.nodes[index.row()]
        if role == Qt.FontRole:
            return QVariant(node.font)
        elif (role == Qt.CheckStateRole and index.column() == 0):
            return QVariant(node.checked)
        elif (role == Qt.TextAlignmentRole and index.column() == 1):
            return Qt.AlignRight
        elif role != Qt.DisplayRole: 
            return QVariant() 

        return QVariant(node.labels[index.column()])

    def rowCount(self, parent):
        return len(self.nodes)

    def columnCount(self, parent):
        return 2

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.HEADERS[col])
        return QVariant()

    def flags(self, index):
        flags = QAbstractTableModel.flags(self, index)
        if index.column() == 0:
            flags |= Qt.ItemIsUserCheckable

        return flags

    def setData(self, index, value, role):
        ni = self.nodes[index.row()]
        account = ni.account
        account.enabled = (not account.enabled)
        self.accountEnableChanged.emit()
        return True

    def setRootNodes(self, rootExpenseNode, rootIncomeNode):
        self.initNodes(rootExpenseNode, rootIncomeNode)
        self.layoutChanged.emit()

class AccountSummaryView(QTableView):
    rootNodeChanged = pyqtSignal()

    def __init__(self, parent=None, tableModelClass=AccountSummaryTableModel):
        super(QTableView, self).__init__(parent)

        self.rootExpenseAccount = None
        self.rootIncomeAccount = None
        self.tableModelClass = tableModelClass

        self.setStyleSheet('border: none;')
        self.setColumnWidth(0, 150)
        self.verticalHeader().setDefaultSectionSize(16)

        self.doubleClicked.connect(self.onDoubleClicked)

    def setRootNodes(self, rootExpenseNode, rootIncomeNode):
        self.rootExpenseAccount = rootExpenseNode.acct
        self.rootIncomeAccount = rootIncomeNode.acct

        if not self.model():
            self.setModel(self.tableModelClass(rootExpenseNode, rootIncomeNode))
        else:
            self.model().setRootNodes(rootExpenseNode, rootIncomeNode)

    def onDoubleClicked(self, index):
        acct = self.model().nodes[index.row()].account
        if acct:
            if acct.type == Account.Expense:
                self.rootExpenseAccount = acct
            elif acct.type == Account.Income:
                self.rootIncomeAccount = acct

        self.rootNodeChanged.emit()

if __name__ == '__main__':
    from testdata import getTestData
    db = getTestData()

    def foobar(index):
        print index.model()

    nodes = getAccountSummary(db)
    app = QApplication(sys.argv)
    view = AccountSummaryView(nodes)
    view.doubleClicked.connect(foobar)
    view.show()

    app.exec_()
