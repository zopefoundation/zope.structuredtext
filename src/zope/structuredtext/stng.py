##############################################################################
#
# Copyright (c) 2001 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
""" Core document model.
"""

import re

from . import stdom


def indention(str, front=re.compile(r"^\s+").match):
    """Find the number of leading spaces. If none, return 0.
    """
    result = front(str)
    if result is not None:
        start, end = result.span()
        return end - start
    else:
        return 0     # no leading spaces


def insert(struct, top, level):
    """Find what will be the parant paragraph of a sentence and return
    that paragraph's sub-paragraphs. The new paragraph will be
    appended to those sub-paragraphs
    """
    if top - 1 not in range(len(struct)):
        if struct:
            return struct[len(struct) - 1].getSubparagraphs()
        return struct
    run = struct[top - 1]
    i = 0
    while i + 1 < level:
        run = run.getSubparagraphs()[len(run.getSubparagraphs()) - 1]
        i = i + 1
    return run.getSubparagraphs()


def display(struct):
    """Runs through the structure and prints out the paragraphs. If
    the insertion works correctly, display's results should mimic the
    orignal paragraphs.
    """
    if struct.getColorizableTexts():
        print('\n'.join(struct.getColorizableTexts()))
    if struct.getSubparagraphs():
        for x in struct.getSubparagraphs():
            display(x)


def display2(struct):
    """Runs through the structure and prints out the paragraphs. If
    the insertion works correctly, display's results should mimic the
    orignal paragraphs.
    """
    if struct.getNodeValue():
        print(struct.getNodeValue(), "\n")
    if struct.getSubparagraphs():
        for x in struct.getSubparagraphs():
            display(x)


def findlevel(levels, indent):
    """Remove all level information of levels with a greater level of
    indentation. Then return which level should insert this paragraph
    """
    keys = list(levels.keys())
    for key in keys:
        if levels[key] > indent:
            del levels[key]
    keys = levels.keys()
    if not keys:
        return 0
    else:
        for key in keys:
            if levels[key] == indent:
                return key
    highest = 0
    for key in keys:
        if key > highest:
            highest = key
    return highest - 1


def flatten(obj, append):
    if obj.getNodeType() == stdom.TEXT_NODE:
        append(obj.getNodeValue())
    else:
        for child in obj.getChildNodes():
            flatten(child, append)


para_delim = r'(\n\s*\n|\r\n\s*\r\n)'  # UNIX or DOS line endings, respectively


def structurize(paragraphs, delimiter=re.compile(para_delim)):
    """Accepts paragraphs, which is a list of lines to be
    parsed. structurize creates a structure which mimics the
    structure of the paragraphs.  Structure =>
    [paragraph,[sub-paragraphs]]
    """

    currentlevel = 0
    currentindent = 0
    levels = {0: 0}
    level = 0        # which header are we under
    struct = []       # the structure to be returned
    run = struct

    paragraphs = paragraphs.expandtabs()
    paragraphs = '{}{}{}'.format('\n\n', paragraphs, '\n\n')
    paragraphs = delimiter.split(paragraphs)
    paragraphs = [x for x in paragraphs if x.strip()]

    if not paragraphs:
        return StructuredTextDocument()

    ind = []     # structure based on indention levels
    for paragraph in paragraphs:
        ind.append([indention(paragraph), paragraph])

    currentindent = indention(paragraphs[0])
    levels[0] = currentindent

    for indent, paragraph in ind:
        if indent == 0:
            level = level + 1
            currentlevel = 0
            currentindent = 0
            levels = {0: 0}
            struct.append(StructuredTextParagraph(paragraph,
                                                  indent=indent,
                                                  level=currentlevel))
        elif indent > currentindent:
            currentlevel = currentlevel + 1
            currentindent = indent
            levels[currentlevel] = indent
            run = insert(struct, level, currentlevel)
            run.append(StructuredTextParagraph(paragraph,
                                               indent=indent,
                                               level=currentlevel))
        elif indent < currentindent:
            result = findlevel(levels, indent)
            if result > 0:
                currentlevel = result
            currentindent = indent
            if not level:  # pragma: no cover Can we ever even get here?
                struct.append(StructuredTextParagraph(paragraph,
                                                      indent=indent,
                                                      level=currentlevel))
            else:
                run = insert(struct, level, currentlevel)
                run.append(StructuredTextParagraph(paragraph,
                                                   indent=indent,
                                                   level=currentlevel))
        else:
            if insert(struct, level, currentlevel):
                run = insert(struct, level, currentlevel)
            else:
                run = struct
                currentindent = indent
            run.append(StructuredTextParagraph(paragraph,
                                               indent=indent,
                                               level=currentlevel))

    return StructuredTextDocument(struct)


class StructuredTextParagraph(stdom.Element):

    indent = 0

    def __init__(self, src, subs=None, **kw):
        if subs is None:
            subs = []
        self._src = src
        self._subs = list(subs)

        self._attributes = kw.keys()
        for k, v in kw.items():
            setattr(self, k, v)

    def getChildren(self):
        src = self._src
        if not isinstance(src, list):
            src = [src]
        return src + self._subs

    def getSubparagraphs(self):
        return self._subs

    def setSubparagraphs(self, subs):
        self._subs = subs

    def getColorizableTexts(self):
        return (self._src,)

    def setColorizableTexts(self, src):
        self._src = src[0]

    def __repr__(self):
        r = []
        a = r.append
        a((' ' * (self.indent or 0))
          + ('%s(' % self.__class__.__name__)
          + str(self._src) + ', [')
        for p in self._subs:
            a(repr(p))
        a((' ' * (self.indent or 0)) + '])')
        return '\n'.join(r)


class StructuredTextDocument(StructuredTextParagraph):
    """A StructuredTextDocument holds StructuredTextParagraphs
    as its subparagraphs.
    """
    _attributes = ()

    def __init__(self, subs=None, **kw):
        super().__init__('', subs, **kw)

    def getChildren(self):
        return self._subs

    def getColorizableTexts(self):
        return ()

    def setColorizableTexts(self, src):
        pass

    def __repr__(self):
        r = []
        a = r.append
        a('%s([' % self.__class__.__name__)
        for p in self._subs:
            a(repr(p) + ',')
        a('])')
        return '\n'.join(r)


class StructuredTextExample(StructuredTextParagraph):
    """Represents a section of document with literal text, as for examples"""

    def __init__(self, subs, **kw):
        t = []
        for s in subs:
            flatten(s, t.append)
        super().__init__('\n\n'.join(t), (), **kw)

    def getColorizableTexts(self):
        return ()

    def setColorizableTexts(self, src):
        pass  # never color examples


class StructuredTextBullet(StructuredTextParagraph):
    """Represents a section of a document with a title and a body
    """


class StructuredTextNumbered(StructuredTextParagraph):
    """Represents a section of a document with a title and a body
    """


class StructuredTextDescriptionTitle(StructuredTextParagraph):
    """Represents a section of a document with a title and a body
    """


class StructuredTextDescriptionBody(StructuredTextParagraph):
    """Represents a section of a document with a title and a body
    """


class StructuredTextDescription(StructuredTextParagraph):
    """Represents a section of a document with a title and a body
    """

    def __init__(self, title, src, subs, **kw):
        super().__init__(src, subs, **kw)
        self._title = title

    def getColorizableTexts(self):
        return self._title, self._src

    def setColorizableTexts(self, src):
        self._title, self._src = src

    def getChildren(self):
        return (StructuredTextDescriptionTitle(self._title),
                StructuredTextDescriptionBody(self._src, self._subs))


class StructuredTextSectionTitle(StructuredTextParagraph):
    """Represents a section of a document with a title and a body"""


class StructuredTextSection(StructuredTextParagraph):
    """Represents a section of a document with a title and a body"""

    def __init__(self, src, subs=None, **kw):
        super().__init__(
            StructuredTextSectionTitle(src), subs, **kw)

    def getColorizableTexts(self):
        return self._src.getColorizableTexts()

    def setColorizableTexts(self, src):
        self._src.setColorizableTexts(src)

# a StructuredTextTable holds StructuredTextRows


class StructuredTextTable(StructuredTextParagraph):
    """
    rows is a list of lists containing tuples, which
    represent the columns/cells in each rows.
    EX
    rows = [[('row 1:column1',1)],[('row2:column1',1)]]
    """

    def __init__(self, rows, src, subs, **kw):
        super().__init__(subs, **kw)
        self._rows = []
        for row in rows:
            if row:
                self._rows.append(StructuredTextRow(row, kw))

    def getRows(self):
        return [self._rows]

    _getRows = getRows

    def getColumns(self):
        result = []
        for row in self._rows:
            result.append(row.getColumns())
        return result

    _getColumns = getColumns

    def setColumns(self, columns):
        for index, row in enumerate(self._rows):
            row.setColumns(columns[index])

    _setColumns = setColumns

    def getColorizableTexts(self):
        """
        return a tuple where each item is a column/cell's
        contents. The tuple, result, will be of this format.
        ("r1 col1", "r1=col2", "r2 col1", "r2 col2")
        """

        result = []
        for row in self._rows:
            for column in row.getColumns()[0]:
                result.append(column.getColorizableTexts()[0])
        return result

    def setColorizableTexts(self, texts):
        """
        texts is going to a tuple where each item is the
        result of being mapped to the colortext function.
        Need to insert the results appropriately into the
        individual columns/cells
        """
        for row_index in range(len(self._rows)):
            for column_index in range(len(self._rows[row_index]._columns)):
                self._rows[row_index
                           ]._columns[column_index
                                      ].setColorizableTexts((texts[0],))
                texts = texts[1:]

    _getColorizableTexts = getColorizableTexts
    _setColorizableTexts = setColorizableTexts

# StructuredTextRow holds StructuredTextColumns


class StructuredTextRow(StructuredTextParagraph):

    def __init__(self, row, kw):
        """
        row is a list of tuples, where each tuple is
        the raw text for a cell/column and the span
        of that cell/column.
        EX
        [('this is column one',1), ('this is column two',1)]
        """
        super().__init__([], **kw)

        self._columns = []
        for column in row:
            self._columns.append(StructuredTextColumn(column[0],
                                                      column[1],
                                                      column[2],
                                                      column[3],
                                                      column[4],
                                                      kw))

    def getColumns(self):
        return [self._columns]

    _getColumns = getColumns

    def setColumns(self, columns):
        self._columns = columns

    _setColumns = setColumns


# this holds the text of a table cell
class StructuredTextColumn(StructuredTextParagraph):
    """
    StructuredTextColumn is a cell/column in a table.
    A cell can hold multiple paragraphs. The cell
    is either classified as a StructuredTextTableHeader
    or StructuredTextTableData.
    """

    def __init__(self, text, span, align, valign, typ, kw):
        super().__init__(text, [], **kw)
        self._span = span
        self._align = align
        self._valign = valign
        self._type = typ

    def getSpan(self):
        return self._span

    _getSpan = getSpan

    def getAlign(self):
        return self._align

    _getAlign = getAlign

    def getValign(self):
        return self._valign

    _getValign = getValign

    def getType(self):
        return self._type

    _getType = getType


class StructuredTextTableHeader(StructuredTextParagraph):
    pass


class StructuredTextTableData(StructuredTextParagraph):
    pass


class StructuredTextMarkup(stdom.Element):

    def __init__(self, value, **kw):
        self._value = value
        self._attributes = kw.keys()
        for key, value in kw.items():
            setattr(self, key, value)

    def getChildren(self):
        v = self._value
        if not isinstance(v, list):
            v = [v]
        return v

    def getColorizableTexts(self):
        return self._value,

    def setColorizableTexts(self, v):
        self._value = v[0]

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._value)})'


class StructuredTextLiteral(StructuredTextMarkup):
    def getColorizableTexts(self):
        return ()

    def setColorizableTexts(self, v):
        pass


class StructuredTextEmphasis(StructuredTextMarkup):
    pass


class StructuredTextStrong(StructuredTextMarkup):
    pass


class StructuredTextInnerLink(StructuredTextMarkup):
    pass


class StructuredTextNamedLink(StructuredTextMarkup):
    pass


class StructuredTextUnderline(StructuredTextMarkup):
    pass


class StructuredTextSGML(StructuredTextMarkup):
    pass


class StructuredTextLink(StructuredTextMarkup):
    pass


class StructuredTextXref(StructuredTextMarkup):
    pass


class StructuredTextImage(StructuredTextMarkup):
    """A simple embedded image
    """
