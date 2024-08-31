from PyQt4 import uic
from glob import glob
import os
from os import path
import argparse

parser = argparse.ArgumentParser(description="Convert .ui files to .py")
parser.add_argument('-c', '--clean', 
        action="store_true",
        help="clean all auto generated files")
parser.add_argument('-f', '--force', 
        action="store_true",
        help="force generation of .py files from .ui (ignore timestamps)")

def doit(force):
    files = glob('*.ui')
    for uifileName in files:
        (name, ext) = path.splitext(uifileName)
        pyfileName = name + '.py'
        if ((not path.isfile(pyfileName)) or force or
                (path.getmtime(pyfileName) < path.getmtime(uifileName))):
            print 'Converting %s into %s' % (uifileName, pyfileName)
            with open(pyfileName, 'w') as pyfile:
                uic.compileUi(uifileName, pyfile)

def clean():
    def removeFile(fname):
        if path.exists(fname):
            os.remove(fname)

    files = glob('*.ui')
    for uifileName in files:
        (name, ext) = path.splitext(uifileName)
        pyfileName = name + '.py'
        pycfileName = name + '.pyc'
        removeFile(pyfileName)
        removeFile(pycfileName)

args = parser.parse_args()
os.chdir('ui')
if args.clean:
    clean()
else:
    doit(args.force)
