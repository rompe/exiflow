#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
Rename a bunch of image files according to our holy file naming schema.

Example:
dsc_1235.jpg  becomes  20050914-n001235-jd000.jpg

Here's why:
TODO: too lazy to document right now
"""

import os
import re
import time
import optparse
import subprocess
import ConfigParser

configfiles = ["/etc/exiflow/cameras.cfg",
               os.path.expanduser('~/.exiflow/cameras.cfg')]

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


parser = optparse.OptionParser(usage="usage: %prog [options] <files or dirs>")
parser.add_option("--cam_id", "-c", dest="cam_id",
                  help="ID string for the camera model. Should normally be" \
                       " three characters long.")
parser.add_option("--artist_initials", "-a", dest="artist_initials",
                  help="Initials of the artist. Should be two characters" \
                       " long.")
parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                  help="Be verbose.")
myoptions, args = parser.parse_args()

config = ConfigParser.ConfigParser()
config.read(configfiles)

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

filename_re = re.compile("^\d{8}-.{3}\d{4}-.{5}\.[^.]*$")

for imagefile in imagefiles:
   if filename_re.match(os.path.basename(imagefile)):
      if myoptions.verbose:
         print imagefile, "already seems to be formatted, skipping."
      continue
   tmpindex = imagefile.rfind(".")
   number = imagefile[tmpindex - 4 : tmpindex].ljust(4, "0")
   try:
      int(number)
   except ValueError:
      if myoptions.verbose:
         print "Can't find a number in", imagefile, ", skipping."
      continue
   extension = imagefile[tmpindex + 1 : len(imagefile)].lower()
   leader = imagefile[0 : tmpindex]
   try:
      exif = read_exif(imagefile)
   except NotAnImageError, message:
      if myoptions.verbose:
         print "Skipping %s: %s" % (imagefile, message)
      continue
   model = exif.get("Model", "all")
   date = exif.get("DateTimeOriginal", "0")
   if ":" in date:
      date = date[0:4] + date[5:7] + date[8:10]
   else:
      if date == "0":
         date = os.stat(imagefile).st_mtime
      date = time.strftime("%Y%m%d", time.localtime(float(date)))

   if myoptions.cam_id:
      cam_id = myoptions.cam_id
   elif config.has_section(model) and config.has_option(model, "cam_id"):
      cam_id = config.get(model, "cam_id")
   elif config.has_section("all") and config.has_option("all", "cam_id"):
      cam_id = config.get("all", "cam_id")
   else:
      cam_id = "000"

   if myoptions.artist_initials:
      artist_initials = myoptions.artist_initials
   elif config.has_section(model) and config.has_option(model,
                                                        "artist_initials"):
      artist_initials = config.get(model, "artist_initials")
   elif config.has_section("all") and config.has_option("all",
                                                        "artist_initials"):
      artist_initials = config.get("all", "artist_initials")
   else:
      artist_initials = "xy"

   revision = "000"
# Look for high quality versions of this image
   if extension == "jpg":
# TODO: find a simpler version of this loop, maybe fnmatch.filter()?
      count = 0
      for tmpfile in imagefiles:
         if tmpfile.startswith(leader):
            count += 1
      if count > 1:
         revision = "00l"
   newname = date + "-" + cam_id + number + "-" + artist_initials + revision + \
             "." + extension
   if myoptions.verbose:
       print imagefile, "->", newname
   os.rename(imagefile, os.path.join(os.path.dirname(imagefile), newname))
