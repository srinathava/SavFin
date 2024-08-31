from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ui.SimpleRuleManager import Ui_SimpleRuleManager
from CompleteLineEdit import CompleteLineEdit
from AddRuleDialog import AddRuleDialog

class RuleEditorDelegate(QItemDelegate):
    def __init__(self, db, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)
        self.db = db

    def createEditor(self, parent, option, index):
        accountPaths = [a.path for a in self.db.accounts if not a.children]
        lineEdit = CompleteLineEdit(parent, accountPaths)
        return lineEdit

    def setModelData(self, lineEdit, model, index):
        model.setData(index, QVariant(lineEdit.text()), Qt.EditRole)

    def setEditorData(self, lineEdit, index):
        model = index.model()
        txt = model.data(index, Qt.DisplayRole)
        lineEdit.setText(txt)

class SimpleRuleManager(QDialog, Ui_SimpleRuleManager):
    def __init__(self, db, parent=None):
        self.db = db

        QDialog.__init__(self, parent)
        self.setupUi(self)

        ruleEditor = RuleEditorDelegate(self.db)
        self.rulesTableView.setItemDelegateForColumn(1, ruleEditor)
        self.rulesTableView.setItemDelegateForColumn(2, ruleEditor)

        self.addButton.clicked.connect(self.addNewRule)
        self.rulesTableView.initDb(self.db)

        self.deleteButton.clicked.connect(self.deleteRule)
        self.setMinimumWidth(800)

        self.moveUpButton.clicked.connect(lambda: self.move(-1))
        self.moveDownButton.clicked.connect(lambda: self.move(+1))
        self.runAllRulesButton.clicked.connect(lambda: self.db.runAllRules())

        self.exportButton.clicked.connect(self.exportRules)
        self.importButton.clicked.connect(self.importRules)

    def exportRules(self):
        filename = QFileDialog.getSaveFileName(self, 'Save file...', '', 'Savfin Rule Files (*.savfin_rules)')
        filename = str(filename)

        txt = ''
        for r in self.db.rules:
            txt += '\t'.join([r.pattern, r.fromPath, r.toPath]) + '\n'

        with open(filename, 'w') as f:
            f.write(txt)

    def importRulesFromFile(self, filename):
        with open(filename) as f:
            lines = f.read().splitlines()
            for l in lines:
                (pattern, fromPath, toPath) = l.split('\t')
                self.db.addSimpleRule(pattern, fromPath, toPath)

    def importRules(self):
        files = QFileDialog.getOpenFileNames(self,
                'Choose a saved rule file...', '',
                'Savfin Rule Files (*.savfin_rules)')

        if not files:
            return

        files = [str(f) for f in files]

        for f in files:
            self.importRulesFromFile(f)

    def addNewRule(self):
        addRuleDialog = AddRuleDialog(self.db)

        if addRuleDialog.exec_():
            self.db.addSimpleRule(addRuleDialog.pattern,
                    addRuleDialog.fromAccountPath,
                    addRuleDialog.toAccountPath)

    def deleteRule(self):
        index = self.rulesTableView.currentIndex()
        if not index.isValid():
            return

        rule = self.db.rules[index.row()]
        self.db.deleteRule(rule)

    def move(self, dir):
        index = self.rulesTableView.currentIndex()
        if not index.isValid():
            return

        model = self.rulesTableView.model()
        newIndex = model.index(index.row() + dir, index.column())
        if not newIndex.isValid():
            return

        self.db.moveRule(index.row(), dir)

        self.rulesTableView.selectionModel().clear()
        self.rulesTableView.selectionModel().setCurrentIndex(newIndex,
                QItemSelectionModel.Select)
