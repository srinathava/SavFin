from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import sys

# stolen from http://www.cppblog.com/biao/archive/2009/10/31/99873.html

class CompleteLineEdit(QLineEdit):
    def __init__(self, parent=None, words=[]):
        QLineEdit.__init__(self, parent)

        self.words = words
        self.listView = QListView(self)
        self.model = QStringListModel(self)
        self.listView.setWindowFlags(Qt.ToolTip)

        self.textEdited.connect(self.setCompleter)
        self.listView.clicked.connect(self.completeText)

    def keyPressEvent(self, e):
        if self.listView.isHidden():
            if e.key() == Qt.Key_Down:
                self.listView.show()
            else:
                QLineEdit.keyPressEvent(self, e)
                return

        if not self.listView.model():
            self.setCompleter('')
            return

        count = self.listView.model().rowCount()
        currentIndex = self.listView.currentIndex()
        if e.key() == Qt.Key_Down:
            row = currentIndex.row() + 1
            if row >= count:
                row = 0

            index = self.listView.model().index(row, 0)
            self.listView.setCurrentIndex(index)

        elif e.key() == Qt.Key_Up:
            row = currentIndex.row() - 1
            if row < 0:
                row = count - 1

            index = self.listView.model().index(row, 0)
            self.listView.setCurrentIndex(index)

        elif e.key() == Qt.Key_Escape:
            self.listView.hide()

        elif e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
            if currentIndex.isValid():
                text = self.listView.currentIndex().data().toString()
                self.setText(text)

            self.listView.hide()

        else:
            self.listView.hide()
            QLineEdit.keyPressEvent(self, e)

    def setCompleter(self, text):
        text = str(text).lower()

        strList = [w for w in self.words if text in w.lower()]
        if not strList:
            self.listView.hide()
            return

        self.model.setStringList(strList)
        self.listView.setModel(self.model)
        index = self.model.index(0, 0)
        self.listView.setCurrentIndex(index)

        self.listView.setMinimumWidth(self.width())
        self.listView.setMaximumWidth(self.width())

        p = QPoint(0, self.height())
        x = self.mapToGlobal(p).x()
        y = self.mapToGlobal(p).y()

        self.listView.move(x, y)
        self.listView.show()

    def completeText(self, index):
        text = index.data().toString()
        self.setText(text)
        self.listView.hide()

def main():
    words = ["Biao", "Bin", "Huang", "Hua", "Hello", "BinBin", "Hallo"]

    app = QApplication(sys.argv)
    w = QWidget()
    layout = QHBoxLayout()

    le = CompleteLineEdit(None, words)
    button = QPushButton('OK')

    layout.addWidget(le)
    layout.addWidget(button)

    w.setLayout(layout)
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

