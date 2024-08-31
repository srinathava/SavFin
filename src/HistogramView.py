from __future__ import division
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import sys

import math

class MyGraphicsPolygonItem(QGraphicsPolygonItem, QObject):
    def __init__(self, rect, histogram, idx):
        QGraphicsPolygonItem.__init__(self, rect)
        self.histogram = histogram
        self.idx = idx

    def mouseDoubleClickEvent(self, e):
        self.histogram.onDoubleClick(self.idx)

class Histogram(QGraphicsView):
    doubleClicked = pyqtSignal(int)

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setMinimumSize(200, 200)
        self.posData = []
        self.negData = []
        self.w = 200
        self.h = 200

    @staticmethod
    def getError(rangeval, f, maxTicks):
        N = math.ceil(math.log10(1.0*rangeval/maxTicks/f))
        interval = f*math.pow(10, N)
        e = (interval - rangeval/10)/rangeval

        return (e, interval)

    @staticmethod
    def getTicks(minval, maxval, maxTicks):
        rangeval = maxval - minval
        factors = [1, 2, 5]
        errs_intervals = [Histogram.getError(rangeval, f, maxTicks) for f in factors]
        err_int_opt = min(errs_intervals, key=lambda x: x[0])
        interval = err_int_opt[1]
        minidx = int(math.ceil(minval/interval))
        maxidx = int(math.floor(maxval/interval))
        mintick = minidx*interval
        maxtick = maxidx*interval
        ticks = [tick*interval for tick in range(minidx, maxidx+1)]
        return ticks

    def resizeEvent(self, event):
        self.w = event.size().width()
        self.h = event.size().height()
        self.draw()

    def draw(self):
        w = self.w
        h = self.h

        scene = self.scene
        scene.clear()

        if not self.posData and not self.negData:
            return

        margin = 60.
        dataminx = -margin/(w - margin)
        datamaxx = 1.0

        datamaxy = max(self.posData)
        if self.negData:
            datamaxy = max(datamaxy, max(self.negData))
        datamaxy *= 1.1
        dataminy = -.1*datamaxy

        dataw = datamaxx - dataminx
        datah = datamaxy - dataminy
        if datah <= 0:
            return

        eps = 10
        # scalex*dataminx + dx = eps
        # scalex*datamaxx + dx = w-eps
        scalex = (w-2*eps)/dataw
        dx = eps - scalex*dataminx
        Tx = lambda x: scalex*x + dx
        
        # scaley*dataminy + dy = h-eps
        # scaley*datamaxy + dy = eps
        scaley = (2*eps-h)/datah
        dy = h - eps - scaley*dataminy
        Ty = lambda y: scaley*y + dy

        T = QTransform(scalex, 0, 0, scaley, dx, dy)

        def Tp(x, y): return T.map(QPointF(x, y))
        def Tl(x1, y1, x2, y2): return T.map(QLineF(x1, y1, x2, y2))
        def Tr(x1, y1, x2, y2): return T.map(QPolygonF(QRectF(x1, y1, x2, y2)))

        self.setSceneRect(0, 0, w, h)

        # draw Y tick marks
        ticks = self.getTicks(dataminy, datamaxy, math.floor(h/30))
        for tick in ticks:
            t = scene.addText(str(tick))
            y = Ty(tick)
            t.setPos(margin-t.boundingRect().width(), y)
            l = scene.addLine(margin, y, w, y)
            l.setPen(QColor(Qt.lightGray))

        # draw the xtick labels
        N = len(self.posData)
        for i in range(N):
            pos = T.map(QPointF(1.*i/N + 1./(2*N), 0))
            t = scene.addText(self.xTickLabels[i])
            t.setPos(pos.x() - t.boundingRect().width()/2, pos.y())

        self.drawHist(scene, self.posData, T, QColor(Qt.green), 0)
        if self.negData:
            self.drawHist(scene, self.negData, T, QColor(Qt.red), 1)

        # draw X/Y axes
        scene.addLine(Tl(dataminx, 0, datamaxx, 0))
        scene.addLine(Tl(0, dataminy, 0, datamaxy))

    def onDoubleClick(self, idx):
        self.doubleClicked.emit(idx)

    def drawHist(self, scene, data, T, col, off):
        N = len(data)
        xstart = 1./(2*N) - 0.4/N
        penColor = col.darker()
        brushColor = col.lighter()
        brushColor.setAlphaF(0.8)
        for (i, d) in enumerate(data):
            r = T.map(QPolygonF(QRectF(1.*i/N + xstart + 0.4*off/N, 0, 0.8/N, d)))
            gr = MyGraphicsPolygonItem(r, self, i)
            gr.setPen(penColor)
            gr.setBrush(brushColor)

            r = scene.addItem(gr)

            t = scene.addText(str(d))
            pos = T.map(QPointF(1.*i/N + 1./(2*N) + 0.4*off/N, d))
            t.setPos(pos.x() - t.boundingRect().width()/2, pos.y() - t.boundingRect().height())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QWidget()
    layout = QVBoxLayout()
    view = Histogram()
    view.xTickLabels = ['Jan', 'Feb', 'Mar', 'Apr']
    view.posData = [3, 4, 6, 1]
    view.negData = [2, 1, 7, 2]
    layout.addWidget(view)
    widget.setLayout(layout)
    widget.show()
    sys.exit(app.exec_())
