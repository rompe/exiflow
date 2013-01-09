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
import time
import unittest

import NikonD70
sys.path.append(os.path.dirname(sys.path[0]))
import exiflow.configfile
import exiflow.exirename
import exiflow.filelist


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

    def test_run__space_in_filename(self):
        """ Test run() with file containing a space and "--with_time". """
        shutil.copyfile(os.path.join(self.__data_dir, "NikonD70.jpg"),
                        os.path.join(self.__tempdir, "Nikon D70.jpg"))
        exiflow.exirename.run(argv=["--cam_id=n00", "--artist_initials=xy",
                              "--with_time", "--verbose", self.__tempdir])
        self.assertEqual(os.listdir(self.__tempdir),
                         ["20040330-104346-n000070-xy000.jpg"])

    def test_run__low_quality_jpg(self):
        """ Test run() with a low quality JPG preview. """
        shutil.copyfile(os.path.join(self.__data_dir, "python.jpg"),
                        os.path.join(self.__tempdir, "DSC1234.jpg"))
        shutil.copyfile(os.path.join(self.__data_dir, "python.jpg"),
                        os.path.join(self.__tempdir, "DSC1234.nef"))
        exiflow.exirename.run(argv=["--cam_id=n00", "--artist_initials=xy",
                              self.__tempdir])
        self.assertTrue(time.strftime("%Y%m%d") + "-n001234-xy00l.jpg" in
                        os.listdir(self.__tempdir))

    def test_run__no_number_in_filename(self):
        """ Test run() with a filename not containing a number. """
        shutil.copyfile(os.path.join(self.__data_dir, "python.jpg"),
                        os.path.join(self.__tempdir, "python.jpg"))
        exiflow.exirename.run(argv=["--cam_id=n00", "--artist_initials=xy",
                              self.__tempdir])
        # Nothing should have changed.
        self.assertEqual(os.listdir(self.__tempdir), ["python.jpg"])

    def test_run__no_camid_no_artistinitials(self):
        """ Test run() with undefined cam_id and artist_initials. """
        shutil.copyfile(os.path.join(self.__data_dir, "python.jpg"),
                        os.path.join(self.__tempdir, "DSC1234.jpg"))
        exiflow.exirename.run(argv=[self.__tempdir])
        # Nothing should have changed.
        self.assertEqual(os.listdir(self.__tempdir), ["DSC1234.jpg"])

    def test_run__already_in_exiflow_format(self):
        """ Test run() with a filename already in our naming scheme. """
        shutil.copyfile(os.path.join(self.__data_dir, "NikonD70.jpg"),
                        os.path.join(self.__tempdir,
                                     "20121212-n000001-ad000.jpg"))
        exiflow.exirename.run(argv=["--with_time", self.__tempdir])
        self.assertEqual(os.listdir(self.__tempdir),
                         ["20121212-104346-n000001-ad000.jpg"])
        
    def test_run__callback(self):
        """ Test run() with a callback function. """
        mylist = []

        def callback(*dummy_args):
            """ Just set callback_called to True. """
            mylist.append(True)
            return True

        shutil.copyfile(os.path.join(self.__data_dir, "python.jpg"),
                        os.path.join(self.__tempdir, "python.jpg"))
        exiflow.exirename.run(argv=["--cam_id=n00", "--artist_initials=xy",
                              self.__tempdir], callback=callback)
        self.assertEqual(mylist, [True])

    def test_rename_file__exceptions(self):
        """ Test exceptions of rename_file(). """
        my_filelist = exiflow.filelist.Filelist([])
        jpg_file = os.path.join(self.__tempdir, "20121212-n000001-ad000.jpg")
        shutil.copyfile(os.path.join(self.__data_dir, "NikonD70.jpg"), jpg_file)
        # File name doesn't change.
        self.assertRaises(IOError, exiflow.exirename.rename_file, jpg_file,
                          my_filelist, with_time=False)
        # Target already exists.
        open(os.path.join(self.__tempdir, "20121212-104346-n000001-ad000.jpg"),
             'w').write(":-)")
        self.assertRaises(IOError, exiflow.exirename.rename_file, jpg_file,
                          my_filelist, with_time=True)
