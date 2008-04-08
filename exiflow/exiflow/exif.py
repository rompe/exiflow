#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
A module for reading and writing EXIF information.
"""
__revision__ = "$Id$"

import subprocess

class Exif:
   """
   A class for reading and writing EXIF information.
   """

   def __init__(self, filename):
      """
      Create an Exif object for filename.
      """
      self.filename = filename
      self.fields = {}

   def read_exif(self):
      """
      Read EXIF information from self.filename into self.fields
      Raises IOError on errors.
      """
      exiftool = subprocess.Popen("exiftool -d %s -S " + self.filename,
                                  shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
      for line in exiftool.stdout:
         if ": " in line:
            key, value = line.split(": ", 1)
            self.fields[key] = value.strip()
# TODO: Check if we may rely on exit status or if we have to check stderr like
# we do in write_exif
      if exiftool.wait():
         raise IOError, "".join(exiftool.stderr)
      else:
# We have to read the ImageDescription binary because it may contain
# things like line breaks.
         self.fields["ImageDescription"] = \
            "".join(subprocess.Popen("exiftool -b -ImageDescription "
                                     + self.filename, shell=True,
                                     stdout=subprocess.PIPE).stdout)
# We don't need an empty "ImageDescription" for any merge operations.
         if self.fields["ImageDescription"] == "":
            del self.fields["ImageDescription"] 
# Be shure to have proper UTF8 strings
      for key in self.fields:
         self.fields[key] = unicode(self.fields[key], "utf-8")


   def write_exif(self):
      """
      Write Exif Information from self.fields into self.filename.
      Raises IOError on errors.
      """
      command = "exiftool -overwrite_original -P"
      for field in self.fields.keys():
         if field == "Keywords":
            for keyword in self.fields[field].split(","):
               command += " -%s=\"%s\"" % (field, keyword)
         elif field == "DateTimeOriginal":
# TODO: Writing back DateTimeOriginal seems to be a bad idea since gthumb
# drops seconds and there is some confusion with time strings and epoch.
            continue
         else:
            command += " -%s=\"%s\"" % (field, self.fields[field])
      command += " " + self.filename
      exiftool = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
# exiftool doesn't reflect errors in it's return code, so we have to
# assume an error if something is written to stderr.
      errors = exiftool.stderr.readlines()
      if len(errors) > 0:
         raise IOError, "".join(errors + exiftool.stdout.readlines())
      return exiftool.wait()


   def update_exif(self, sourcefile):
      """
      Copy Exif Information from sourcefile into destfile and merge in values
      from myexif. The fields used for merging have to be defined in exiffields.
      Raises IOError on errors.
      """
# Fields we want to keep
      exiffields = ["Artist", "Credit", "Copyright", "CopyrightNotice", 
                    "ImageDescription", "Keywords", "Location", "UserComment",
                    "XPTitle"]
      command = "exiftool -overwrite_original -x Orientation -P -TagsFromFile " + sourcefile
      for field in exiffields:
         if field in self.fields:
            if field == "Keywords":
               for keyword in self.fields[field].split(","):
                  command += " -%s=\"%s\"" % (field, keyword)
            else:
               command += " -%s=\"%s\"" % (field, self.fields[field])
      command += " " + self.filename
      exiftool = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
# exiftool doesn't reflect errors in it's return code, so we have to
# assume an error if something is written to stderr.
      errors = exiftool.stderr.readlines()
      if len(errors) > 0:
         raise IOError, "".join(errors + exiftool.stdout.readlines())
      return exiftool.wait()


