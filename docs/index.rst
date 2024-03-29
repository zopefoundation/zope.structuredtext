==========================================
 :mod:`zope.structuredtext` Documentation
==========================================

.. currentmodule:: zope.restructuredtext

Using Structured Text
=====================

The goal of StructuredText is to make it possible to express
structured text using a relatively simple plain text format. Simple
structures, like bullets or headings are indicated through
conventions that are natural, for some definition of
"natural". Hierarchical structures are indicated through
indentation. The use of indentation to express hierarchical
structure is inspired by the Python programming language.

Use of StructuredText consists of one to three logical steps. In the
first step, a text string is converted to a network of objects using
the :func:`~.structurize` facility, as in the following example:

.. code-block:: python

  raw = open("mydocument.txt").read()
  from zope.structuredtext.stng import structurize
  st = structurize(raw)

The output of :func:`~.structurize` is simply a :class:`~.StructuredTextDocument`
object containing :class:`~.StructuredTextParagraph` objects arranged in a
hierarchy. Paragraphs are delimited by strings of two or more
whitespace characters beginning and ending with newline
characters. Hierarchy is indicated by indentation. The indentation
of a paragraph is the minimum number of leading spaces in a line
containing non-white-space characters after converting tab
characters to spaces (assuming a tab stop every eight characters).

:class:`~.StructuredTextNode` objects support the read-only subset of the
Document Object Model (DOM) API. It should be possible to process
:class:`~.StructuredTextNode` hierarchies using XML tools such as XSLT.

The second step in using StructuredText is to apply additional
structuring rules based on text content. A variety of different text
rules can be used.  Typically, these are used to implement a
structured text language for producing documents, but any sort of
structured text language could be implemented in the second
step. For example, it is possible to use StructuredText to implement
structured text formats for representing structured data. The second
step, which could consist of multiple processing steps, is
performed by processing, or "coloring", the hierarchy of generic
StructuredTextParagraph objects into a network of more specialized
objects. Typically, the objects produced should also implement the DOM
API to allow processing with XML tools.

A document processor is provided to convert a StructuredTextDocument
object containing only StructuredTextParagraph objects into a
StructuredTextDocument object containing a richer collection of
objects such as bullets, headings, emphasis, and so on using hints
in the text. Hints are selected based on conventions of the sort
typically seen in electronic mail or news-group postings. It should
be noted, however, that these conventions are somewhat culturally
dependent, fortunately, the document processor is easily customized
to implement alternative rules. Here's an example of using the DOC
processor to convert the output of the previous example:

.. code-block:: python

  from zope.structuredtext.document import Document
  doc = Document()(st)

The final step is to process the colored networks produced from the
second step to produce additional outputs. The final step could be
performed by Python programs, or by XML tools. A Python outputter is
provided for the document processor output that produces Hypertext Markup
Language (HTML) text:

.. code-block:: python

  from zope.structuredtext.html import HTML
  html = HTML()(doc)


Customizing the document processor
==================================

The document processor is driven by two tables. The first table,
named ``paragraph_types``, is a sequence of callable objects or method
names for coloring paragraphs. If a table entry is a string, then it
is the name of a method of the document processor to be used. For
each input paragraph, the objects in the table are called until one
returns a value (not 'None'). The value returned replaces the
original input paragraph in the output. If none of the objects in
the paragraph types table return a value, then a copy of the
original paragraph is used.  The new object returned by calling a
paragraph type should implement the ``ReadOnlyDOM``,
``StructuredTextColorizable``, and ``StructuredTextSubparagraphContainer``
interfaces. See the :mod:`zope.structuredtext.document` source file for
examples.

A paragraph type may return a list or tuple of replacement
paragraphs, this allowing a paragraph to be split into multiple
paragraphs.

The second table, ``text_types``, is a sequence of callable objects or
method names for coloring text. The callable objects in this table
are used in sequence to transform the input text into new text or
objects.  The callable objects are passed a string and return
nothing (``None``) or a three-element tuple consisting of:

- a replacement object,

- a starting position, and

- an ending position

The text from the starting position is (logically) replaced with the
replacement object. The replacement object is typically an object
that implements that implements the ``ReadOnlyDOM`` and
``StructuredTextColorizable`` interfaces. The replacement object can
also be a string or a list of strings or objects. Replacement is
done from beginning to end and text after the replacement ending
position will be passed to the character type objects for processing.


Contents:

.. toctree::
   :maxdepth: 2

   api
   changelog

====================
 Indices and tables
====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
