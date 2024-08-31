#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

import sys
from WebScraperBase import WebScraperBase
import re
from datetime import datetime

PAGE_START = r"https://www.schwab.com/public/workplace/get_started"
PAGE_READY = r"https://www.schwabplan.com/Net2/ContentPages/HomePages/DCParticipantHome.aspx"
PAGE_PERFORMANCE = r'https://www.schwabplan.com/Net2/ContentPages/Inquiries/PersonalPerf/PersonalPerformance.aspx?Graph=ActivitySummary'

PAT_ASOF = re.compile(r'as of ([\d/]+)')
PAT_AMT = re.compile(r'\$([\d.,]+)')

class SchwabScraper(WebScraperBase):
    def __init__(self, db, account):
        WebScraperBase.__init__(self, db, account)

    def getMainPage(self):
        return PAGE_START
    
    def onLoadFinishedImpl(self):
        frame = self.page.mainFrame()
        url = frame.url().toString()
        if url == PAGE_START:
            el = frame.findFirstElement('input[id="ssn"]')
            el.evaluateJavaScript("this.value = '%s'" % self.userNumber)
            el = frame.findFirstElement('input[id="pin"]')
            el.evaluateJavaScript("this.value = '%s'" % self.password)
            if self.password:
                el = frame.findFirstElement('input[id="SignonSubmit"]')
                el.evaluateJavaScript("this.click()")

        elif url == PAGE_READY:
            frame.setUrl(QUrl(PAGE_PERFORMANCE))

        elif url == PAGE_PERFORMANCE:
            elems = frame.findAllElements('td[class="EMVBMV"]')

            date = None
            amount = 0
            for el in elems:
                txt = str(el.toPlainText())
                m = PAT_ASOF.search(txt)
                if m:
                    date = datetime.strptime(m.group(1), '%m/%d/%Y')

                m = PAT_AMT.search(txt)
                if m:
                    amount = float(m.group(1).replace(',', ''))

            self.db.addBalanceSnapshot(self.account, date, amount)
            self.close()

if __name__ == "__main__":
    class Anon:
        pass

    account = Anon()
    account.userName = ''
    account.password = ''
    account.webCookieJar = ''

    class DbMock:
        def addBalanceSnapshot(self, *args, **kwargs):
            pass
    db = DbMock()

    app = QApplication(sys.argv)
    web = SchwabScraper(db, account)
    web.show()
    sys.exit(app.exec_())
