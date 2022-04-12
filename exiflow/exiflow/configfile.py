#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
A set of functions to handle config files.

They look for existance of ~/.exiflow/<classname>.cfg and will create it if
it doesn't exist. Afterwards a configparser object of this file and
/etc/exiflow/<classname>.cfg is returned.
"""
__revision__ = "$Id: "

import os
import logging
import configparser
from typing import Dict, List, Iterable, Optional

GLOBAL_CONFIG_DIR = "/etc/exiflow"
local_config_dir = os.path.expanduser('~/.exiflow')

# Defaults
__default_contents = {"settings": open(os.path.join(os.path.dirname(__file__),
                                                    "default_settings.cfg"),
                                       encoding="utf-8").read(),
                      "cameras": open(os.path.join(os.path.dirname(__file__),
                                                   "default_cameras.cfg"),
                                      encoding="utf-8").read(),
                      "exif": open(os.path.join(os.path.dirname(__file__),
                                                "default_exif.cfg"),
                                   encoding="utf-8").read()}

# ConfigParser Caches
__cache: Dict[str, configparser.ConfigParser] = {}
__stats: Dict[str, Optional[os.stat_result]] = {}


def __stat(filename: str) -> Optional[os.stat_result]:
    """Return a stat object or None if "filename" doesn't exist."""
    try:
        return os.stat(filename)
    except OSError:
        return None


def parse(configname: str) -> configparser.ConfigParser:
    """
    Handle cached access to <configname>.cfg.

    Return a configparser object and a list of processed files.
    """
    logger = logging.getLogger("configfile.parse")
    local_config = os.path.join(local_config_dir, configname + ".cfg")
    global_config = os.path.join(GLOBAL_CONFIG_DIR, configname + ".cfg")
    if (configname not in __cache
            or __stats.get(local_config, None) != __stat(local_config)
            or __stats.get(global_config, None) != __stat(global_config)):
        if not os.path.exists(local_config):
            if not os.path.isdir(local_config_dir):
                os.makedirs(local_config_dir)
            with open(local_config, "w", encoding="utf-8") as cfg_file:
                cfg_file.write(__default_contents[configname])
            logger.warning("Created example %s.", local_config)
        __stats[local_config] = __stat(local_config)
        __stats[global_config] = __stat(global_config)
        config = configparser.ConfigParser()
        read_files = config.read([global_config, local_config])
        logger.info("Read %s config files: %s",
                    configname, " ".join(read_files))
        __cache[configname] = config
    return __cache[configname]


def get_options(configname: str, section: str, options: Iterable[str]):
    """
    Try to get options from section "section" from configfile "configname".

    If section doesn't exist or options don't exist in it, fall back to
    section "all". If that doesn't succed either, call append() and return
    empty values.
    """
    config = parse(configname)
    values: List[str] = []
    must_append = False
    for option in options:
        if config.has_section(section) and config.has_option(section, option):
            values.append(config.get(section, option))
        elif config.has_section("all") and config.has_option("all", option):
            values.append(config.get("all", option))
        else:
            must_append = True
            values.append("")
    if must_append:
        append(configname, section, options)
    return values


def append(configname: str, section: str, options: Iterable[str]) -> None:
    """Append a commented section with options to "configname".cfg."""
    logger = logging.getLogger("configfile.append")
    configfile = os.path.join(local_config_dir, configname + ".cfg")
    string_to_append = "\n#[%s]\n#%s = \n" % (section, " = \n#".join(options))
    with open(configfile, "r", encoding="utf-8") as cfg_file:
        cfg_content = "".join(cfg_file.readlines())
    if string_to_append in cfg_content:
        logger.warning("Commented section [%s] found in %s\nPlease edit!\n",
                       section, configfile)
    else:
        logger.warning("Adding commented section [%s] to %s\nPlease edit!\n",
                       section, configfile)
        with open(configfile, "a", encoding="utf-8") as cfg_file:
            cfg_file.write(string_to_append)
