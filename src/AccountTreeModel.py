from PyQt4.QtCore import *
from TreeModel import TreeModel
from Account import Account

class AccountTreeModel(TreeModel):
    def __init__(self, db, parent=None):
        self.db = db
        TreeModel.__init__(self, db.rootOfAllAccounts, parent)

        self.currentDragIndex = None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return (Qt.ItemIsEnabled | 
                Qt.ItemIsSelectable | 
                Qt.ItemIsEditable |
                Qt.ItemIsDragEnabled |
                Qt.ItemIsDropEnabled)

    def supportedDropActions(self): 
        return Qt.CopyAction | Qt.MoveAction 

    def setData(self, index, value, role):
        if role != Qt.EditRole:
            return False

        if not index.isValid():
            return False

        account = index.internalPointer()
        account.name = str(value.toString())
        account.setPath()

        self.dataChanged.emit(index, index)
        return True

    def removeNode(self, account):
        self.db.removeAccount(account)

    def mimeTypes(self):
        return ['savfin/accountName']

    def newNode(self, parent):
        return self.db.addAccount(parent, 'new_account')

    def mimeData(self, indexes):
        mimedata = QMimeData()
        mimedata.setData('savfin/accountName', 'blah')
        # This seems hacky.
        self.currentDragIndex = indexes[0]
        return mimedata

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat('savfin/accountName'):
            return False

        if not self.currentDragIndex:
            return False

        fromIndex = self.currentDragIndex
        toIndex = parent

        if not self.db.canReparent(fromIndex.internalPointer(), toIndex.internalPointer()):
            return False

        if not self.beginMoveRows(fromIndex.parent(), fromIndex.row(),
                fromIndex.row(), toIndex, self.rowCount(toIndex)):
            return

        self.db.reparentAccount(fromIndex.internalPointer(), toIndex.internalPointer())

        self.endMoveRows()
        self.currentDragIndex = None
        return True
