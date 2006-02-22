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
import sys
import time
import optparse
import exiflow.exif
import exiflow.filelist
import exiflow.configfile


def rename_file(filename, cameraconfig, cam_id=None, artist_initials=None):
   """
   Rename filename and return the newly generated name without dir.
   """
   filename_re = re.compile("^\d{8}-.{3}\d{4}-.{5}\.[^.]*$")
   if filename_re.match(os.path.basename(filename)):
      raise IOError, filename + " already seems to be formatted."
   tmpindex = filename.rfind(".")
   number = filename[tmpindex - 4 : tmpindex].ljust(4, "0")
   try:
      int(number)
   except ValueError:
      raise IOError, "Can't find a number in " + filename
   extension = filename[tmpindex + 1 : len(filename)].lower()
   leader = filename[0 : tmpindex]
   exif_file = exiflow.exif.Exif(filename)
# read_exif may throw IOError. We leave the catching to our caller.
   exif_file.read_exif()
   model = exif_file.fields.get("Model", "all")
   date = exif_file.fields.get("DateTimeOriginal", "0")
   if ":" in date:
      date = date[0:4] + date[5:7] + date[8:10]
   else:
      if date == "0":
         date = os.stat(filename).st_mtime
      date = time.strftime("%Y%m%d", time.localtime(float(date)))

   if not cam_id:
      if cameraconfig.has_section(model) and cameraconfig.has_option(model,
                                                                     "cam_id"):
         cam_id = cameraconfig.get(model, "cam_id")
      elif cameraconfig.has_section("all") and cameraconfig.has_option("all",
                                                                     "cam_id"):
         cam_id = cameraconfig.get("all", "cam_id")
      else:
         cam_id = "000"

   if not artist_initials:
      if cameraconfig.has_section(model) and cameraconfig.has_option(model,
                                                           "artist_initials"):
         artist_initials = cameraconfig.get(model, "artist_initials")
      elif cameraconfig.has_section("all") and cameraconfig.has_option("all",
                                                           "artist_initials"):
         artist_initials = cameraconfig.get("all", "artist_initials")
      else:
         artist_initials = "xy"

   revision = "000"
# Look for high quality versions of this image
   if extension == "jpg":
# TODO: find a simpler version of this loop, maybe fnmatch.filter()?
      count = 0
      for tmpfile, tmppercentage in filelist:
         if tmpfile.startswith(leader):
            count += 1
      if count > 1:
         revision = "00l"
   newname = date + "-" + cam_id + number + "-" + artist_initials + revision + \
             "." + extension
   os.rename(filename, os.path.join(os.path.dirname(filename), newname))
   return newname


def run(argv, callback=None):
   parser = optparse.OptionParser(usage="usage: %prog [options] <files or dirs>")
   parser.add_option("--cam_id", "-c", dest="cam_id",
                     help="ID string for the camera model. Should normally be" \
                          " three characters long.")
   parser.add_option("--artist_initials", "-a", dest="artist_initials",
                     help="Initials of the artist. Should be two characters" \
                          " long.")
   parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                     help="Be verbose.")
   options, args = parser.parse_args(args=argv)

   cameraconfig, read_config_files = exiflow.configfile.cameras()

   filelist = exiflow.filelist.Filelist(*args)
   if options.verbose:
      print "Read settings config files:", " ".join(filelist.get_read_config_files())
      print "Read camera config files:", " ".join(read_config_files)


   for filename, percentage in filelist:
      try:
         newname = rename_file(filename, cameraconfig,
                               options.cam_id, options.artist_initials)
      except IOError, msg:
         newname = os.path.basename(filename)
         sys.stderr.write("ERROR, skipping %s:\n%s\n" % (filename, str(msg)))
      if options.verbose:
          print "%3s%% %s -> %s" % (percentage, filename, newname)
      if callable(callback):
         if callback(filename,
                     os.path.join(os.path.dirname(filename), newname),
                     percentage):
            break


if __name__ == "__main__":
   run(sys.argv[1:])

