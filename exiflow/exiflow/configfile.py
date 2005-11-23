#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
A set of functions to handle config files.
They look for existance of ~/.exiflow/<classname>.cfg and will create it if
it doesn't exist. Afterwards a configparser object of this file and
/etc/exiflow/<classname>.cfg is returned.
"""

import os.path
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
# Write private config file
   config.write(open(local_config, "w"))
   return config, read_files

