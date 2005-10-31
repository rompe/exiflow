#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
Personalize images by setting EXIF fields to values spezified in exif.cfg or
on command line. Any arbitrary field name may be configured or given.

Field names are the short versions supported by Exiftool. Look up the
Exiftool documentation for information about possible names.
"""

import os
import optparse
import subprocess
import ConfigParser

configfiles = ["/etc/exiflow/exif.cfg",
               os.path.expanduser('~/.exiflow/exif.cfg')]

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
myoptions, args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.read(configfiles)

# collect args for Exiftool
exiftool_args = ""
remaining_args = []
for arg in args:
   if arg.startswith("-"):
      exiftool_args += " \"" + arg +"\""
   else:
      remaining_args.append(arg)

imagefiles = []
for arg in remaining_args:
   if os.path.isfile(arg):
      imagefiles.append(arg)
   elif os.path.isdir(arg):
      for root, dirs, files in os.walk(arg):
         for myfile in files:
            imagefiles.append(os.path.join(root, myfile))
   else:
      print arg + " is not a regular file or directory."
      sys.exit(1)

defaultpersonals = []
if config.has_section("all"):
   defaultpersonals += config.items("all")
if myoptions.section:
   if config.has_section(myoptions.section):
      defaultpersonals += config.items(myoptions.section)
   else:
      sys.exit("ERROR: Section %s not found in config files" % myoptions.section)


for imagefile in imagefiles:

   try:
      exif = read_exif(imagefile)
   except NotAnImageError, message:
      if myoptions.verbose:
         print "Skipping %s: %s" % (imagefile, message)
      continue

   personals = defaultpersonals[:]
   if exif.has_key("Model") and config.has_section(exif["Model"]):
      personals += config.items(exif["Model"])

   exiftool_config_args = ""
   for pair in personals:
      exiftool_config_args += " -%s=\"%s\"" % pair

   exiftool = "exiftool -P -overwrite_original" + exiftool_config_args + \
              exiftool_args + " " + imagefile

   if myoptions.verbose:
      print "Running: " + exiftool
   subprocess.call(exiftool, shell=True)
