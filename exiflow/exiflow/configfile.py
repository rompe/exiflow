#!/usr/bin/python
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
import logging
import ConfigParser

__global_config_dir = "/etc/exiflow"
__local_config_dir = os.path.expanduser('~/.exiflow')

# Defaults
__default_contents = {"settings": """# settings.cfg
# This file defines some values to tell exiflow which types of files
# we want to process and which files and dirs we always want to skip.
# The only valid section here is [all].

   [all]
   image_extensions = .jpg .nef .raw .crw .tif
   unwantend_files = nikon001.dsc
   unwantend_dirs = .comments
""",
                      "cameras": """# cameras.cfg
# This file defines values to be used as filename parts and converters to be
# used for conversion of RAW file formats to JPEG.. An example filename:
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
#raw_extension = .nef
#raw_converter = ufraw-batch --gamma=0.45 --saturation=1.0 --exposure=0.0 --black-point=0 --interpolation=ahd --compression=85 --noexif --wb=camera --curve=linear --linearity=0.06 --clip --out-type=jpeg

#[HP PhotoSmart 715]
#cam_id = hp0

#[C2040Z]
#cam_id = o00
""",
                         "exif": """# exif.cfg
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
"""}

# ConfigParser Caches
__cache = {}


def parse(configname):
   """
   Handle cached access to <configname>.cfg.
   Return a configparser object and a list of processed files.
   """
   logger = logging.getLogger("configfile.parse")
   if not __cache.has_key(configname):
      local_config = os.path.join(__local_config_dir, configname + ".cfg")
      global_config = os.path.join(__global_config_dir, configname + ".cfg")
      if not os.path.exists(local_config):
         if not os.path.isdir(__local_config_dir):
            os.makedirs(__local_config_dir)
         file(local_config, "w").write(__default_contents[configname])
         logger.warning("Created example %s.", local_config)
      config = ConfigParser.ConfigParser()
      read_files = config.read([global_config, local_config])
      logger.info("Read %s config files: %s", configname, " ".join(read_files))
      __cache[configname] = config
   return __cache[configname]


def get_options(configname, section, options):
   """
   Try to get options from section "section" from configfile "configname".
   If section doesn't exist or options don't exist in it, fall back to
   section "all". If that doesn't succed either, call append() and return
   empty values.
   """
   config = parse(configname)
   values = []
   for option in options:
      if config.has_section(section) and config.has_option(section, option):
         values.append(config.get(section, option))
      elif config.has_section("all") and config.has_option("all", option):
         values.append(config.get("all", option))
      else:
         append(configname, section, options)
         values.append("")
   return values


def append(configname, section, options):
   """
   Append a commented section with options to "configname".cfg
   """
   configfile = os.path.join(__local_config_dir, configname + ".cfg")
   string_to_append = "\n#[%s]\n#%s = \n" % (section, " = \n#".join(options))
   if string_to_append in "".join(file(configfile, "r").readlines()):
      sys.stderr.write("Commented section [%s] found in %s\nPlease edit!\n" %
                       (section, configfile))
   else:
      sys.stderr.write("Adding commented section [%s] to %s\nPlease edit!\n" %
                       (section, configfile))
      file(configfile, "a").write(string_to_append)

