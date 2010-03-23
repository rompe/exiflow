#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests for exif.py
"""
__revision__ = "$Id$"


import shutil
import os
import pprint
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
        self.__tempdir = tempfile.mkdtemp()
        self.__d70jpeg = os.path.join(self.__tempdir, "NikonD70.jpg")
        shutil.copy(os.path.join(sys.path[0], "NikonD70.jpg"), self.__tempdir)
        self.__d70jpeg_imgdesc_latin1 = os.path.join(self.__tempdir,
            "NikonD70_ImageDescription_2rows_latin1.jpg")
        shutil.copy(os.path.join(sys.path[0], 
            "NikonD70_ImageDescription_2rows_latin1.jpg"), self.__tempdir)
        self.__d70jpeg_imgdesc_utf8 = os.path.join(self.__tempdir,
            "NikonD70_ImageDescription_2rows_utf8.jpg")
        shutil.copy(os.path.join(sys.path[0], 
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
        for field in ("Directory", "FileModifyDate"):
            exif.fields[field] = NikonD70.fields[field]
        self.failUnlessEqual(exif.fields, NikonD70.fields)

    def test_read_exif_imagedescription(self):
        """ Tests for read_exif() with valid image """
        exif = exiflow.exif.Exif(self.__d70jpeg_imgdesc_utf8)
        self.failUnless(isinstance(exif, exiflow.exif.Exif))
        exif.read_exif()
        for field in ("Directory", "FileModifyDate"):
            exif.fields[field] = NikonD70.fields[field]
        self.failUnlessEqual(exif.fields["ImageDescription"], 
            u"ImageDescription first row äöüß\nImageDescription second row ÄÖÜß\n")

    def test_read_exif_imagedescription_decode(self):
        """ Tests for read_exif() with valid image """
        exif = exiflow.exif.Exif(self.__d70jpeg_imgdesc_latin1)
        self.failUnless(isinstance(exif, exiflow.exif.Exif))
        exif.read_exif()
        for field in ("Directory", "FileModifyDate"):
            exif.fields[field] = NikonD70.fields[field]
        self.failUnlessEqual(exif.fields["ImageDescription"], 
            u"ImageDescription first row äöüß\nImageDescription second row ÄÖÜß\n")

    

if __name__ == '__main__':
    unittest.main()

