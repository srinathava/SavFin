from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class TreeModel(QAbstractItemModel):
    '''
    Provides a proxy to the interface required by QAbstractItemModel

    Should be instantiated with a root object which has the following
    interface:

    class TreeItem:
        def __init__(self):
            self.parent = []
            self.children = []
            self.data = ()

    '''
    def __init__(self, root, parent=None):
        QAbstractItemModel.__init__(self, parent)
        self.root = root

    def columnCount(self, parentIndex):
        if parentIndex.isValid():
            return len(parentIndex.internalPointer().data)
        else:
            return len(self.root.data)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return QVariant()

        treeItem = index.internalPointer()
        return treeItem.data[index.column()]

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.root.data[section]

        return QVariant()

    def index(self, row, column, parentIndex):
        if not self.hasIndex(row, column, parentIndex):
            return QModelIndex()

        if not parentIndex.isValid():
            parentItem = self.root
        else:
            parentItem = parentIndex.internalPointer()

        if row < len(parentItem.children):
            childItem = parentItem.children[row]
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    @staticmethod
    def ownRowNum(item):
        return item.parent.children.index(item)

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        treeItem = index.internalPointer()

        parentItem = treeItem.parent
        if not parentItem:
            return QModelIndex()

        if parentItem == self.root:
            return QModelIndex()

        return self.createIndex(self.ownRowNum(parentItem), 0, parentItem)

    def rowCount(self, parentIndex):
        if parentIndex.column() > 0:
            return 0

        if not parentIndex.isValid():
            parentItem = self.root
        else:
            parentItem = parentIndex.internalPointer()

        return len(parentItem.children)

    def remove(self, index):
        if not index.isValid():
            return

        parentIdx = index.parent()
        node = index.internalPointer()
        self.beginRemoveRows(parentIdx, index.row(), index.row())
        self.removeNode(node)
        self.endRemoveRows()

    def newNode(self):
        raise ValueError, "Not implemented"

    def appendRow(self, index):
        if not index.isValid():
            return

        numRows = self.rowCount(index)

        node = index.internalPointer()
        self.beginInsertRows(index, numRows, numRows)
        self.newNode(index.internalPointer())
        self.endInsertRows()

def viewTree(root, name):
    app = QApplication(sys.argv)
    view = QTreeView()
    model = TreeModel(root)
    proxyModel = QSortFilterProxyModel()
    proxyModel.setSourceModel(model)

    view.setModel(proxyModel)
    view.setWindowTitle(name)
    view.show()
    view.setColumnWidth(0, 200)
    view.expandToDepth(0)
    view.setWindowState(Qt.WindowMaximized)

    view.setSortingEnabled(True)
    lastCol = len(root.data) - 1
    view.sortByColumn(lastCol, Qt.DescendingOrder)

    app.exec_()
