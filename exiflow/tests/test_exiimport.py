#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
Unit tests for exiimport.py
"""
__revision__ = "$Id$"


import shutil
import os
import sys
import tempfile
import time
import unittest

import NikonD70
sys.path.append(os.path.dirname(sys.path[0]))
import exiflow.configfile
import exiflow.exiimport


class TestImport(unittest.TestCase):
    """ Tests for exiimport.py """

    def setUp(self):
        """ Create a directory with an image. """
        self.__data_dir = os.path.join(os.path.dirname(__file__), "testdata")
        self.__sourcedir = tempfile.mkdtemp()
        self.__targetdir = tempfile.mkdtemp()
        self.__configdir = tempfile.mkdtemp()
        exiflow.configfile.global_config_dir = self.__configdir
        exiflow.configfile.local_config_dir = self.__configdir

    def tearDown(self):
        """ Clean up. """
        shutil.rmtree(self.__configdir)
        shutil.rmtree(self.__sourcedir)
        shutil.rmtree(self.__targetdir)

    def test_run(self):
        """ Test run(). """
        shutil.copyfile(os.path.join(self.__data_dir, "NikonD70.jpg"),
                        os.path.join(self.__sourcedir, "DSC0001.jpg"))
        shutil.copyfile(os.path.join(self.__data_dir, "NikonD70.jpg"),
                        os.path.join(self.__sourcedir, "DSC0002.jpg"))
        exiflow.exiimport.run(argv=["--mount", self.__sourcedir,
                                    "--target", self.__targetdir,
                                    "--verbose"])
        self.assertEqual(os.listdir(self.__sourcedir),
                         os.listdir(os.path.join(self.__targetdir,
                                             os.listdir(self.__targetdir)[0])))
        # Run twice and check if another directory have been created.
        exiflow.exiimport.run(argv=["--mount", self.__sourcedir,
                                    "--target", self.__targetdir])
        self.assertEqual(len(os.listdir(self.__targetdir)), 2)

    def test_run__syntax_error(self):
        """ Test run() with wrong syntax. """
        result = exiflow.exiimport.run(argv=["--target", self.__targetdir,
                                       "bla"])
        self.assertTrue(result)

    def test_run__no_files(self):
        """ Test run() with empty source dir. """
        result = exiflow.exiimport.run(argv=["--mount", self.__sourcedir,
                                             "--target", self.__targetdir])
        self.assertTrue(result)

    def test_run__callback(self):
        """ Test run() with a callback function. """
        mylist = []

        def callback(*dummy_args, **dummy_kwargs):
            """ Just set callback_called to True. """
            mylist.append(True)
            return True

        shutil.copyfile(os.path.join(self.__data_dir, "NikonD70.jpg"),
                        os.path.join(self.__sourcedir, "DSC0001.jpg"))
        exiflow.exiimport.run(argv=["--mount", self.__sourcedir,
                                    "--target", self.__targetdir,
                                    "--verbose"], callback=callback)
        self.assertEqual(mylist, [True])

