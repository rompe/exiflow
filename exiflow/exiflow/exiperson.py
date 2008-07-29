#!/usr/bin/python
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
sys.path.insert(1, "/usr/share/exiflow") 
import exiflow.exif
import exiflow.filelist
import exiflow.configfile


def personalize_file(filename, personals, forced_personals):
   """
   Personalize an image using data from the dictionary "personals".
   The optional "forced_personals" override all other personals.
   """
   logger = logging.getLogger("exiperson.personalize_file")
   exifconfig = exiflow.configfile.parse("exif")
   exif_file = exiflow.exif.Exif(filename)
   try:
      exif_file.read_exif()
   except IOError, msg:
      logger.warning("Skipping %s: %s", filename, msg)
      return 1

   if exif_file.fields.has_key("Model"):
      if exifconfig.has_section(exif_file.fields["Model"]):
         personals += exifconfig.items(exif_file.fields["Model"])
      else:
         exiflow.configfile.append("exif", exif_file.fields["Model"],
                                   ("Artist", "Contact"))
         sys.stderr.write("Get rid of this message by defining at least"
                          " an empty [%s] section.\n" %
                          exif_file.fields["Model"])
   
   if len(forced_personals) > 0:
      personals.update(forced_personals)

   if len(personals) == 0:
      logger.warning("No [all] or [%s] section with data, skipping.", 
                     exif_file.fields["Model"])
      return 1

   exif_file.fields = {}
   for key, value in personals:
      exif_file.fields[key] = value

   try:
      exif_file.write_exif()
   except IOError, msg:
      logger.error("Error writing EXIF data:%s\n%s", filename, msg)
      return 1
   return 0


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

   logging.basicConfig(format="%(module)s: %(message)s")
   if options.verbose:
      logging.getLogger().setLevel(logging.INFO)
   logger = logging.getLogger("exiperson")

   exifconfig = exiflow.configfile.parse("exif")

   defaultpersonals = []
   if exifconfig.has_section("all"):
      defaultpersonals += exifconfig.items("all")

   if options.section:
      if exifconfig.has_section(options.section):
         defaultpersonals += exifconfig.items(options.section)
      else:
         logger.error("ERROR: Section %s not found in config files",
                      options.section)
         sys.exit(1)

# collect EXIF data supplied on command line
   forced_personals = {}
   remaining_args = []
   for arg in args:
      if arg.startswith("-") and "=" in arg:
         field, value = arg.lstrip("-").split("=")
         forced_personals[field] += value
      else:
         remaining_args.append(arg)

   for filename, percentage in exiflow.filelist.Filelist(remaining_args):
      logger.info("%3s%% %s", percentage, filename)
      if callable(callback):
         if callback(filename, filename, percentage):
            break
# Note to programmer:
# The [:] is needed to get a slice copy instead of a reference.
      personalize_file(filename, defaultpersonals[:], forced_personals)


if __name__ == "__main__":
   run(sys.argv[1:])

