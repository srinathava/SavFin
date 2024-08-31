import cStringIO
import subprocess
import re

PAT_MULT_SPACE = re.compile(r'\s+')
PAT_EMPTY = re.compile(r'^\s*$')

class PdfParser:
    def __init__(self, fileName):
        output = subprocess.Popen([r'pdftotext', '-layout', fileName, '-'], stdout=subprocess.PIPE).communicate()[0]
        self.file = cStringIO.StringIO(output)
        self.line = ''

    def nextLine(self):
        self.line = self.file.readline()
        if not self.line:
            raise EOFError('End of file encountered')

    def skipToLineMatching(self, pat):
        while 1:
            self.nextLine()
            m = pat.search(self.line)
            if m:
                return m

    def skipToLineContaining(self, str):
        while 1:
            self.nextLine()
            if str in self.line:
                break

    def removeSpaces(self, line):
        return PAT_MULT_SPACE.sub(' ', line.strip())

    def isEmpty(self):
        return PAT_EMPTY.match(self.line)


    def parseAmount(self, txt):
        txt = txt.replace(',', '')
        return float(txt)

