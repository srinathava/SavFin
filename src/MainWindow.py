from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.MainWindow import Ui_SavFin
from SavfinData import SavfinData
from CsvImporter import CsvImporter
from AddRuleDialog import AddRuleDialog
from SimpleRuleManager import *
from MasterPasswordDialog import MasterPasswordDialog
from AssociateWithAccountDialog import AssociateWithAccountDialog
from processChaseStmt import getChaseTransactionsPdf, getChaseTransactionsQfx
from processBankOfAmericaStmt import getBankOfAmericaTransactionsPdf
from processDcuStmt import getDcuTransactionsPdf, getDcuTransactionsQfx
from ofxparse import OfxParser
from Transaction import Transaction
from OfxUtils import importOfxTransactionsFromFile
import os
from os import path
import pickle
import re
from datetime import timedelta
import locale
import socket
import shutil
import tempfile
import subprocess

def is_exe(fpath):
    return path.isfile(fpath) and os.access(fpath, os.X_OK)

def which(program):
    fpath, fname = path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for p in os.environ["PATH"].split(os.pathsep):
            exe_file = path.join(p, program)
            if is_exe(exe_file):
                return exe_file

    return None

HOST = '127.0.0.1'
PORT = 50007
OPENSSL_PATH = which('openssl')
if not OPENSSL_PATH:
    OPENSSL_PATH = which('openssl.exe')

if not OPENSSL_PATH:
    # randomly choose this because this is the default path for open SSL
    # install on windows.
    OPENSSL_PATH = r'c:\OpenSSL-Win32\bin\openssl.exe'

if not is_exe(OPENSSL_PATH):
    OPENSSL_PATH = ''

ENCRYPTED_ON_HEADER = '--encrypted-1--'
ENCRYPTED_OFF_HEADER = '--encrypted-0--'

class ServerThread(QThread):
    somethingHappened = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))

        while 1:
            s.listen(1)
            conn, addr = s.accept()
            data = ''
            while 1:
                d = conn.recv(1024)
                if not d:
                    break
                data += d

            self.somethingHappened.emit(data)

class TempDirObject:
    def __enter__(self):
        self.origDir = os.getcwd()
        self.tempDir = tempfile.mkdtemp()
        os.chdir(self.tempDir)

    def __exit__(self, type, value, traceback):
        os.chdir(self.origDir)
        shutil.rmtree(self.tempDir)

def getPassword():
    (password, ok) = QInputDialog.getText(None, 'Enter master password',
                'Password', QLineEdit.Password)
    password = str(password)
    return password

def alertImportStatus(nums):
    numNew = nums[0]
    numDups = nums[1]

    title = 'Import status'
    msg = 'Imported %d transactions, discarded %d duplicates' % (numNew, numDups)
    msgBox = QMessageBox(QMessageBox.Information, title, msg)
    msgBox.exec_()

class MainWindow(QMainWindow, Ui_SavFin):
    def __init__(self):
        QMainWindow.__init__(self)
        locale.setlocale(locale.LC_ALL, '')

        self.setupUi(self)

        self.actionOpen.triggered.connect(self.openFile)
        self.actionImportStatement.triggered.connect(self.importStatement)
        self.actionSetMasterPassword.triggered.connect(self.setMasterPassword)

        self.actionSave.triggered.connect(self.saveFile)
        self.actionSaveAs.triggered.connect(self.saveFileAs)

        self.actionAddRule.triggered.connect(self.addRule)
        self.actionManageRules.triggered.connect(self.manageRules)

        self.inShowTimeExtents = False
        self.setupDurationCombo()
        self.nextIntervalButton.clicked.connect(self.setNextInterval)
        self.prevIntervalButton.clicked.connect(self.setPrevInterval)

        self.actionQuit.triggered.connect(QApplication.instance().quit)

        self.actionDetectDuplicates.triggered.connect(self.detectDuplicates)

        # self.ofxFileThread = ServerThread()
        # self.ofxFileThread.somethingHappened.connect(lambda filename: importOfxTransactionsFromFile(self.db, filename))
        # self.ofxFileThread.start()

        self.dirty = False

        self.recentFileActions = []
        self.setupRecentFiles()

        self.filename = ''
        self.db = SavfinData()
        self.initDb()

    def setupDurationCombo(self):
        self.durationCombo.clear()
        for d in SavfinData.DURATIONS:
            self.durationCombo.addItem(d)

        self.durationCombo.currentIndexChanged.connect(self.onDurationChanged)

    def setMasterPassword(self):
        d = MasterPasswordDialog()
        if d.exec_():
            self.db.masterPassword = d.password
            self.markDirty()

    def detectDuplicates(self, detectDuplicatesFlag):
        self.transactionsTab.detectDuplicates(detectDuplicatesFlag)

    def closeEvent(self, event):
        if self.dirty:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Confirm exit')
            msgBox.setText('<b>Document has unsaved changes</b>')
            msgBox.setInformativeText('Do you want to save your changes?')
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Save)
            msgBox.setIcon(QMessageBox.Warning)

            ret = msgBox.exec_()
            if ret == QMessageBox.Save:
                self.saveFile()
                event.accept()
            elif ret == QMessageBox.Discard:
                event.accept()
            elif ret == QMessageBox.Cancel:
                event.ignore()
        else:
            event.accept()

    def refreshTitle(self):
        if self.dirty:
            self.setWindowTitle('SavFin - (*) %s' % self.filename)
        else:
            self.setWindowTitle('SavFin - %s' % self.filename)

    def initDb(self):
        self.expenseReportTab.initDb(self.db)
        self.transactionsTab.initDb(self.db)
        self.selectedTransactionsTab.initDb(self.db, self.expenseReportTab)
        self.accountTreeView.initDb(self.db)
        self.accountInfoWidget.initDb(self.db)
        self.assetViewTab.initDb(self.db)
        self.refreshTitle()
        self.showTimeExtents()

        self.db.emitter.dataChanged.connect(self.showTimeExtents)
        self.db.emitter.dataChanged.connect(self.markDirty)
        self.db.emitter.datesChanged.connect(self.showTimeExtents)

    def markDirty(self):
        self.dirty = True
        self.refreshTitle()

    ################################################################################
    # Rules
    ################################################################################
    def addRule(self):
        tabName = self.tabWidget.currentWidget().objectName()
        transaction = None
        if (tabName == 'selectedTransactionsTab' or 
                tabName == 'transactionsTab'):
            transactions = self.tabWidget.currentWidget().getSelectedTransactions()
            if transactions:
                transaction = transactions[0]

        addRuleDialog = AddRuleDialog(self.db, transaction)
        addRuleDialog.exec_()

    def manageRules(self):
        manageRulesDialog = SimpleRuleManager(self.db)
        manageRulesDialog.exec_()

    ################################################################################
    # Time extent management
    ################################################################################
    def showTimeExtents(self):
        minTimeStr = self.db.datemin.strftime('%m/%d/%y')
        maxTimeStr = self.db.datemax.strftime('%m/%d/%y')

        self.inShowTimeExtents = True
        if self.db.datemax - self.db.datemin < timedelta(35):
            idx = self.db.DURATIONS.index(self.db.durationType)
            self.durationCombo.setCurrentIndex(idx)

        self.inShowTimeExtents = False
        self.timeExtentsLabel.setText('<b>Currently showing transactions between %s and %s.' % (minTimeStr, maxTimeStr))

    def onDurationChanged(self, value):
        if not self.inShowTimeExtents:
            self.db.setDuration(value)
            self.showTimeExtents()

    def setNextInterval(self):
        self.db.setNextInterval()
        self.showTimeExtents()

    def setPrevInterval(self):
        self.db.setPrevInterval()
        self.showTimeExtents()

    ################################################################################
    # Save
    ################################################################################
    def saveFile(self):
        self.saveFileImpl(0)

    def saveFileAs(self):
        self.saveFileImpl(1)

    def saveFileImpl(self, saveAs):
        if not self.filename or saveAs:
            self.filename = QFileDialog.getSaveFileName(self, 'Save file...', '', 'Savfin Files (*.savfin)')
            self.filename = str(self.filename)
            if not self.filename:
                return

        self.writeFile()
        self.refreshTitle()

        self.dirty = False
        self.refreshTitle()

    def writeFile(self):
        if self.db.masterPassword:
            openSslArgs = [OPENSSL_PATH, 'enc', 
                    '-aes-256-cbc', '-a', '-salt', 
                    '-in', 'file.pickle', 
                    '-pass', 'pass:%s' % self.db.masterPassword]
            header = ENCRYPTED_ON_HEADER + '\n'
        else:
            openSslArgs = [OPENSSL_PATH, 'enc', 
                    '-base64', 
                    '-in', 'file.pickle']
            header = ENCRYPTED_OFF_HEADER + '\n'

        with TempDirObject():
            with open('file.pickle', 'wb') as pickledFile:
                # Use -1 for binary format. This probably makes a .savfin
                # file saved in windows load-able in linux.
                pickle.dump(self.db, pickledFile, -1)

            enc_pickle = subprocess.check_output(openSslArgs)

            with open(self.filename, 'w') as f:
                f.write(header)
                f.write(enc_pickle)

    ################################################################################
    # Load
    ################################################################################
    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file...', '', 'Savfin Files (*.savfin)')
        if not filename:
            return

        self.loadFile(filename)

    def loadFile(self, filename, password=''):
        self.filename = filename

        with open(self.filename) as f:
            firstLine = f.readline(50).strip()

        if firstLine == ENCRYPTED_ON_HEADER:
            self.loadNewFormat(True, password)
        elif firstLine == ENCRYPTED_OFF_HEADER:
            self.loadNewFormat(False)
        else:
            self.loadOldFormat()

        self.updateRecentFiles(filename)

    def loadNewFormat(self, isEncrypted, password=''):
        if isEncrypted:
            if password == '':
                password = getPassword()
            openSslArgs = [OPENSSL_PATH, 'enc', '-d',
                    '-aes-256-cbc', '-a', '-salt',
                    '-in', 'file.enc',
                    '-out', 'file.pickle',
                    '-pass', 'pass:%s' % password]
        else:
            openSslArgs = [OPENSSL_PATH, 'enc', '-d',
                    '-base64',
                    '-in', 'file.enc',
                    '-out', 'file.pickle']

        with TempDirObject():
            with open(self.filename) as f:
                # read and throw away the first line
                f.readline()

                with open('file.enc', 'w') as encFile:
                    # TODO: make this not read the entire contents into memory?
                    encFile.write(f.read())

            # time to decrypt
            try:
                subprocess.check_call(openSslArgs)
            except subprocess.CalledProcessError as err:
                msgBox = QMessageBox()
                msgBox.setText('Invalid password!')
                msgBox.setStandardButtons(QMessageBox.Abort | QMessageBox.Retry)
                msgBox.setDefaultButton(QMessageBox.Retry)

                ret = msgBox.exec_()
                if ret == QMessageBox.Retry:
                    self.loadFile(self.filename)
                    return
                else:
                    return

            # unpickle
            self.loadPickledFile('file.pickle')

    def loadPickledFile(self, filename):
        retry = False
        with open(filename, 'rb') as f:
            try:
                self.db = pickle.load(f)
            except:
                print "Error opening the pickled file in binary mode.  Re-trying after opening in text mode"
                retry = True

        if retry:
            with open(filename, 'r') as f:
                self.db = pickle.load(f)

        for t in self.db.transactions:
            t.desc = re.sub(r'\s+', ' ', t.desc)
        self.initDb()

    def loadOldFormat(self):
        self.loadPickledFile(self.filename)

    ################################################################################
    # Recent file management
    ################################################################################
    def openRecentFile(self):
        action = self.sender()
        filename = action.data()
        self.loadFile(str(filename.toString()))

    def setupRecentFiles(self):
        for a in self.recentFileActions:
            self.menu_File.removeAction(a)

        self.recentFileActions = []
        recentFiles = self.getRecentFiles()

        if not recentFiles:
            return

        for i, f in enumerate(recentFiles):
            fileAction = QAction('&%d %s' % (i+1, f), self)
            fileAction.setData(f)
            fileAction.triggered.connect(self.openRecentFile)

            self.menu_File.insertAction(self.actionQuit, fileAction)
            self.recentFileActions.append(fileAction)

        self.menu_File.insertSeparator(self.actionQuit)

    def updateRecentFiles(self, filename):
        recentFiles = self.getRecentFiles()

        if filename in recentFiles:
            recentFiles.remove(filename)

        recentFiles.insert(0, filename)

        settings = QSettings()

        recentFiles = QStringList(recentFiles)
        settings.setValue('recentFilesList', recentFiles)

        self.setupRecentFiles()

    def getRecentFiles(self):
        settings = QSettings()
        recentFiles = settings.value('recentFilesList').toStringList()
        recentFiles = [str(f) for f in recentFiles]
        recentFiles = [path.normcase(f) for f in recentFiles if f]

        recentFilesSet = set()
        recentFilesListUniq = []
        for f in recentFiles:
            if not (f in recentFilesSet):
                recentFilesListUniq.append(f)
                recentFilesSet.add(f)

        return recentFilesListUniq

    ################################################################################
    # Import statements
    ################################################################################
    def importFile(self, filename, account, pdfParser, qfxParser):
        print 'Importing from %s' % filename
        (basename, ext) = path.splitext(filename)
        ext = ext.lower()
        if ext == '.csv':
            csvImporter = CsvImporter(self.db, filename, account)
            csvImporter.exec_()
            newTrans = csvImporter.transactions
        elif (ext == '.pdf') and pdfParser:
            newTrans = pdfParser(filename)
        elif (ext == '.qfx') and qfxParser:
            newTrans = qfxParser(filename)
        else:
            msgBox = QMessageBox()
            msgBox.setText('Unknown file extension "%s". Only .pdf and .csv files are supported' % ext)
            msgBox.exec_()
            return

        for t in newTrans:
            t.accountFrom = account

        (numNew, numDups) = self.db.addTransactions(newTrans)
        return (numNew, numDups)

    def getOrCreateAccount(self, accountId):
        foundAccount = None
        for account in self.db.accounts:
            if account.accountId == accountId:
                foundAccount = account
                break

        if not foundAccount:
            d = AssociateWithAccountDialog(self.db, accountId)
            if not d.exec_():
                return None

            foundAccount = self.db.getAccountFromName(d.accountPath)
            foundAccount.accountId = accountId

        return foundAccount

    def addTransactions(self, importedInfo):
        numNew = 0
        numDups = 0

        for importedAccountInfo in importedInfo.importedAccountInfos:
            account = self.getOrCreateAccount(importedAccountInfo.accountId)
            if not account:
                continue

            for t in importedAccountInfo.transactions:
                t.accountFrom = account

            (numNew_, numDups_) = self.db.addTransactions(importedAccountInfo.transactions)
            numNew += numNew_
            numDups += numDups_

            if importedAccountInfo.beginBalance:
                account.addBalanceSnapshot(importedAccountInfo.beginBalance[0], importedAccountInfo.beginBalance[1])

            if importedAccountInfo.endBalance:
                account.addBalanceSnapshot(importedAccountInfo.endBalance[0], importedAccountInfo.endBalance[1])

        return (numNew, numDups)

    def importGenericFile(self, filename):
        (basename, ext) = path.splitext(filename)
        ext = ext.lower()

        if (ext == '.pdf'):
            importedInfo = getBankOfAmericaTransactionsPdf(filename)
            if importedInfo:
                print 'Adding BOFA transactions'
                return self.addTransactions(importedInfo)

            importedInfo = getChaseTransactionsPdf(filename)
            if importedInfo:
                print 'Adding Chase transactions'
                return self.addTransactions(importedInfo)

            importedInfo = getDcuTransactionsPdf(filename)
            if importedInfo:
                print 'Adding DCU transactions'
                return self.addTransactions(importedInfo)

            msgBox = QMessageBox()
            msgBox.setText("Failed to import from PDF file")
            msgBox.exec_()
            return

        elif (ext == '.ofx' or ext == '.qfx'):
            importedInfo = importOfxTransactionsFromFile(self.db, str(filename))
            return self.addTransactions(importedInfo)

        else:
            msgBox = QMessageBox()
            msgBox.setText('Unknown file extension "%s". Only .pdf, .ofx and .qfx files are supported' % ext)
            msgBox.exec_()
            return

    def importGenericStatement(self):
        patterns = ['*.pdf', '*.qfx', '*.ofx']

        filePattern = 'Statements (%s)' % (' '.join(patterns))
        files = QFileDialog.getOpenFileNames(self,
                'Choose a statement', '',
                filePattern)

        if not files:
            return

        numNew = 0
        numDups = 0

        for filename in files:
            print("Importing from %s" % str(filename))
            (new, dups) = self.importGenericFile(str(filename))
            numNew += new
            numDups += dups

        alertImportStatus((numNew, numDups))

    def importStatement(self):
        self.db.stopChangeNotifications()
        try:
            self.importGenericStatement()
        finally:
            self.db.startChangeNotifications()

if __name__ == '__main__':
    import sys
    from PyQt4.QtCore import pyqtRemoveInputHook
    pyqtRemoveInputHook()

    import pdb
    try:
        import win32api
        import win32con

        def handle(event):
            if event != win32con.CTRL_C_EVENT:
                return 0
            pdb.set_trace()
            return 1

        result = win32api.SetConsoleCtrlHandler(handle, 1)
        if result == 0:
            sys.exit('Could not SetConsoleCtrlHandler')

    except:
        import signal
        def signal_handler(signal, frame):
            pdb.set_trace()

        signal.signal(signal.SIGINT, signal_handler)

    QCoreApplication.setOrganizationName('SavadhanSoft')
    QCoreApplication.setOrganizationDomain('savadhansoft.com')
    QCoreApplication.setApplicationName('savfin')

    app = QApplication(sys.argv)
    main = MainWindow()

    main.show()

    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        filename = ''

    if len(sys.argv) >= 3:
        password = sys.argv[2]
    else:
        password = ''

    if filename:
        main.loadFile(filename, password)

    app.exec_()
