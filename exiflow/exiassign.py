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
import exiflow.exif


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
      exif_file = exiflow.exif.Exif(imagefile)
      try:
         exif_file.read_exif()
      except IOError, msg:
         print msg
         continue
      if not myoptions.force and exif_file.fields.has_key("DateTimeOriginal"):
         if myoptions.verbose:
            print "Skipping %s, it seems to contain EXIF data." % imagefile
         continue
      mtimes = {}
      for otherfile in glob.glob(os.path.join(os.path.dirname(imagefile),
                                              leader + "*")):
         if otherfile == imagefile:
            continue
         else:
            mtimes[str(os.stat(otherfile).st_mtime) + otherfile] = otherfile
      if len(mtimes) == 0 and myoptions.verbose:
         print "No sibling found for %s." % imagefile
      for otherfile in sorted(mtimes, None, None, True):
         other_exif_file = exiflow.exif.Exif(mtimes[otherfile])
         try:
            other_exif_file.read_exif()
         except IOError:
            continue
         other_exif_file.fields.update(exif_file.fields)
         if other_exif_file.fields != exif_file.fields:
            if myoptions.verbose:
               print "Updating %s from %s." % (imagefile, mtimes[otherfile])
            exif_file.update_exif(mtimes[otherfile])
            break

