#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
import optparse
import os
import sys
import gzip
import xml.dom.minidom
import re
import exiflow.exif
import exiflow.gthumb
import exiflow.filelist


def autogate_gthumb(filename, myoptions):
   """
   Decide if we gate from gthumb to Exif or vice versa by looking at the
   time stamps of the comment and the Exif file.
   Run read and write functions accordingly.
   """
   filename = os.path.abspath(filename)
   gthumbfile = exiflow.gthumb.Gthumb(filename)
   gthumbtimestamp = gthumbfile.get_mtime()
   filetimestamp = os.path.getmtime(filename)
   if gthumbtimestamp > filetimestamp:
      if myoptions.verbose:
         print "Updating", filename, "from comment file"
      try:
         gthumbfile.read()
      except IOError, msg:
         print "Error reading gthumb comment:\n", myxmlfile, "\n", msg
         return False
      exif_file = exiflow.exif.Exif(filename)
      exif_file.fields = gthumbfile.fields
      try:
         exif_file.write_exif()
      except IOError, msg:
         print "Error writing EXIF data:\n", filename, "\n", msg
         return False
# TODO: Find out why we intruduced this line. Seems odd...
      #write_gthumb(filename, gthumb, myoptions.addfields,
      #             myoptions.template)
      gthumbfile.set_mtime(filetimestamp)
      os.utime(filename, (filetimestamp, filetimestamp))
   elif filetimestamp > gthumbtimestamp or myoptions.addfields or myoptions.template:
      if myoptions.verbose:
         print "Updating comment file from", filename
      exif_file = exiflow.exif.Exif(filename)
      try:
         exif_file.read_exif()
      except IOError, message:
         if myoptions.verbose:
            print "Skipping %s: %s" % (filename, message)
         return 1
      gthumbfile.fields = exif_file.fields
      gthumbfile.write(myoptions.addfields, myoptions.template)
      gthumbfile.set_mtime(filetimestamp)
   else:
      if myoptions.verbose:
         print filename, "is in sync with comment file"
   return True


def run(argv, callback=None):
   parser = optparse.OptionParser(usage="usage: %prog [options] <files or dirs>")
   parser.add_option("--gthumb", action="store_true", dest="gthumb",
                     help="Gateway to/from gthumb comment files."
                          "This is the default.")
   parser.add_option("--additional-fields", "-a", action="store_true",
                     dest="addfields",
                     help="When gating from Exif to gthumb, combine "
                          "additional Exif fields into the comment.")
   parser.add_option("--template", "-t", action="store_true", dest="template",
                     help="Like --additional-fields, but also combine empty "
                          "fields as templates into the comment.")
# TODO: 
#parser.add_option("--merge", action="store_true", dest="merge",
#                  help="Merge data instead of just using the newest version "\
#                       "to overwrite the older one.")
   parser.add_option("--cleanup", "-c", action="store_true", dest="cleanup",
                     help="The opposite of --additional-fields, that is, "
                          "remove additional fields from gthumb comments.")
   parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                     help="Be verbose.")
   options, args = parser.parse_args(argv)

   filelist = exiflow.filelist.Filelist(*args)
   if options.verbose:
      print "Read config files:", " ".join(filelist.get_read_config_files())

   for filename, percentage in filelist:
      if options.verbose:
         print "%3s%% " % percentage,
      if callable(callback):
         if callback(filename, filename, percentage):
	    break
      autogate_gthumb(filename, options)
      if options.cleanup:
         log_prefix = "Leaving"
         if exiflow.gthumb.Gthumb(filename).cleanup():
            log_prefix = "Cleaning"
         if options.verbose:
            print log_prefix, "comment file of", filename


if __name__ == "__main__":
   run(sys.argv[1:])


