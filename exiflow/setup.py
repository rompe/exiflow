#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
Install the exiflow collection on your computer.
"""

import distutils.core

distutils.core.setup(name='exiflow',
                     version='0.1',
                     scripts=['exigui',
                              'exiassign',
                              'exigate',
                              'exiimport',
                              'exiperson',
                              'exirename'],
                     packages=['exiflow'],
                     package_data={'exiflow': ['*.glade']})

