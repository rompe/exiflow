#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
Convert any RAW images into JPEG images.

The raw file extensions as well as the converters to call
are read from the config file "cameras.cfg" using the keys
"raw_extension" and "raw_converter". As alway, the [all]
section may contain general defaults used for all cameras
and camera specific sections may contain values for a given
camera model.

An example section would look like this:

[NIKON D70]
raw_extension = .nef
raw_converter = ufraw-batch --clip --out-type=jpeg

Given this, any files produced by a Nikon D70 that end in
".nef" are converted using this artificial ufraw call.

The raw converter is expected to write a file of the same
prefix as the input file with an extension of ".jpg".
For example, a file "test.nef" should result in "test.jpg".
"""

__revision__ = "$Id$"

import os
import sys
import logging
import optparse
import subprocess
import exiflow.exif
import exiflow.filelist
import exiflow.configfile


def convert_file(filename, cameraconfig):
   """
   Convert filename and return the newly generated name without dir.
   """
   logger = logging.getLogger("exiconvert.convert_file")
   basename = os.path.basename(filename)
# Sanity check - no sense in trying to convert jpeg  to jpeg
   if basename.lower().endswith(".jpg"):
      logger.debug("%s is a Jpeg file, skipping.", basename)
      return basename

   exif_file = exiflow.exif.Exif(filename)
# read_exif may throw IOError. We leave the catching to our caller.
   exif_file.read_exif()
   model = exif_file.fields.get("Model", "all")

   if cameraconfig.has_section(model) \
      and cameraconfig.has_option(model, "raw_extension"):
      raw_extension = cameraconfig.get(model, "raw_extension")
   elif cameraconfig.has_section("all") \
      and cameraconfig.has_option("all", "raw_extension"):
      raw_extension = cameraconfig.get("all", "raw_extension")
   else:
      exiflow.configfile.append("cameras", model,
                                "raw_extension", "raw_converter")
      logger.warning("No raw_extension configured, skipping %s", basename)
      return basename

   if not filename.endswith(raw_extension):
      logger.debug("%s doesn't match, skipping.", filename)
      return basename
      
   if cameraconfig.has_section(model) \
      and cameraconfig.has_option(model, "raw_converter"):
      raw_converter = cameraconfig.get(model, "raw_converter")
   elif cameraconfig.has_section("all") \
      and cameraconfig.has_option("all", "raw_converter"):
      raw_converter = cameraconfig.get("all", "raw_converter")
   else:
      exiflow.configfile.append("cameras", model,
                                "raw_extension", "raw_converter")
      logger.warning("No raw_converter configured, skipping %s", basename)
      return basename

   newname = os.path.splitext(filename)[0] + ".jpg"
   if os.path.exists(newname):
      logger.info("%s already exists, skipping %s.", newname, basename)
      return basename
   command = raw_converter + " " + filename
   if subprocess.call(command, shell=True) > 0:
      logger.error("Converter invocation returned an error:\n%s", command)
      return basename
   if not os.path.exists(newname):
      logger.error("Converter returned 0, but %s is absent!", newname)
   else:
      return os.path.basename(newname)



def run(argv, callback=None):
   """
   Take an equivalent of sys.argv[1:] and optionally a callable.
   Parse options, convert convertible files and optionally call the callable
   on every processed file with 4 arguments: filename, newname, percentage,
   keep_original=true. The latter option means "The new file is an addition,
   not a replacement". If the callable returns True, stop the processing.
   """
   parser = optparse.OptionParser(usage="usage: %prog [options] "
                                        "<files or dirs>")
   parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                     help="Be verbose.")
   options, args = parser.parse_args(args=argv)

   if options.verbose:
      logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger("exiconvert")

   cameraconfig, read_config_files = exiflow.configfile.cameras()

   filelist = exiflow.filelist.Filelist(*args)
   logger.info("Read settings config files: %s",
               " ".join(filelist.get_read_config_files()))
   logger.info("Read camera config files: %s",
               " ".join(read_config_files))

   for filename, percentage in filelist:
      try:
         newname = convert_file(filename, cameraconfig)
      except IOError, msg:
         newname = os.path.basename(filename)
         logger.error("Skipping %s:\n%s\n", filename, msg)
      logger.info("%3s%% %s", percentage, filename)
      if callable(callback):
         if callback(filename,
                     os.path.join(os.path.dirname(filename), newname),
                     percentage, keep_original=True):
            break


if __name__ == "__main__":
   run(sys.argv[1:])

