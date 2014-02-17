#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
Automatically gate image meta information between EXIF
headers and Gthumb comment files.
"""
__revision__ = "$Id$"

import os
import sys
import logging
import optparse
from . import exif
from . import gthumb
from . import filelist


def autogate_gthumb(filename, myoptions):
    """
    Decide if we gate from gthumb to Exif or vice versa by looking at the
    time stamps of the comment and the Exif file.
    Run read and write functions accordingly.
    """
    logger = logging.getLogger("exigate.autogate_gthumb")
    filename = os.path.abspath(filename)
    gthumbfile = gthumb.Gthumb(filename)
    gthumbtimestamp = gthumbfile.get_mtime()
    filetimestamp = os.path.getmtime(filename)
    if gthumbtimestamp > filetimestamp:
        logger.info("Updating %s from comment file.", filename)
        try:
            gthumbfile.read()
        except IOError, msg:
            logger.error("Error reading gthumb comment for %s:\n%s",
                         filename, msg)
            return False
        exif_file = exif.Exif(filename)
        exif_file.fields = gthumbfile.fields
        try:
            exif_file.write_exif()
        except IOError, msg:
            logger.error("Error writing EXIF data to %s:\n%s", filename, msg)
            return False
        # TODO: Find out why we intruduced this line. Seems odd...
        #write_gthumb(filename, gthumb, myoptions.addfields,
        #             myoptions.template)
        # Maybe that way we wanted to update in addfields and template mode
        # even if the file's timestamp is older than the gthumb comment? Check
        # if that is needed and if so, if we can do it conditionally!
        gthumbfile.set_mtime(filetimestamp)
        os.utime(filename, (filetimestamp, filetimestamp))
    elif (filetimestamp > gthumbtimestamp
          or myoptions.addfields
          or myoptions.template):
        logger.info("Updating comment file from %s.", filename)
        exif_file = exif.Exif(filename)
        try:
            exif_file.read_exif()
        except IOError, message:
            logger.info("Skipping %s: %s", filename, message)
            return 1
        gthumbfile.fields = exif_file.fields
        gthumbfile.write(myoptions.addfields, myoptions.template)
        gthumbfile.set_mtime(filetimestamp)
    else:
        logger.info("%s is in sync with comment file.", filename)
    return True


def run(argv, callback=None):
    """
    Take an equivalent of sys.argv[1:] and optionally a callable.
    Parse options, gate meta information and optionally call the callable on
    every processed file with 3 arguments: filename, newname, percentage.
    If the callable returns True, stop the processing.
    """
    parser = optparse.OptionParser(usage="usage: %prog [options] "
                                         "<files or dirs>")
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
    #                  help="Merge data instead of just using the newest "
    #                       "version to overwrite the older one.")
    parser.add_option("--cleanup", "-c", action="store_true", dest="cleanup",
                      help="The opposite of --additional-fields, that is, "
                           "remove additional fields from gthumb comments.")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="Be verbose.")
    options, args = parser.parse_args(argv)

    logging.basicConfig(format="%(module)s: %(message)s")
    if options.verbose:
        logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger("exigate")

    for filename, percentage in filelist.Filelist(args):
        if callable(callback):
            if callback(filename, filename, percentage):
                break
        logger.info("%3s%% %s", percentage, filename)
        autogate_gthumb(filename, options)
        if options.cleanup:
            log_prefix = "Leaving"
            if gthumb.Gthumb(filename).cleanup():
                log_prefix = "Cleaning"
            if options.verbose:
                logger.info("%s comment file of %s.", log_prefix, filename)


if __name__ == "__main__":
    run(sys.argv[1:])
