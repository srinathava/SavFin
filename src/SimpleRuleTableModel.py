from PyQt4.QtCore import *

class SimpleRuleTableModel(QAbstractTableModel):
    FROM_COL = 0
    DESC_COL = 1
    TO_COL = 2
    DUP_COL = 3
    NUM_COLS = 4

    def __init__(self, db, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.db = db
        self.db.emitter.rulesChanged.connect(self.layoutChanged)

    def rowCount(self, parent):
        return len(self.db.rules)

    def columnCount(self, parent):
        return self.NUM_COLS

    def data(self, index, role):
        if not index.isValid(): 
            return QVariant() 

        rule = self.db.rules[index.row()]
        
        if index.column() == self.DUP_COL:
            if role == Qt.CheckStateRole:
                return Qt.Checked if rule.setDuplicate else Qt.Unchecked
            else:
                return QVariant()

        if role != Qt.DisplayRole and role != Qt.EditRole: 
            return QVariant() 

        col = index.column()
        if col == self.FROM_COL:
            return rule.fromPath
        elif col == self.TO_COL:
            return rule.toPath
        elif col == self.DESC_COL:
            return rule.pattern
        else:
            return QVariant()

    def setData(self, index, value, role):
        if not index.isValid():
            return False

        rule = self.db.rules[index.row()]

        if role == Qt.CheckStateRole and index.column() == 3:
            isChecked = (value == Qt.Checked)
            rule.setDuplicate = isChecked
            return True

        if role == Qt.EditRole:
            value = str(value.toString())
            account = None
            if value:
                account = self.db.getAccountFromName(value)

            if index.column() == 0:
                rule.pattern = value
            if index.column() == 1:
                rule.accountFrom = account
            elif index.column() == 2:
                rule.accountTo = account
            else:
                return False

            return True

        return False
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled

        flags = QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable
        if index.column() == 3:
            flags |= Qt.ItemIsUserCheckable

        return flags
        
    def headerData(self, col, orientation, role):
        headers = ['Pattern', 'Account From', 'Account To', 'Mark Duplicate']
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == self.FROM_COL:
                return 'From Account'
            elif col == self.TO_COL:
                return 'To Account'
            elif col == self.DESC_COL:
                return 'pattern'
            elif col == self.DUP_COL:
                return 'Mark duplicate'

        return QVariant()
