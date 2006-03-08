#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
Install the exiflow collection on your computer.
"""

import distutils.core

distutils.core.setup(name='exiflow',
                     version='0.2.0',
                     scripts=['exigui',
                              'exiassign',
                              'exigate',
                              'exiimport',
                              'exiperson',
                              'exirename'],
                     packages=['exiflow'],
                     package_data={'exiflow': ['*.glade']},
                     data_files=[('share/doc/exiflow', ['README', 'INSTALL', 'COPYING'])],
                     author='Ulf Rompe, Sebastian Berthold',
                     author_email='exiflow-devel@lists.sourceforge.net',
                     license='GNU General Public License (GPL)',
                     url='http://sourceforge.net/projects/exiflow/',
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
                     classifiers=['Development Status :: 3 - Alpha',
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

