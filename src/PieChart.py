from __future__ import division
import math
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import sys

COLORS = ['Green',
'Yellow',
'Red',
'Orange',
'LightBlue',
'Teal',
'Navy']
NUM_COLORS = len(COLORS)

class PieChart(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMinimumSize(200, 200)
        self.data = []
        self.labels = []
        self.w = 200
        self.h = 200

    def resizeEvent(self, event):
        self.w = event.size().width()
        self.h = event.size().height()
        self.draw()

    def draw(self):
        w = self.w
        h = self.h

        scene = self.scene
        scene.clear()

        total = sum(self.data)
        if total <= 0:
            return

        self.setSceneRect(-w/2, -h/2, w, h)

        rad = min([w/2, h/2]) - 50
        circRect = QRectF(-rad,-rad,2*rad,2*rad)

        startang = 60
        endang = 120

        def addSector(startang, endang):
            path = QPainterPath()
            path.moveTo(0,0)
            path.arcTo(circRect, startang, endang-startang)
            path.lineTo(0,0)
            ang = (startang+endang)/2
            p = QTransform().rotate(-ang).map(QPointF(0,0))
            path.translate(p)
            arc = self.scene.addPath(path)
            return arc

        def addRadialLabel(ang, label, color):
            p = QTransform().rotate(-ang).map(QPointF(rad,0))
            t = scene.addText(label)
            tr = t.boundingRect()
            if p.x() < 0:
                p = p - QPointF(tr.width(), 0)
            if p.y() < 0:
                p = p - QPointF(0, tr.height())
            t.setPos(p)
            return t

        def drawPie(startang, endang, label, col):
            s = addSector(startang, endang)
            t = addRadialLabel((startang+endang)/2, label)

        data_labels = zip(self.data, self.labels)
        data_labels.sort(key=lambda dl: -dl[0])
        data_labels = [dl for dl in data_labels if dl[0]/total > 0.02]

        rest = total - sum([dl[0] for dl in data_labels])
        if rest > 0:
            data_labels.append([rest, 'rest'])

        startang = 30
        i = 0
        colidx = 0
        for dl in data_labels:
            endang = startang + (dl[0]/total)*360

            colstr = COLORS[colidx]
            col = QColor(colstr)
            s = addSector(startang, endang)
            t = addRadialLabel((startang+endang)/2, dl[1], colstr)
            s.setPen(col.darker())
            s.setBrush(col)
            # t.setDefaultTextColor(col)

            startang = endang
            i += 1
            colidx += 1
            if colidx >= NUM_COLORS:
                colidx = 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QWidget()
    layout = QVBoxLayout()
    view = PieChart()
    view.data = [1, 2, 3]
    view.labels = ['foo', 'bar', 'baz']
    layout.addWidget(view)
    widget.setLayout(layout)
    widget.show()
    sys.exit(app.exec_())

