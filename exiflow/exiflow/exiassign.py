#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
Find groups of derived images and exchange EXIF information between them.

Example:
 These files are a raw image, a low quality version and two edited versions:
 20050914-n001235-jd000.nef
 20050914-n001235-jd00l.jpg
 20050914-n001235-jd100.jpg
 20050914-n001235-jd110.jpg
 The last one doesn't have EXIF informations. This tool will find that out and
 look at 20050914-n001235-jd100.jpg and 20050914-n001235-jd000.nef in this
 order to copy the EXIF header from.
"""
__revision__ = "$Id$"

import os
import re
import sys
import glob
import logging
import optparse
from . import exif
from . import filelist


def find_siblings(filename, prefix):
    """
    Try to find siblings for "filename" in the same directory and return them
    as a list of files reverse sorted by modification time.
    Return [] if no sibling is found.
    A file is considered a sibling if it's basename starts with "prefix".
    """
    mtimes = {}
    for otherfile in glob.glob(os.path.join(os.path.dirname(filename),
                                            prefix + "*")):
        extension = os.path.splitext(otherfile)[1]
        extension = extension.lower()

        if otherfile == filename:
            continue
        elif extension in (".ufraw", ".xmp"):
            continue
        else:
            mtimes[str(os.stat(otherfile).st_mtime) + otherfile] = otherfile
    return [mtimes[mtime] for mtime in sorted(mtimes, reverse=True)]


def assign_file(filename, prefix, force=False):
    """
    Process "filename", passing "prefix" to find_siblings().
    With force=True, force update even if EXIF is already present.
    """
    logger = logging.getLogger("exiassign.assign_file")
    exif_file = exif.Exif(filename)
    try:
        exif_file.read_exif()
    except IOError, msg:
        logger.warning(str(msg))
        return 1
    # Currently F-spot always tries to write "DateTimeOriginal", so we must
    # change the key to detect files with valid exif information.
    #if not force and exif_file.fields.has_key("DateTimeOriginal"):
    if not force and "Model" in exif_file.fields:
        logger.info("Skipping %s, it seems to contain EXIF data.", filename)
        return 0
    for sibling in find_siblings(filename, prefix):
        other_exif_file = exif.Exif(sibling)
        try:
            other_exif_file.read_exif()
        except IOError:
            continue
        other_exif_file.fields.update(exif_file.fields)
        if other_exif_file.fields != exif_file.fields:
            logger.info("Updating %s from %s.", filename, sibling)
            exif_file.update_exif(sibling)
            return 0
    logger.info("No sibling found for %s.", filename)
    return 0


def run(argv, callback=None):
    """
    Take an equivalent of sys.argv[1:] and optionally a callable.
    Parse options, assign relating files and gate meta information between
    them, and optionally call the callable on every processed file with
    3 arguments:
    filename, newname, percentage.
    If the callable returns True, stop the processing.
    """
    parser = optparse.OptionParser(usage="usage: %prog [options] "
                                         "<files or dirs>")
    parser.add_option("-f", "--force", action="store_true", dest="force",
                      help="Force update even if EXIF is already present. "
                           "The fields handled by these scripts are kept "
                           "anyway.")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="Be verbose.")
    options, args = parser.parse_args(argv)

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    logging.basicConfig(format="%(module)s: %(message)s")
    if options.verbose:
        logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger("exiassign")

    filename_re = re.compile("^(\\d{8}(-\\d{6})?-.{3}\\d{4}-)(.{5})\\.[^.]*$")

    for filename, percentage in filelist.Filelist(args):
        mymatch = filename_re.match(os.path.basename(filename))
        if mymatch:
            logger.info("%3s%% %s", percentage, filename)
            prefix = mymatch.groups()[0]
            assign_file(filename, prefix, options.force)
            if callable(callback):
                if callback(filename, filename, percentage):
                    break


if __name__ == "__main__":
    run(sys.argv[1:])
