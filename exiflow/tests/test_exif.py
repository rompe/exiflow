#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
Unit tests for exif.py
"""
__revision__ = "$Id$"


import shutil
import os
import sys
import tempfile
import unittest

import NikonD70
sys.path.append(os.path.dirname(sys.path[0]))
import exiflow.exif


class TestExif(unittest.TestCase):
    """ Tests for exif.py """

    def setUp(self):
        """ Create a directory with an image. """
        data_dir = os.path.join(os.path.dirname(__file__), "testdata")
        self.__fields = {"Keywords": u"foo, bar, thingamabob",
                         "Description": u"Hello world!"}
        self.__tempdir = tempfile.mkdtemp()
        self.__virginjpeg = os.path.join(self.__tempdir, "python.jpg")
        shutil.copy(os.path.join(data_dir, "python.jpg"), self.__tempdir)
        self.__d70jpeg = os.path.join(self.__tempdir, "NikonD70.jpg")
        shutil.copy(os.path.join(data_dir, "NikonD70.jpg"), self.__tempdir)
        self.__d70jpeg_imgdesc_latin1 = os.path.join(self.__tempdir,
            "NikonD70_ImageDescription_2rows_latin1.jpg")
        shutil.copy(os.path.join(data_dir,
            "NikonD70_ImageDescription_2rows_latin1.jpg"), self.__tempdir)
        self.__d70jpeg_imgdesc_utf8 = os.path.join(self.__tempdir,
            "NikonD70_ImageDescription_2rows_utf8.jpg")
        shutil.copy(os.path.join(data_dir,
            "NikonD70_ImageDescription_2rows_utf8.jpg"), self.__tempdir)
        self.__emptyfile = os.path.join(self.__tempdir, "emptyfile.jpg")
        file(self.__emptyfile, 'w')
        self.__nosuchfile = os.path.join(self.__tempdir, "nosuchfile.jpg")

    def tearDown(self):
        """ Clean up. """
        shutil.rmtree(self.__tempdir)

    def test_read_exif_without_image(self):
        """ Tests for read_exif() with invalid filename """
        exif = exiflow.exif.Exif(self.__nosuchfile)
        self.failUnlessRaises(IOError, exif.read_exif)

    def test_read_exif_with_corrupt_image(self):
        """ Tests for read_exif() with invalid image content """
        exif = exiflow.exif.Exif(self.__emptyfile)
        self.failUnlessRaises(IOError, exif.read_exif)

    def test_read_exif(self):
        """ Tests for read_exif() with valid image """
        exif = exiflow.exif.Exif(self.__d70jpeg)
        self.failUnless(isinstance(exif, exiflow.exif.Exif))
        exif.read_exif()
        for field in NikonD70.fields:
            self.failUnless(field in exif.fields, field + " not in fields")
            self.failUnlessEqual(exif.fields[field], NikonD70.fields[field])

    def test_read_exif_imagedescription(self):
        """ Tests for read_exif() with valid image """
        exif = exiflow.exif.Exif(self.__d70jpeg_imgdesc_utf8)
        self.failUnless(isinstance(exif, exiflow.exif.Exif))
        exif.read_exif()
        self.failUnlessEqual(exif.fields["ImageDescription"],
                             u"ImageDescription first row äöüß\n" +
                             u"ImageDescription second row ÄÖÜß\n")

    def test_read_exif_imagedescription_decode(self):
        """ Tests for read_exif() with valid image """
        exif = exiflow.exif.Exif(self.__d70jpeg_imgdesc_latin1)
        self.failUnless(isinstance(exif, exiflow.exif.Exif))
        exif.read_exif()
        self.failUnlessEqual(exif.fields["ImageDescription"],
                             u"ImageDescription first row äöüß\n" +
                             u"ImageDescription second row ÄÖÜß\n")

    def test_write_exif_without_image(self):
        """ Test for write_exif() with invalid filename """
        exif = exiflow.exif.Exif(self.__nosuchfile)
        exif.fields = self.__fields
        self.failUnlessRaises(IOError, exif.write_exif)

    def test_write_exif_with_corrupt_image(self):
        """ Test for write_exif() with invalid image content """
        exif = exiflow.exif.Exif(self.__emptyfile)
        exif.fields = self.__fields
        self.failUnlessRaises(IOError, exif.write_exif)

    def test_write_exif(self):
        """ Test for write_exif() with valid image """
        exif = exiflow.exif.Exif(self.__d70jpeg)
        exif.fields = self.__fields.copy()
        self.failUnlessEqual(exif.write_exif(), 0)
        exif.read_exif()
        for field in self.__fields:
            self.failUnlessEqual(exif.fields[field], self.__fields[field])

    def test_update_exif_without_image(self):
        """ Test for update_exif() with invalid filename """
        exif = exiflow.exif.Exif(self.__nosuchfile)
        self.failUnlessRaises(IOError, exif.update_exif, self.__d70jpeg)
        exif = exiflow.exif.Exif(self.__d70jpeg)
        self.failUnlessRaises(IOError, exif.update_exif, self.__nosuchfile)

    def test_update_exif_with_corrupt_image(self):
        """ Test for update_exif() with invalid image content """
        exif = exiflow.exif.Exif(self.__emptyfile)
        self.failUnlessRaises(IOError, exif.update_exif, self.__d70jpeg)
        exif = exiflow.exif.Exif(self.__d70jpeg)
        self.failUnlessRaises(IOError, exif.update_exif, self.__emptyfile)

    def test_update_exif(self):
        """ Test for update_exif() with valid image """
        exif = exiflow.exif.Exif(self.__virginjpeg)
        self.failUnlessEqual(exif.update_exif(self.__d70jpeg), 0)
        exif.read_exif()
        for field in NikonD70.fields:
            self.failUnless(field in exif.fields, field + " not in fields")
            self.failUnlessEqual(exif.fields[field], NikonD70.fields[field])


if __name__ == '__main__':
    unittest.main()
