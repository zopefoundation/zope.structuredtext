"""Utility to convert stx to html
"""

import sys
from zope.structuredtext import stng
from zope.structuredtext.document import Document
from zope.structuredtext.html import HTML

def convert(raw_text):
    doc = stng.structurize(raw_text)
    doc = Document()(doc)
    return HTML()(doc)

if __name__ == '__main__':
    fname = sys.argv[1]
    print convert(open(fname).read())
