#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
setup(name='Exiflow',
      version='0.4.5',
      package_dir={'foobar': ''},
      packages=['exiflow'],
      scripts=["exiassign", "exiconvert", "exigate", "exigui",
               "exiimport", "exiperson", "exirename"],
      data_files=["exiflow/exigui.glade"]
      )
