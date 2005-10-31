#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
Find groups of derived images and exchange EXIF information between them.

Example:
 These files are a raw image, a low quality version and two edited versions:
 20050914-n001235-jd000.nef
 20050914-n001235-jd00l.jpg
 20050914-n001235-jd100.jpg
 20050914-n001235-jd110.jpg
 The last one doesn't have EXIF informations. This tool will find that out and
 look at 20050914-n001235-jd100.jpg and 20050914-n001235-jd000.nef in this
 order to copy the EXIF header from.
"""

import os
import re
import sys
import glob
import optparse
import subprocess


class NotAnImageError(Exception):
   def __init__(self, value):
      self.value = value
   def __str__(self):
      return repr(self.value)

def read_exif(filename):
   """
   Read EXIF information from filename
   and return a dictionary containing the collected values.
   """
   myexif = {}
   exiftool = subprocess.Popen("exiftool -S " + filename, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   for line in exiftool.stdout:
      if ": " in line:
         key, value = line.split(": ", 1)
         myexif[key] = value.strip()
   if exiftool.wait():
      raise NotAnImageError, "".join(exiftool.stderr)
   else:
# We have to read the ImageDescription binary because it may contain
# things like line breaks.
      myexif["ImageDescription"] = \
         "".join(subprocess.Popen("exiftool -b -ImageDescription " + filename,
                             shell=True, stdout=subprocess.PIPE).stdout)
# Be shure to have proper UTF8 strings
   for key in myexif:
      myexif[key] = unicode(myexif[key], "utf-8")
   return myexif


def update_exif(destfile, sourcefile, myexif):
   """
   Copy Exif Information from sourcefile into destfile and merge in values
   from myexif. The fields used for merging have to be defined in exiffields.
   Returns True on success.
   """
# Fields we want to keep
   exiffields = ["Artist", "Credit", "Copyright", "CopyrightNotice", 
                 "ImageDescription", "Keywords", "Location", "UserComment",
                 "XPTitle"]
   command = "exiftool -overwrite_original -P -TagsFromFile " + sourcefile
   for field in exiffields:
      if field in myexif:
         if field == "Keywords":
            for keyword in myexif[field].split(","):
               command += " -%s=\"%s\"" % (field, keyword)
         else:
            command += " -%s=\"%s\"" % (field, myexif[field])
   command += " " + destfile
   ret = True
   exiftool = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
# exiftool doesn't reflect errors in it's return code, so we have to
# assume an error if something is written to stderr.
   for line in exiftool.stderr:
      print >>sys.stderr, line
      ret = False
   exiftool.wait()
   return ret


parser = optparse.OptionParser(usage="usage: %prog [options] <files or dirs>")
parser.add_option("-f", "--force", action="store_true", dest="force",
                  help="Force update even if EXIF is already present. " \
                       "The fields handled by these scripts are kept " \
                       "anyway.")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                  help="Be verbose.")
myoptions, args = parser.parse_args()

if len(args) == 0:
   parser.print_help()
   sys.exit(1)

imagefiles = []
for arg in args:
   if os.path.isfile(arg):
      imagefiles.append(arg)
   elif os.path.isdir(arg):
      for root, dirs, files in os.walk(arg):
         for myfile in files:
            imagefiles.append(os.path.join(root, myfile))
   else:
      print arg + " is not a regular file or directory."
      sys.exit(1)

filename_re = re.compile("^(\d{8}-.{3}\d{4}-)(.{5})\.[^.]*$")

for imagefile in imagefiles:
   mymatch = filename_re.match(os.path.basename(imagefile))
   if mymatch:
      leader, revision = mymatch.groups()
      try:
         imageexif = read_exif(imagefile)
      except NotAnImageError, msg:
         print msg
         continue
      if not myoptions.force and imageexif.has_key("DateTimeOriginal"):
         if myoptions.verbose:
            print "Skipping %s, it seems to contain EXIF data." % imagefile
         continue
      mtimes = {}
      for otherfile in glob.glob(leader + "*"):
         if otherfile == imagefile:
            continue
         else:
            mtimes[str(os.stat(otherfile).st_mtime) + otherfile] = otherfile
      for otherfile in sorted(mtimes, None, None, True):
         try:
            otherexif = read_exif(mtimes[otherfile])
         except NotAnImageError:
            continue
         otherexif.update(imageexif)
         if otherexif != imageexif:
            if myoptions.verbose:
               print "Updating %s from %s." % (imagefile, mtimes[otherfile])
            update_exif(imagefile, mtimes[otherfile], imageexif)
            break

