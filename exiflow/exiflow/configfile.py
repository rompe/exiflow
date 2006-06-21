#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
A set of functions to handle config files.
They look for existance of ~/.exiflow/<classname>.cfg and will create it if
it doesn't exist. Afterwards a configparser object of this file and
/etc/exiflow/<classname>.cfg is returned.
"""
__revision__ = "$Id: "

import os
import sys
import ConfigParser

global_config_dir = "/etc/exiflow"
local_config_dir = os.path.expanduser('~/.exiflow')


def settings():
   """
   Handle access to settings.cfg.
   Return a configparser object and a list of processed files.
   """
   local_config = os.path.join(local_config_dir, "settings.cfg")
   global_config = os.path.join(global_config_dir, "settings.cfg")
   if not os.path.exists(global_config) and not os.path.exists(local_config):
      if not os.path.isdir(local_config_dir):
         os.makedirs(local_config_dir)
      file(local_config, "w").write("""# settings.cfg
# This file defines some values to tell exiflow which types of files
# we want to process and which files and dirs we always want to skip.
# The only valid section here is [all].

[all]
image_extensions = .jpg .nef .raw .crw .tif
unwantend_files = nikon001.dsc
unwantend_dirs = .comments
""")
      sys.stderr.write("Created example " + local_config + "\n")
   config = ConfigParser.ConfigParser()
   read_files = config.read([global_config, local_config])
   return config, read_files


def cameras():
   """
   Handle access to cameras.cfg.
   Return a configparser object and a list of processed files.
   """
   local_config = os.path.join(local_config_dir, "cameras.cfg")
   global_config = os.path.join(global_config_dir, "cameras.cfg")
   if not os.path.exists(global_config) and not os.path.exists(local_config):
      if not os.path.isdir(local_config_dir):
         os.makedirs(local_config_dir)
      file(local_config, "w").write("""# cameras.cfg
# This file defines values to be used as filename parts. An example filename:
#
# 20050807-n005965-sb000.jpg
#
# In this case cam_id was "n00" and artist_initials was "sb".
#
# While it is possible to only have an [all] section in this file, we recommend
# using camera specific sections for at least the cam_id to generate unique and
# meaningfull filenames.

#[all]
#cam_id = 000
#artist_initials = xy

#[NIKON D70]
#cam_id = n00
#artist_initials = yz

#[HP PhotoSmart 715]
#cam_id = hp0

#[C2040Z]
#cam_id = o00
""")
      sys.stderr.write("Created example " + local_config + "\n")
   config = ConfigParser.ConfigParser()
   read_files = config.read([global_config, local_config])
   return config, read_files


def exif():
   """
   Handle access to exif.cfg.
   Return a configparser object and a list of processed files.
   """
   local_config = os.path.join(local_config_dir, "exif.cfg")
   global_config = os.path.join(global_config_dir, "exif.cfg")
   if not os.path.exists(global_config) and not os.path.exists(local_config):
      if not os.path.isdir(local_config_dir):
         os.makedirs(local_config_dir)
      file(local_config, "w").write("""# exif.cfg
# This file contains EXIF information to be inserted into images.
# Configure global values in the [all] section and camera specific values
# in a section for the camera model. It is also possible to create sections
# with arbitrary names and supply these names later on the command line.

#[all]
#Artist = Arthur Dent
#Contact = adent@example.com
#Copyright = (c)2006 adent@example.com
#CopyrightNotice = All rights reserved, no redistribution without written permission.
#Credit = adent@example.com
# ATTENTION: You will want to set UserComment to an empty string even if you
# do not use it. It will prevent Exiftool from setting it to the word "ASCII".
#UserComment = 

#[custom]
#artist = I. M. Weasel

#[NIKON D70]
#artist = I. R. Baboon
""")
      sys.stderr.write("Created example " + local_config + "\n")
   config = ConfigParser.ConfigParser()
   read_files = config.read([global_config, local_config])
   return config, read_files


def append(configname, section, *entries):
   """
   Append a commented section with entries to "configname".cfg
   """
   configfile = os.path.join(local_config_dir, configname + ".cfg")
   string_to_append = "\n#[%s]\n#%s = \n" % (section, " = \n#".join(entries))
   if string_to_append in "".join(file(configfile, "r").readlines()):
      sys.stderr.write("Commented section [%s] found in %s\nPlease edit!\n" %
                       (section, configfile))
   else:
      sys.stderr.write("Adding commented section [%s] to %s\nPlease edit!\n" %
                       (section, configfile))
      file(configfile, "a").write(string_to_append)

