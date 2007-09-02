##############################################################################
#
# Copyright (c) 2004-2007 Zope Corporation and Contributors.
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
"""Setup for zope.structuredtext package

$Id$
"""

import os

from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('src', 'zope', 'structuredtext', 'STNG.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

setup(
    name='zope.structuredtext',
    version = '3.4.0',
    url='http://pypi.python.org/pypi/zope.structuredtext',
    author='Zope Corporation and Contributors',
    author_email='zope3-dev@zope.org',
    license='ZPL 2.1',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        ],
    description='StructuredText parser',
    long_description=long_description,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['zope',],
    include_package_data=True,
    install_requires=['setuptools'],
    zip_safe=False,
    )
