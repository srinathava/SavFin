#!/usr/bin/env python

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

from WebScraperBase import WebScraperBase
from OfxUtils import importOfxTransactionsFromFile
from cStringIO import StringIO

PAGE_START = r'https://www.dcu.org/index.html'
PAGE_READY = r'https://www.dcu-online.org/onlineserv/HB/HomeBanking.cgi'
PAGE_EXPORT = r'https://www.dcu-online.org/onlineserv/HB/Summary.cgi?state=export&primaryButton=ACCOUNTS&secondaryButton=EXPORT'

class DcuScraper(WebScraperBase):
    def __init__(self, db, account):
        super(DcuScraper, self).__init__(db, account)

        self.gotSavingsInfo = False
        self.gotCheckingInfo = False
        self.numQfxFiles = 0

    def getMainPage(self):
        return PAGE_START

    def onLoadFinishedImpl(self):
        frame = self.page.mainFrame()
        if frame.url().toString() == PAGE_START:
            el = frame.findFirstElement('input[name="userNumber"]')
            el.evaluateJavaScript("this.value = '%s'" % self.userNumber)
            el = frame.findFirstElement('input[name="password"]')
            el.evaluateJavaScript("this.value = '%s'" % self.password)
            if self.password:
                el = frame.findFirstElement('input[name="login"]')
                el.evaluateJavaScript("this.click()")

        if frame.url().toString() == PAGE_READY:
            frame.setUrl(QUrl(PAGE_EXPORT))

        elif frame.url().toString() == PAGE_EXPORT:
            # select[name="ref"] // D0: savings, D1: checking 1 2 in list
            # nextStartMonth
            # nextStartDay
            # nextStartYear
            # nextEndMonth
            # nextEndDay
            # nextEndYear
            # select[name="typeList"] // QFX (2nd) 0 based indexing
            if not self.gotSavingsInfo:
                self.gotSavingsInfo = True
                el = frame.findFirstElement('select[name="ref"]')
                el.evaluateJavaScript('this.selectedIndex = 1')
                el = frame.findFirstElement('select[name="typeList"]')
                el.evaluateJavaScript('this.selectedIndex = 2')
                el = frame.findFirstElement('input[type="submit"]')
                el.evaluateJavaScript('this.click()')
                return
            
            if not self.gotCheckingInfo:
                self.gotCheckingInfo = True
                el = frame.findFirstElement('select[name="ref"]')
                el.evaluateJavaScript('this.selectedIndex = 2')
                el = frame.findFirstElement('select[name="typeList"]')
                el.evaluateJavaScript('this.selectedIndex = 2')
                el = frame.findFirstElement('input[type="submit"]')
                el.evaluateJavaScript('this.click()')
                return

    def replyFinished(self, reply):
        type = reply.rawHeader('Content-type')
        if reply in self.ignoredReplies:
            return

        if 'application/vnd.intu.qfx' in type:
            self.numQfxFiles += 1
            ofxString = reply.readAll()
            importOfxTransactionsFromFile(self.db, StringIO(ofxString))

            if self.numQfxFiles == 2:
                self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    web = DcuScraper()
    web.show()
    sys.exit(app.exec_())
