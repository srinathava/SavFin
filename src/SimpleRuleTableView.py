from PyQt4.QtCore import *
from PyQt4.QtGui import *
from SimpleRuleTableModel import *

class SimpleRuleTableView(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.verticalHeader().setDefaultSectionSize(16)

    def initDb(self, db):
        self.db = db
        self.setModel(SimpleRuleTableModel(self.db))

        self.setColumnWidth(1, 250)
        self.setColumnWidth(2, 250)
