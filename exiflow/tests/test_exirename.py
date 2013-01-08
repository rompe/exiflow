#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
Unit tests for exirename.py
"""
__revision__ = "$Id$"


import shutil
import os
import sys
import tempfile
import unittest

import NikonD70
sys.path.append(os.path.dirname(sys.path[0]))
import exiflow.configfile
import exiflow.exirename


class TestExirename(unittest.TestCase):
    """ Tests for exirename.py """

    def setUp(self):
        """ Create a directory with an image. """
        self.__data_dir = os.path.join(os.path.dirname(__file__), "testdata")
        self.__tempdir = tempfile.mkdtemp()
        self.__configdir = tempfile.mkdtemp()
        exiflow.configfile.global_config_dir = self.__configdir
        exiflow.configfile.local_config_dir = self.__configdir

    def tearDown(self):
        """ Clean up. """
        shutil.rmtree(self.__tempdir)
        shutil.rmtree(self.__configdir)

    def test_exirename__space_in_filename(self):
        """ Test exirename() with file containing a space. """
        shutil.copyfile(os.path.join(self.__data_dir, "NikonD70.jpg"),
                        os.path.join(self.__tempdir, "Nikon D70.jpg"))
        exiflow.exirename.run(argv=["--cam_id=n00", "--artist_initials=xy", self.__tempdir])
        self.assertEqual(os.listdir(self.__tempdir), ["20040330-n000070-xy000.jpg"])
