# -*- coding: utf-8 -*-

from setuptools import setup

NAME = 'pyxenter'

VERSION = '1.0.0'

DESCRIPTION = 'Xen Server control script.'

LONG_DESCRIPTION = """
Xen Server control script.

Requirements
------------
* Python 2.7 or Python 2.x (not support 3.x)

Features
--------
* nonthing

Setup
-----
::

    $ easy_install pyxenter
"""

PACKAGES = ['xen', 'esxi']

AUTHOR = 'Kazuki Hasegawa'

MAIL_ADDRESS = "hasegawa_0204@hotmail.co.jp"

ENTRY_POINTS = """
[console_scripts]
xenxen = xen.xen:main
xenes  = esxi.esxi:main
"""

REQUIRES = [
    'XenAPI',
    'pysphere',
    ]

setup(name         = NAME,
      version      = VERSION,
      packages     = PACKAGES,
      author       = AUTHOR,
      author_email = MAIL_ADDRESS,
      entry_points = ENTRY_POINTS,
      install_requires = REQUIRES,
      )