from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.MasterPasswordDialog import Ui_MasterPasswordDialog

class MasterPasswordDialog(QDialog, Ui_MasterPasswordDialog):
    def __init__(self, *args, **kwargs):
        super(MasterPasswordDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.okButton.clicked.connect(self.onOkButtonPressed)
        self.cancelButton.clicked.connect(self.reject)

        self.password = None

    def onOkButtonPressed(self):
        pass1 = str(self.passwordLineEdit.text())
        pass2 = str(self.confirmPasswordLineEdit.text())
        if pass1 == pass2:
            self.password = pass1
            self.accept()
        else:
            self.statusLabel.setText('Passwords do not match!')

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = MasterPasswordDialog()
    main.show()
    app.exec_()
