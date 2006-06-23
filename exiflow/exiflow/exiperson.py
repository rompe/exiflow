#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
Personalize images by setting EXIF fields to values spezified in exif.cfg or
on command line. Any arbitrary field name may be configured or given.

This is normally used for artist and copyright information.

Field names are the short versions supported by Exiftool. Look up the
Exiftool documentation for information about possible names.
"""

__revision__ = "$Id$"

import sys
import logging
import optparse
import exiflow.exif
import exiflow.filelist
import exiflow.configfile

def run(argv, callback=None):
   """
   Take an equivalent of sys.argv[1:] and optionally a callable.
   Parse options, personalize files and optionally call the callable
   on every processed file with 3 arguments: filename, newname, percentage.
   If the callable returns True, stop the processing.
   """
   parser = optparse.OptionParser(usage="usage: %prog [options] [-- -TAGNAME=" \
                                        "VALUE [...]] <files or dirs>")
   parser.add_option("--section", "-s", dest="section",
                     help="Name of a config file section to be read. This is" \
                          " useful if different people are using the same" \
                          " camera model. By default, the section name is" \
                          " guessed from the camera model. Section 'all' is" \
                          " the default.")
   parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                     help="Be verbose.")
   options, args = parser.parse_args(argv)

   if options.verbose:
      logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger("exiperson")

   exifconfig = exiflow.configfile.parse("exif")

# collect args for Exiftool
   exiftool_args = ""
   remaining_args = []
   for arg in args:
      if arg.startswith("-"):
         exiftool_args += " \"" + arg +"\""
      else:
         remaining_args.append(arg)

   defaultpersonals = []
   if exifconfig.has_section("all"):
      defaultpersonals += exifconfig.items("all")

   if options.section:
      if exifconfig.has_section(options.section):
         defaultpersonals += exifconfig.items(options.section)
      else:
         sys.exit("ERROR: Section %s not found in config files" % \
                  options.section)

   filelist = exiflow.filelist.Filelist(*args)
   for filename, percentage in filelist:
      logger.info("%3s%% %s", percentage, filename)
      if callable(callback):
         if callback(filename, filename, percentage):
            break

      exif_file = exiflow.exif.Exif(filename)
      try:
         exif_file.read_exif()
      except IOError, msg:
         logger.warning("Skipping %s: %s", filename, msg)
         if callable(callback):
            if callback(filename, filename, percentage):
               break
         continue

# Note to programmer: The [:] is needed to get a slice copy instead of a reference.
      personals = defaultpersonals[:]
      if exif_file.fields.has_key("Model"):
         if exifconfig.has_section(exif_file.fields["Model"]):
            personals += exifconfig.items(exif_file.fields["Model"])
         else:
            exiflow.configfile.append("exif", exif_file.fields["Model"],
                                      ("Artist", "Contact"))
            sys.stderr.write("Get rid of this message by defining at least"
                             " an empty [%s] section.\n" %
                             exif_file.fields["Model"])
      
      if len(personals) == 0:
         sys.stderr.write("No [all] or [%s] section with data, skipping.\n" % 
                          exif_file.fields["Model"])
         continue

      exif_file.fields = {}
      for key, value in personals:
         exif_file.fields[key] = value

      try:
         exif_file.write_exif()
      except IOError, msg:
         print "Error writing EXIF data:\n", filename, "\n", msg


if __name__ == "__main__":
   run(sys.argv[1:])

