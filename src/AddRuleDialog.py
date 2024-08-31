from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.AddRule import Ui_AddRule

class AddRuleDialog(QDialog, Ui_AddRule):
    def __init__(self, db, transaction):
        QDialog.__init__(self)
        self.db = db
        self.setupUi(self)

        accountPaths = [a.path for a in db.accounts if len(a.children) == 0]
        self.fromEdit.words = accountPaths
        self.toEdit.words = accountPaths

        self.pattern = transaction.desc if transaction else ''
        self.patternEdit.setText(self.pattern)
        self.fromAccountPath = ''
        self.toAccountPath = ''

    def accept(self):
        self.pattern = str(self.patternEdit.text())
        self.fromAccountPath = str(self.fromEdit.text())
        self.toAccountPath = str(self.toEdit.text())
        self.setDuplicate = bool(self.setDuplicateCheck.isChecked())

        self.db.addSimpleRule(self.pattern,
                self.fromAccountPath,
                self.toAccountPath,
                self.setDuplicate)

        QDialog.accept(self)

