#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
A set of functions to handle config files.
They look for existance of ~/.exiflow/<classname>.cfg and will create it if
it doesn't exist. Afterwards a configparser object of this file and
/etc/exiflow/<classname>.cfg is returned.
"""

import os
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
   config = ConfigParser.ConfigParser()
# Create some defaults
   config.add_section("all")
   config.set("all", "image_extensions", ".jpg .nef .raw .crw .tif")
   config.set("all", "unwantend_files", "nikon001.dsc")
   config.set("all", "unwantend_dirs", ".comments")
# Eventually read config files
   read_files = config.read([global_config, local_config])
# Write private config file (unconditionally, in case we have new options)
   if not os.path.isdir(local_config_dir):
      os.makedirs(local_config_dir)
   config.write(open(local_config, "w"))
   return config, read_files

def cameras():
   """
   Handle access to cameras.cfg.
   Return a configparser object and a list of processed files.
   """
   local_config = os.path.join(local_config_dir, "cameras.cfg")
   global_config = os.path.join(global_config_dir, "cameras.cfg")
   config = ConfigParser.ConfigParser()
# Create some defaults
   config.add_section("all")
   config.set("all", "cam_id", "000")
   config.set("all", "artist_initials", "xy")

   config.add_section("NIKON D70")
   config.set("NIKON D70", "cam_id", "n00")

   config.add_section("HP PhotoSmart 715")
   config.set("HP PhotoSmart 715", "cam_id", "hp0")

   config.add_section("C2040Z")
   config.set("C2040Z", "cam_id", "o00")
# Eventually read config files
   read_files = config.read([global_config, local_config])
# Write private config file (unconditionally, in case we have new options)
   if not os.path.isdir(local_config_dir):
      os.makedirs(local_config_dir)
   config.write(open(local_config, "w"))
   return config, read_files

def exif():
   """
   Handle access to exif.cfg.
   Return a configparser object and a list of processed files.
   """
   local_config = os.path.join(local_config_dir, "exif.cfg")
   global_config = os.path.join(global_config_dir, "exif.cfg")
   config = ConfigParser.ConfigParser()
# Create some defaults
   config.add_section("all")
   config.set("all", "Artist", "xxx yyy")
   config.set("all", "Contact", "xy@example.org")
   config.set("all", "Copyright", "(c)2005 xy@example.org")
   config.set("all", "CopyrightNotice", "All rights reserved, no redistribution without written permission.")
   config.set("all", "Credit", "xy@example.org")
   config.set("all", "UserComment", "")

   config.add_section("custom")
   config.set("custom", "Artist", "custom xxx yyy")

   config.add_section("NIKON D70")
   config.set("NIKON D70", "Artist", "custom xxx yyy for this camera")
# Eventually read config files
   read_files = config.read([global_config, local_config])
# Write private config file (unconditionally, in case we have new options)
   if not os.path.isdir(local_config_dir):
      os.makedirs(local_config_dir)
   config.write(open(local_config, "w"))
   return config, read_files

