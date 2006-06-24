#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
Import files from given directories to your photo folder.
Optionally unmounts source media after successfull import.
"""
__revision__ = "$Id$"

import os
import sys
import stat
import shutil
import optparse
import subprocess
import exiflow.filelist

def run(argv, callback=None):
   """
   Take an equivalent of sys.argv[1:] and optionally a callable.
   Parse options, import files and optionally call the callable on every
   processed file with 3 arguments: filename, newname, percentage.
   If the callable returns True, stop the processing.
   """
# Parse command line.
   parser = optparse.OptionParser()
   parser.add_option("-m", "--mount", dest="mount",
                     help="Mountpoint of directory to import. Corresponds"
                          " to %m in the gnome-volume-manager config dialog.")
   parser.add_option("-t", "--target", dest="target",
                     help="Target directory. A subdirectory will be created"
                          " in this directory.")
   parser.add_option("-d", "--device", dest="device",
                     help="Mounted device file. If given, this device will be"
                          " unmounted using pumount after the import."
                          " Corresponds to %d in the gnome-volume-manager"
                          " config dialog.")
   parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                     help="Be verbose.")
   options, args = parser.parse_args(argv)
   if len(args) > 0 or not options.mount or not options.target:
      sys.exit("Wrong syntax, call with --help for info.")

# Build file list whithout skipping unknown files
   filelist = exiflow.filelist.Filelist()
   if options.verbose:
      print "Read config files:", " ".join(filelist.get_read_config_files())
   filelist.process_unknown_types()
   filelist.add_files([options.mount])

# Cry if we found no images
   if filelist.get_filecount() == 0:
      sys.exit("No files to import, sorry.")

# Create targetdir
   targetdir = os.path.join(options.target, filelist.get_daterange())
# TODO: find a better solution than just appendings "+" chars.
   while os.path.exists(targetdir):
      targetdir += "+"
   os.makedirs(targetdir)
   print "Importing", filelist.get_fullsize() / 1024 / 1024 , "MB in", \
         filelist.get_filecount(), "files to", targetdir

# Copy files
   for filename, percentage in filelist:
      if options.verbose:
         print "%3s%% %s" % (percentage, filename)
      if callable(callback):
         if callback("", os.path.join(targetdir, os.path.basename(filename)),
                                      percentage, keep_original=True):
            break

      shutil.copy2(filename, targetdir)
      os.chmod(os.path.join(targetdir, os.path.basename(filename)),
               stat.S_IMODE(0644))

# Unmount card
   if options.device:
      subprocess.call("pumount " + options.device, shell=True)


if __name__ == "__main__":
   run(sys.argv[1:])

