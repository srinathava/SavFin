from distutils.core import setup
import py2exe

setup(windows=[
        {"script" : "MainWindow.py", "dest_base" : "savfin"},
        {"script": "FileOpener.py", "dest_base": "savfin-openofx"}
        ], 
        options={
            "py2exe" : {
                "includes" : ["sip"],
                "dll_excludes" : ["MSVCP90.dll"]
            },
        })

