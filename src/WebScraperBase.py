#!/usr/bin/env python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

class MyCookieJar(QNetworkCookieJar):
    def __init__(self, account):
        super(MyCookieJar, self).__init__()
        self.account = account

        try:
            cookieStr = account.webCookieJar
        except IOError:
            return

        self.setAllCookies(QNetworkCookie.parseCookies(cookieStr))

    def setCookiesFromUrl(self, newCookies, url):
        ret = super(MyCookieJar, self).setCookiesFromUrl(newCookies, url)

        str = ''
        for cookie in self.allCookies():
            if not cookie.isSessionCookie():
                str += cookie.toRawForm() + '\n'

        self.account.webCookieJar = str
        return ret

class MyWebView(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        layout = QVBoxLayout()

        self.urlBar = QLineEdit()
        self.urlBar.setReadOnly(True)

        self.webview = QWebView()

        layout.addWidget(self.urlBar)
        layout.addWidget(self.webview)

        self.setLayout(layout)

class WebScraperBase(QDialog):
    def __init__(self, db, account):
        super(WebScraperBase, self).__init__()

        self.db = db
        self.account = account
        self.userNumber = self.account.userName
        self.password = self.account.password

        self.webviewContainer = MyWebView()

        self.webview = self.webviewContainer.webview
        self.statusBar = QLabel()
        self.urlBar = self.webviewContainer.urlBar

        layout = QVBoxLayout()
        layout.addWidget(self.urlBar)
        layout.addWidget(self.webviewContainer)
        layout.addWidget(self.statusBar)
        self.setLayout(layout)

        jar = MyCookieJar(self.account)

        self.page = self.webview.page()
        self.page.mainFrame().load(QUrl(self.getMainPage()))

        self.page.networkAccessManager().sslErrors.connect(self.sslErrorHandler)
        self.page.networkAccessManager().setCookieJar(jar)
        self.page.setForwardUnsupportedContent(True)
        self.page.networkAccessManager().finished.connect(self.replyFinished)
        self.page.loadFinished.connect(self.onLoadFinished)
        self.page.loadProgress.connect(self.onLoadProgress)
        self.page.loadStarted.connect(self.onLoadProgress)

        self.ignoredReplies = set()

    def getMainPage(self):
        return 'http://www.google.com'

    @staticmethod
    def sslErrorHandler(reply, errorList):
        reply.ignoreSslErrors()
        for err in errorList:
            print err.errorString()

    def onLoadProgress(self, progress=0):
        self.urlBar.setText(self.page.mainFrame().url().toString())
        self.statusBar.setText('Loading (%g) ...' % progress)

    def onLoadFinished(self, ok):
        self.statusBar.setText('Ready')
        self.onLoadFinishedImpl()

    def replyFinished(self, reply):
        pass

