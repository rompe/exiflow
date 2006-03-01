#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
Rename a bunch of image files according to our holy file naming schema.

Given a camera that saves a file as:

dsc_1234.nef

we will rename that file to:

20050412-n001234-ur000.nef

At first there is 20050412. That's a date, telling us the
photo has been taken on 2005-04-12. This is determined by
looking it up in the image's EXIF information.

Then there is n001234. The "n00" part is read from a config
file as the three byte string to be put there for a given
camera model. In this case, the camera model information in
the EXIF header reads "Nikon D70", and the config section
for that model reads "n00", meaning an "n" as a model
indicator since I also own an HP camera for which I
configured "h00", and the "00" as a way to extend the
counting possibilities beyond 9999 pictures. Once the
camera switches from 9999 to 0000 I will change that string
to "n01". The "1234" part is just the numeric part of the
original filename.

At last there is ur000. "ur" are my initials; I have
simply configured "If it's a Nikon D70, the artist is me".
Of course there are possibilities to override that. The
"000" part is a revision number. This is an original,
untouched file, so it's revision is 000. An automatic
conversion to JPG would also have revision 000 since there
is no interaction and the files are still distinguishable
by their suffixes. Once I convert it with custom parameters
or do some kind of editing, I will save it as revision 100.
Another derivate of the original will get revision 200.
A derivate of revision 100 will get 110, a derivate of 110
will get 111 and another one will get 112. Got the idea?
Using this revision scheme lets you know about the basic
editing history (if there's any) by just looking at the
filename. If this is too complicated for your needs you
are free to use these three bytes in another way or to
leave them alone.
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

