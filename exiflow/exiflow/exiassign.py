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
__revision__ = "$Id$"

import os
import re
import sys
import glob
import optparse
import exiflow.exif
import exiflow.filelist


def run(argv, callback=None):
   """
   Take an equivalent of sys.argv[1:] and optionally a callable.
   Parse options, assign relating files and gate meta information between them,
   and optionally call the callable on every processed file with 3 arguments:
   filename, newname, percentage.
   If the callable returns True, stop the processing.
   """
   parser = optparse.OptionParser(usage="usage: %prog [options] "
                                        "<files or dirs>")
   parser.add_option("-f", "--force", action="store_true", dest="force",
                     help="Force update even if EXIF is already present. "
                          "The fields handled by these scripts are kept "
                          "anyway.")
   parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                     help="Be verbose.")
   options, args = parser.parse_args(argv)

   if len(args) == 0:
      parser.print_help()
      sys.exit(1)

   filelist = exiflow.filelist.Filelist(*args)
   if options.verbose:
      print "Read config files:", " ".join(filelist.get_read_config_files())

   filename_re = re.compile("^(\d{8}-.{3}\d{4}-)(.{5})\.[^.]*$")

   for filename, percentage in filelist:
      mymatch = filename_re.match(os.path.basename(filename))
      if mymatch:
         if options.verbose:
            print "%3s%% " % percentage,
         leader, dummy = mymatch.groups()
         exif_file = exiflow.exif.Exif(filename)
         try:
            exif_file.read_exif()
         except IOError, msg:
            print msg
            continue
         if not options.force and exif_file.fields.has_key("DateTimeOriginal"):
            if options.verbose:
               print "Skipping %s, it seems to contain EXIF data." % filename
            if callable(callback):
               if callback(filename, filename, percentage):
                  break
            continue
         mtimes = {}
         for otherfile in glob.glob(os.path.join(os.path.dirname(filename),
                                                 leader + "*")):
            if otherfile == filename:
               continue
            else:
               mtimes[str(os.stat(otherfile).st_mtime) + otherfile] = otherfile
         if len(mtimes) == 0 and options.verbose:
            print "No sibling found for %s." % filename
         for otherfile in sorted(mtimes, None, None, True):
            other_exif_file = exiflow.exif.Exif(mtimes[otherfile])
            try:
               other_exif_file.read_exif()
            except IOError:
               continue
            other_exif_file.fields.update(exif_file.fields)
            if other_exif_file.fields != exif_file.fields:
               if options.verbose:
                  print "Updating %s from %s." % (filename, mtimes[otherfile])
               exif_file.update_exif(mtimes[otherfile])
               if callable(callback):
                  if callback(filename, filename, percentage):
                     break
               break



if __name__ == "__main__":
   run(sys.argv[1:])

