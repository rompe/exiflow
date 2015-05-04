#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Install the exiflow collection on your computer.
"""
__revision__ = "$Id: $"

#from distutils.core import setup
from setuptools import setup

setup(name='Exiflow',
      install_requires=["glade2"],
      version='0.4.5.16',
      packages=['exiflow'],
      scripts=["exiassign", "exiconvert", "exigate", "exigui",
               "exiimport", "exiperson", "exirename"],
      package_data={"exiflow": ["exigui.glade"]},
      data_files=[('share/doc/exiflow', ['README', 'INSTALL', 'COPYING'])],
#      entry_points={'console_scripts': ["exiassign = exiflow.exiassign:run",
#                                        "exiconvert = exiflow.exiconvert:run",
#                                        "exigate = exiflow.exigate:run",
#                                        "exiimport = exiflow.exiimport:run",
#                                        "exiperson = exiflow.exiperson:run",
#                                        "exirename = exiflow.exirename:run"],
#                    'gui_scripts': ["exigui = exiflow.exigui:run"]},
      author='Ulf Rompe, Sebastian Berthold',
      author_email='exiflow-devel@lists.sourceforge.net',
      license='GNU General Public License (GPL)',
      platforms="any",
      url='http://exiflow.org/',
      description='A set of tools including a little GUI to '
                  'provide a complete digital photo workflow '
                  'for Unixes, using EXIF headers as the '
                  'central information repository.',
      long_description='A set of tools including a little GUI '
                       'to provide a complete digital photo '
                       'workflow for Unixes. EXIF headers are '
                       'used as the central information '
                       'repository, so users may change their '
                       'software at any time without loosing '
                       'any data. The tools may be used '
                       'individually or combined.',
      download_url='http://sourceforge.net/project/showfiles.php?group_id=151136',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Environment :: X11 Applications :: GTK',
                   'Intended Audience :: End Users/Desktop',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: POSIX',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: Unix',
                   'Programming Language :: Python',
                   'Topic :: Multimedia :: Graphics',
                   'Topic :: Multimedia :: Graphics :: Graphics Conversion',
                   'Topic :: System :: Archiving',
                   'Topic :: Utilities'])
