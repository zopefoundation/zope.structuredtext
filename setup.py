##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zope.i18nmessageid package

$Id$
"""

import os

from setuptools import setup, find_packages

setup(name='zope.structuredtext',
      version = '3.4.0b1',
      url='http://svn.zope.org/zope.structuredtext',
      license='ZPL 2.1',
      description='XXX',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      long_description='',
      
      packages=find_packages('src'),
      package_dir = {'': 'src'},

      namespace_packages=['zope',],
      include_package_data = True,

      zip_safe = False,
      )
