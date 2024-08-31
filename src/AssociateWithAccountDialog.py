from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.AssociateWithAccountDialog import Ui_AssociateWithAccountDialog

class AssociateWithAccountDialog(QDialog, Ui_AssociateWithAccountDialog):
    def __init__(self, db, accountId, *args, **kwargs):
        super(AssociateWithAccountDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        origLabel = self.label.text()
        origLabel.replace('...', '%s' % accountId)
        self.label.setText(origLabel)

        self.accountLineEdit.words = [a.path for a in db.accounts if (not a.children)]
        self.accountPath = ''

    def accept(self):
        self.accountPath = str(self.accountLineEdit.text())
        super(AssociateWithAccountDialog, self).accept()
