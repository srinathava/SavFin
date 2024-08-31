from __future__ import division
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import math
from datetime import datetime, timedelta
from operator import attrgetter, itemgetter
import operator
import locale
import time

from Account import Account
from AccountSummaryTableModel import AccountSummaryView, AccountSummaryTableModel

LEFT_MARGIN = 45
RIGHT_MARGIN = 20
TOP_MARGIN = 50
BOTTOM_MARGIN = 30

TIME_RESOLUTION = 15

COLORS = ['Green',
'Red',
'Blue',
'Orange',
'Brown',
'Teal',
'Navy']

def getError(rangeval, f, maxTicks):
    N = math.ceil(math.log10(1.0*rangeval/maxTicks/f))
    interval = f*math.pow(10, N)
    e = (interval - rangeval/10)/rangeval

    return (e, interval, N, f)

def getTicks(minval, maxval, maxTicks):
    rangeval = maxval - minval
    factors = [1, 2, 5]
    errs_intervals = [getError(rangeval, f, maxTicks) for f in factors]
    err_int_opt = min(errs_intervals, key=itemgetter(0))

    interval = err_int_opt[1]
    N = err_int_opt[2]
    f = err_int_opt[3]

    minidx = int(math.ceil(minval/interval))
    maxidx = int(math.floor(maxval/interval))

    amounts = [f*tick*10**(N-3) for tick in range(minidx, maxidx+1)]
    labels = ['%dK$' % amt for amt in amounts]
    ticks = [tick*interval for tick in range(minidx, maxidx+1)]
    return (ticks, labels)

def addMonth(t, count=1):
    nm = t.month + count
    ny = t.year
    if nm > 12:
        nm = 1
        ny += 1

    t2 = datetime(ny, nm, t.day)
    return t2

class CursorLine(QGraphicsLineItem):
    def __init__(self, line, axis):
        super(CursorLine, self).__init__(line)
        self.setAcceptHoverEvents(True)
        self.axis = axis
        self.line = line

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            event.ignore()
            return

        self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        self.axis.drawCursorAtX(event.pos().x())

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)

class LabelBox(QGraphicsSimpleTextItem):
    def __init__(self, txt, color):
        super(LabelBox, self).__init__(txt)
        self.txt = txt
        self.color = color
        self.setZValue(3)

    def boundingRect(self):
        fm = QFontMetricsF(self.font())
        r = fm.boundingRect(self.txt)
        return QRectF(3, 0, r.width()+5, r.height()+5)

    def paint(self, painter, option, style):
        painter.save()
        painter.setPen(QColor(self.color))
        painter.setBrush(QBrush(QColor('white')))
        painter.drawRect(self.boundingRect())
        painter.restore()

        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.txt)

class TimeAxis(QGraphicsView):
    def __init__(self):
        super(TimeAxis, self).__init__()

        self.setRenderHint(QPainter.Antialiasing)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.setMinimumSize(400, 400)

        self.w = 400
        self.h = 400

        self.xmin = 0
        self.xmax = 1
        self.ymin = 0
        self.ymax = 1

        tnow = datetime.now()
        self.tmin = datetime(tnow.year, 1, 1)
        self.tmax = datetime(tnow.year, 12, 31)
        self.addFcn = lambda t: addMonth(t, 1)

        self.labels = []
        self.lines = []

        self.cursorLabelItems = []
        self.cursorLineItem = []
        self.dateLabelItem = None

    def time2x(self, t):
        dt = (t - self.tmin).total_seconds()
        trange = (self.tmax - self.tmin).total_seconds() 
        xrange_ = self.xmax - self.xmin
        return dt/trange*xrange_ + self.xmin

    def setTransform(self):
        scalex = (self.w - LEFT_MARGIN - RIGHT_MARGIN)/(self.xmax - self.xmin)
        dx = LEFT_MARGIN

        #   ypmin = m22*ymin + dy
        #   ypmax = m22*ymax + dy
        #
        # m22 = (ypmax - ypmin)/(ymax - ymin)
        # dy = ypmin - m22*ymin
        ypmin = self.h - BOTTOM_MARGIN
        ypmax = TOP_MARGIN

        scaley = (ypmax - ypmin)/(self.ymax - self.ymin)
        dy = ypmin - scaley*self.ymin
        self.T = QTransform(scalex, 0, 0, scaley, dx, dy)

    def resizeEvent(self, event):
        self.w = event.size().width()
        self.h = event.size().height()
        self.setSceneRect(0, 0, self.w, self.h)
        self.draw()

    def draw(self):
        self.scene.clear()
        if not self.updateLimits():
            t = self.scene.addText('No data')
            t.setPos(self.w/2, self.h/2)
            return

        self.setTransform()
        self.getTicks()
        self.drawGrid()
        self.drawData()
        # At this point, draw a bunch of rectangles to "clip" the
        # unecessary stuff.
        self.drawWhiteRects()

        self.drawAxisBox()
        self.drawYTicks()
        self.drawTimeTicks()

    def drawWhiteRects(self):
        white = QColor('white')
        pen = QPen(white)
        brush = QBrush(white)

        self.scene.addRect(0, 0, LEFT_MARGIN, self.h, pen, brush)
        self.scene.addRect(0, 0, self.w, TOP_MARGIN, pen, brush)
        self.scene.addRect(self.w - RIGHT_MARGIN, 0, RIGHT_MARGIN, self.h, pen, brush)
        self.scene.addRect(0, self.h - BOTTOM_MARGIN, self.w, BOTTOM_MARGIN, pen, brush)

    def getTicks(self):
        (self.ticks, self.ylabels) = getTicks(self.ymin, self.ymax, (self.h - TOP_MARGIN - BOTTOM_MARGIN)/30)

    def updateLimits(self):
        if not self.lines:
            now = datetime.now()
            self.ymin = 0
            self.ymax = 10
            return

        self.ymin = float('inf')
        self.ymax = -float('inf')
        allEmpty = True

        for line in self.lines:
            y = [p[1] for p in line if p[0] >= self.tmin and p[0] <= self.tmax]
            if not y:
                continue

            allEmpty = False
            self.ymin = min([self.ymin, min(y)])
            self.ymax = max([self.ymax, max(y)])

        if allEmpty:
            return False

        mid = (self.ymax + self.ymin)/2
        diff = self.ymax - self.ymin

        self.ymax = mid + diff/2*1.05
        self.ymin = mid - diff/2*1.05

        availWidth = self.w - LEFT_MARGIN - RIGHT_MARGIN
        minCellWidth = 100
        maxNumCells = availWidth/minCellWidth

        approxTimeDelta = timedelta(seconds = (self.tmax - self.tmin).total_seconds()/maxNumCells)
        self.addFcn = lambda t: t + approxTimeDelta

        return True

    def drawAxisBox(self):
        path = QPainterPath()
        path.moveTo(LEFT_MARGIN, TOP_MARGIN)
        path.lineTo(self.w - RIGHT_MARGIN, TOP_MARGIN)
        path.lineTo(self.w - RIGHT_MARGIN, self.h - BOTTOM_MARGIN)
        path.lineTo(LEFT_MARGIN, self.h - BOTTOM_MARGIN)
        path.lineTo(LEFT_MARGIN, TOP_MARGIN)
        pen = QPen()
        pen.setWidth(2)
        self.scene.addPath(path, pen)

    def drawYTicks(self):
        for (tick, label) in zip(self.ticks, self.ylabels):
            pt = self.T.map(QPointF(0, tick))
            txt = self.scene.addText(label)
            tr = txt.boundingRect()
            txt.setPos(pt - QPointF(tr.width(), tr.height()/2))

    def drawTimeTicks(self):
        t = self.tmin
        while t <= self.tmax:
            x = self.time2x(t)
            pt = self.T.map(QPointF(x, 0))
            pt.setY(self.h - BOTTOM_MARGIN)

            txt = t.strftime('%m/%d/%y')
            fm = QFontMetricsF(self.font())
            r = fm.boundingRect(txt)

            pt.setX(pt.x() - r.width()/2)

            txtObj = self.scene.addText(t.strftime('%m/%d/%y'))
            txtObj.setPos(pt)

            t = self.addFcn(t)

    def drawGrid(self):
        pen = QPen(QColor('#ddd'))

        t = self.tmin
        while t <= self.tmax:
            x = self.time2x(t)
            line = QLineF(x, self.ymin, x, self.ymax)
            self.scene.addLine(self.T.map(line), pen)
            t = self.addFcn(t)

        for tick in self.ticks:
            line = QLineF(self.xmin, tick, self.xmax, tick)
            self.scene.addLine(self.T.map(line), pen)

    def setTimeLimits(self, tmin, tmax):
        self.tmin = tmin
        self.tmax = tmax
        self.update()

    def drawData(self):
        for (i, line) in enumerate(self.lines):
            color = COLORS[i % len(COLORS)]
            self._drawLine(line, color)

        dt = timedelta(seconds=(self.tmax - self.tmin).total_seconds()/2)
        cursorTime = self.tmin + dt
        self.drawCursor(cursorTime)

    def drawCursor(self, t):
        self.drawCursorLabels(t)
        self.drawCursorLine(t)
        self.drawTimeLabel(t)

    def drawCursorAtX(self, x):
        if x > self.w - RIGHT_MARGIN:
            x = self.w - RIGHT_MARGIN

        if x <  LEFT_MARGIN:
            x = LEFT_MARGIN

        self.cursorLineItem.setLine(x, TOP_MARGIN, x, self.h - BOTTOM_MARGIN)

        ratio = (x - LEFT_MARGIN) / (self.w - LEFT_MARGIN - RIGHT_MARGIN)
        total_seconds = (self.tmax - self.tmin).total_seconds()
        t = self.tmin + timedelta(seconds = total_seconds* ratio)
        for it in self.cursorLabelItems:
            self.scene.removeItem(it)

        self.drawCursorLabels(t)
        
        if self.dateLabelItem:
            self.scene.removeItem(self.dateLabelItem)
        self.drawTimeLabel(t)

    def drawTimeLabel(self, cursorTime):
        self.dateLabelItem = LabelBox(cursorTime.strftime('%m/%d/%y'), 'white')
        self.scene.addItem(self.dateLabelItem)

        x = self.time2x(cursorTime)
        p = QPointF(x, 0)
        pt = self.T.map(p)

        r = self.dateLabelItem.boundingRect()
        self.dateLabelItem.setPos(QPointF(pt.x() - r.width()/2, TOP_MARGIN - r.height() - 3))

    def drawCursorLabels(self, cursorTime):
        lineVals = []
        colors = []
        for (i, line) in enumerate(self.lines):
            interpVal = self.interpolate(line, cursorTime)
            lineVals.append(interpVal)
            colors.append(COLORS[i % len(COLORS)])

        assert len(lineVals) == len(self.labels)
        assert len(lineVals) == len(colors)

        labelData = zip(lineVals, self.labels, colors)
        labelData.sort(key = itemgetter(0))

        self.cursorLabelItems = []
        for (lval, label, color) in labelData:
            if lval != 0:
                self.cursorLabelItems.append(self.drawLabel(cursorTime,  lval, label, color))

        # Adjust the positions of the label items so that there is no
        # overlap. There is a possibility that this will push certain
        # labels over the top.
        lasty = float('inf')
        for item in self.cursorLabelItems:
            if item.pos().y() > lasty:
                pos = item.pos()
                pos.setY(lasty - 3)
                item.setPos(pos)

            lasty = item.pos().y() - item.boundingRect().height()

    def drawCursorLine(self, cursorTime):
        x = self.time2x(cursorTime)
        line = self.T.map(QLineF(x, self.ymin, x, self.ymax))

        self.cursorLineItem = CursorLine(line, self)

        pen = QPen(QColor('#aaa'))
        pen.setWidth(3)

        self.cursorLineItem.setPen(pen)

        self.scene.addItem(self.cursorLineItem)

    def interpolate(self, line, t):
        p = findLastPointBefore(line, t)
        if not p:
            return 0 #line[0][1]
        else:
            return p[1]

    def _drawLine(self, line, color):
        if not line:
            return

        points = []

        t0 = line[0][0]
        tend = line[-1][0]

        for (t, val) in line:
            x = self.time2x(t)
            p = QPointF(x, val)
            pt = self.T.map(p)
            points.append(pt)

        path = QPainterPath()
        path.moveTo(points[0])
        lastp = points[0]

        for pt in points[1:]:
            hp = QPointF(pt.x(), lastp.y())
            lastp = pt
            path.lineTo(hp)

            path.lineTo(pt)

        pen = QPen(QColor(color))
        pen.setWidthF(2)
        self.scene.addPath(path, pen)

    def drawLabel(self, t, val, label, color):
        x = self.time2x(t)
        p = QPointF(x, val)
        pt = self.T.map(p)
        txt = '%s - %s' % (locale.currency(val, '$', True), label)
        gt = LabelBox(txt, color)
        self.scene.addItem(gt)

        if pt.x() + gt.boundingRect().width() > self.w - RIGHT_MARGIN:
            pt.setX(pt.x() - gt.boundingRect().width() - 3)

        if pt.y() < TOP_MARGIN:
            pt.setY(TOP_MARGIN)

        gt.setPos(pt)
        return gt

    def addLine(self, line, label):
        self.lines.append(line)
        self.labels.append(label)

    def clear(self):
        self.scene.clear()
        self.lines = []
        self.labels = []

    def setTimeLimits(self, tmin, tmax):
        self.tmin = tmin
        self.tmax = tmax

class _AccountInfo(object):
    def __init__(self, account):
        self.account = account
        self.points = []
        self.amount = 0.0

def isAssetAccount(a):
    return a and (a.type == Account.Asset or a.type == Account.Liability)

def findLastPointBefore(points, t):
    lastPoint = None
    for p in points:
        if p[0] > t:
            return lastPoint
        else:
            lastPoint = p
    return lastPoint

class AssetSummaryTableModel(AccountSummaryTableModel):
    def __init__(self, *args, **kwargs):
        AccountSummaryTableModel.__init__(self, *args, **kwargs)

    def getTotal(self):
        return self.rootIncomeNode.total + self.rootExpenseNode.total

    def getTotalName(self):
        return 'Net worth'

class AssetViewRefresherThread(QThread):
    def __init__(self, db):
        QThread.__init__(self)
        self.db = db

        self.infoList = None
        self.allPoints = None
        self.assetSummary = None
        self.liabilitySummary = None

    def adjustPointsFromBalanceSnapshots(self, account, points):
        lastBalanceTime = datetime.min
        for (date, balance) in account.balanceSnapshots:
            # find last time point which is before date
            lastPoint = findLastPointBefore(points, date)
            if not lastPoint:
                continue

            # find what the balance was at that point
            offsetReqd = balance - lastPoint[1]

            # if abs(offsetReqd) > 50 and lastBalanceTime != datetime.min:
            #     print "***Warning***: Had to fudge the account %s by $%g after %s" % (account.name, offsetReqd, lastBalanceTime)

            # now add offsetReqd to all points after last balance point
            for p in points:
                if p[0] > lastBalanceTime:
                    p[1] += offsetReqd

            lastBalanceTime = date

        for (date, balance) in account.balanceSnapshots:
            points.append([date, balance])

        points.sort(key=itemgetter(0))

    def getTotalBalancePoints(self, infoList):
        def findBalanceBeforeTimePoint(points, t, idx):
            # Find the biggest index nextIndex
            #
            # s.t it satisfies the following three conditions 
            #
            #   nextIndex >= idx
            #   points[nextIndex - 1][0] < t
            #   points[nextIndex][0] >= t
            #
            # and then return the (points[nextIndex], nextIndex)

            lastBalance = 0
            nextIdx = idx
            for i in range(idx, len(points)):
                p = points[i]
                if p[0] <= t:
                    lastBalance = p[1]
                    nextIdx = i
                else:
                    break

            return (lastBalance, nextIdx)

        def findBalancesAt(points, times):
            balances = []
            prevIdx = 0
            for t in times:
                (balance, prevIdx) = findBalanceBeforeTimePoint(points, t, prevIdx)
                balances.append(balance)

            return balances

        allTimePoints = []
        for info in infoList:
            allTimePoints.extend([p[0] for p in info.points])

        allTimePoints.sort()

        totalBalancesAtAllTimePoints = [0] * len(allTimePoints)
        for info in infoList:
            interpolatedBalancesForThisAccount = findBalancesAt(info.points, allTimePoints)
            for i in range(len(totalBalancesAtAllTimePoints)):
                totalBalancesAtAllTimePoints[i] += interpolatedBalancesForThisAccount[i]

        allPoints = zip(allTimePoints, totalBalancesAtAllTimePoints)
        return allPoints

    def run(self):
        def isAssetTransaction(t):
            if t.isDuplicate:
                return False

            return isAssetAccount(t.accountFrom) or isAssetAccount(t.accountTo)

        assetAccounts = [a for a in self.db.accounts if isAssetAccount(a)]
        account2info = {}
        for a in assetAccounts:
            account2info[a] = _AccountInfo(a)

        assetTransactions = [t for t in self.db.transactions if isAssetTransaction(t)]
        assetTransactions.sort(key=attrgetter('date'))

        for (i, t) in enumerate(assetTransactions):
            fromIsAsset = isAssetAccount(t.accountFrom)
            toIsAsset = isAssetAccount(t.accountTo)

            if fromIsAsset:
                info = account2info[t.accountFrom]
                info.amount -= t.amount
                info.points.append([t.date, info.amount])

            if toIsAsset:
                info = account2info[t.accountTo]
                info.amount += t.amount
                info.points.append([t.date, info.amount])

        infoList = account2info.values()

        # Adjust all time points between the balance snapshots
        for info in infoList:
            self.adjustPointsFromBalanceSnapshots(info.account, info.points)

        self.infoList = [info for info in infoList if info.points and info.account.enabled]
        self.allPoints = self.getTotalBalancePoints(infoList)
        self.assetSummary = self.getAssetLiabilityAccountSummary(self.db.rootAssetAccount)
        self.liabilitySummary = self.getAssetLiabilityAccountSummary(self.db.rootLiabilityAccount)

    def getAssetLiabilityAccountSummary(self, rootAccount):
        class AssetLiabilitySummaryNode:
            def __init__(self, acct):
                self.acct = acct

                self.amount = 0
                self.total = 0

                self.children = []
                self.parent = None

                self.enabled = True

            def addChild(self, ch):
                self.children.append(ch)
                ch.parent = self

        summaryNode = AssetLiabilitySummaryNode(rootAccount)
        summaryNode.enabled = rootAccount.enabled
        pt = findLastPointBefore(rootAccount.balanceSnapshots, self.db.datemax)

        summaryNode.amount = pt[1] if pt else 0
        summaryNode.total = summaryNode.amount

        for ch in rootAccount.children:
            childSummaryNode = self.getAssetLiabilityAccountSummary(ch)
            summaryNode.addChild(childSummaryNode)
            if childSummaryNode.enabled:
                summaryNode.total += childSummaryNode.total

        return summaryNode

class AssetView(QWidget):
    def __init__(self):
        super(AssetView, self).__init__()

        self.axis = TimeAxis()
        self.assetLiabilityTableView = AccountSummaryView(tableModelClass=AssetSummaryTableModel)

        layout = QHBoxLayout()
        layout.addWidget(self.assetLiabilityTableView)
        layout.addWidget(self.axis)
        layout.setStretch(1, 1)
        self.setLayout(layout)
        self.db = None

    def initDb(self, db):
        self.db = db
        self.db.emitter.dataChanged.connect(self.refresh)
        self.db.emitter.datesChanged.connect(self.refresh)
        self.refreshSync()
        self.assetLiabilityTableView.model().accountEnableChanged.connect(self.refreshSync)

    def refreshSync(self):
        self.refresher = AssetViewRefresherThread(self.db)
        self.refresher.run()
        self.refresher.wait()
        self.redraw()

    def refresh(self):
        self.refresher = AssetViewRefresherThread(self.db)
        self.refresher.finished.connect(self.redraw)
        self.refresher.start()

    def redraw(self):
        self.axis.tmin = self.db.datemin
        self.axis.tmax = self.db.datemax

        self.axis.clear()
        for info in self.refresher.infoList:
            self.axis.addLine(info.points, info.account.name)

        if self.refresher.allPoints:
            self.axis.addLine(self.refresher.allPoints, 'Total')

        self.axis.setTimeLimits(self.db.datemin, self.db.datemax)
        self.axis.draw()
        self.assetLiabilityTableView.setRootNodes(self.refresher.assetSummary, self.refresher.liabilitySummary)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    locale.setlocale(locale.LC_ALL, '')
    widget = QWidget()
    layout = QVBoxLayout()
    view = TimeAxis()

    final = [0.8]
    def doit():
        view.addLine([(datetime(2011, 2, 1), 1.2), (datetime(2011, 10, 20), final[0])], 'foobar')
        final[0] -= 0.2

    layout.addWidget(view)
    button = QPushButton('Hello')
    button.clicked.connect(doit)

    layout.addWidget(button)

    widget.setLayout(layout)
    widget.show()
    sys.exit(app.exec_())
