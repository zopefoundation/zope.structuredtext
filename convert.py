"""Utility to convert stx in regression dir to html
"""

import sys
import os.path
from zope.structuredtext import stng
from zope.structuredtext.document import Document
from zope.structuredtext.html import HTML

def readFile(dirname,fname):
    myfile = open(os.path.join(dirname, fname), "r")
    lines = myfile.readlines()
    myfile.close()
    return ''.join(lines)

def writeFile(dirname,fname, data):
    myfile = open(os.path.join(dirname, fname), "w")
    myfile.truncate()
    myfile.write(data)

if __name__ == '__main__':
    files = ['index.stx','Acquisition.stx','ExtensionClass.stx',
            'MultiMapping.stx','examples.stx','Links.stx','examples1.stx',
            'table.stx','InnerLinks.stx']
    dirname = sys.argv[1]
    for f in files:
        raw_text = readFile(dirname, f)
        doc = stng.structurize(raw_text)
        doc = Document()(doc)
        html = HTML()(doc)
        
        reg_fname = f.replace('.stx','.ref')
        reg_html  = writeFile(dirname , reg_fname, html)
