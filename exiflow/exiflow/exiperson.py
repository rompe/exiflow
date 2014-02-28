#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
Personalize images by setting EXIF fields to values spezified in exif.cfg or
on command line. Any arbitrary field name may be configured or given.

This is normally used for artist and copyright information.

Field names are the short versions supported by Exiftool. Look up the
Exiftool documentation for information about possible names.
"""

__revision__ = "$Id$"

import sys
import logging
import optparse
from . import exif
from . import filelist
from . import configfile


def personalize_file(filename, personals, options_section_personals,
                     forced_personals):
    """
    Personalize an image using data from the dictionary "personals".
    The optional "forced_personals" override all other personals.
    """
    logger = logging.getLogger("exiperson.personalize_file")
    exifconfig = configfile.parse("exif")
    exif_file = exif.Exif(filename)
    try:
        exif_file.read_exif()
    except IOError, msg:
        logger.warning("Skipping %s: %s", filename, msg)
        return 1

    if "Model" in exif_file.fields:
        if exifconfig.has_section(exif_file.fields["Model"]):
            personals += exifconfig.items(exif_file.fields["Model"])
        else:
            configfile.append("exif", exif_file.fields["Model"],
                              ("artist", "contact"))
            sys.stderr.write("Get rid of this message by defining at least"
                             " an empty [%s] section.\n" %
                             exif_file.fields["Model"])

    if len(options_section_personals) > 0:
        personals += options_section_personals

    if len(personals) == 0 and len(forced_personals) == 0:
        logger.warning("No [all] or [%s] section with data, nor custom tags,"
                       " skipping.", exif_file.fields["Model"])
        return 1

    exif_file.fields = {}
    for key, value in personals:
        exif_file.fields[key] = value

    if len(forced_personals) > 0:
        for key in forced_personals:
            exif_file.fields[key] = forced_personals[key]

    try:
        exif_file.write_exif()
    except IOError, msg:
        logger.error("Error writing EXIF data:%s\n%s", filename, msg)
        return 1
    return 0


def run(argv, callback=None):
    """
    Take an equivalent of sys.argv[1:] and optionally a callable.
    Parse options, personalize files and optionally call the callable
    on every processed file with 3 arguments: filename, newname, percentage.
    If the callable returns True, stop the processing.
    """
    parser = optparse.OptionParser(usage="usage: %prog [options] "
                                         "[-- -TAGNAME=VALUE [...]] "
                                         "<files or dirs>")
    parser.description = ("Hint: %prog is able to set or unset any tags "
                          "supported in ExifTool with -TAGNAME=[VALUE] "
                          "syntax.")
    parser.add_option("--section", "-s", dest="section",
                      help="Name of a config file section to be read. This is"
                           " useful if different people are using the same"
                           " camera model. By default, the section name is"
                           " guessed from the camera model. Section 'all' is"
                           " the default.")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="Be verbose.")
    options, args = parser.parse_args(argv)

    logging.basicConfig(format="%(module)s: %(message)s")
    if options.verbose:
        logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger("exiperson")

    exifconfig = configfile.parse("exif")

    defaultpersonals = []
    options_section_personals = []
    if exifconfig.has_section("all"):
        defaultpersonals += exifconfig.items("all")

    if options.section:
        if exifconfig.has_section(options.section):
            options_section_personals += exifconfig.items(options.section)
        else:
            logger.error("ERROR: Section %s not found in config files",
                         options.section)
            sys.exit(1)

    # collect EXIF data supplied on command line
    forced_personals = {}
    remaining_args = []
    for arg in args:
        if arg.startswith("-") and "=" in arg:
            forced_personals.update(dict((arg.lstrip("-").split("="),)))
        else:
            remaining_args.append(arg)

    for filename, percentage in filelist.Filelist(remaining_args):
        logger.info("%3s%% %s", percentage, filename)
        if callable(callback):
            if callback(filename, filename, percentage):
                break
        # Note to programmer:
        # The [:] is needed to get a slice copy instead of a reference.
        personalize_file(filename, defaultpersonals[:],
                         options_section_personals[:], forced_personals)


if __name__ == "__main__":
    run(sys.argv[1:])
