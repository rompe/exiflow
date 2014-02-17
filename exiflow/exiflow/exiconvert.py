#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
Convert any RAW images into JPEG images.

The raw file extensions as well as the converters to call
are read from the config file "cameras.cfg" using the keys
"raw_extension" and "raw_converter". As alway, the [all]
section may contain general defaults used for all cameras
and camera specific sections may contain values for a given
camera model.

An example section would look like this:

[NIKON D70]
raw_extension = .nef
raw_converter = ufraw-batch --clip --out-type=jpeg

Given this, any files produced by a Nikon D70 that end in
".nef" are converted using this artificial ufraw call.

The raw converter is expected to write a file of the same
prefix as the input file with an extension of ".jpg".
For example, a file "test.nef" should result in "test.jpg".
"""

__revision__ = "$Id$"

import os
import re
import sys
import logging
import optparse
import subprocess
from . import exif
from . import filelist
from . import configfile


def convert_file(filename):
    """
    Convert filename and return the newly generated name without dir.
    """
    logger = logging.getLogger("exiconvert.convert_file")
    basename = os.path.basename(filename)
    # Sanity check - no sense in trying to convert jpeg to jpeg
    if basename.lower().endswith(".jpg"):
        logger.debug("%s is a Jpeg file, skipping.", basename)
        return basename

    exif_file = exif.Exif(filename)
    # read_exif may throw IOError. We leave the catching to our caller.
    exif_file.read_exif()
    model = exif_file.fields.get("Model", "all")

    raw_extension, raw_converter = \
        configfile.get_options("cameras", model,
                               ("raw_extension", "raw_converter"))

    if raw_extension == "":
        logger.warning("No raw_extension configured, skipping %s", basename)
        return basename

    if not filename.endswith(raw_extension):
        logger.info("%s doesn't match, skipping.", filename)
        return basename

    if raw_converter == "":
        logger.warning("No raw_converter configured, skipping %s", basename)
        return basename

    newname = os.path.splitext(filename)[0] + ".jpg"
    if os.path.exists(newname):
        logger.info("%s already exists, skipping %s.", newname, basename)
    else:
        command = raw_converter + " " + filename
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        for line in process.stderr:
            logger.warning(line)
        for line in process.stdout:
            logger.info(line)
        if process.wait() > 0:
            logger.error("Converter invocation returned an error:\n%s",
                         command)
        else:
            if not os.path.exists(newname):
                logger.error("Converter returned 0, but %s is absent!",
                             newname)
            else:
                return os.path.basename(newname)
    return basename


def run(argv, callback=None):
    """
    Take an equivalent of sys.argv[1:] and optionally a callable.
    Parse options, convert convertible files and optionally call the callable
    on every processed file with 4 arguments: filename, newname, percentage,
    keep_original=true. The latter option means "The new file is an addition,
    not a replacement". If the callable returns True, stop the processing.
    """
    parser = optparse.OptionParser(usage="usage: %prog [options] "
                                         "<files or dirs>")
    parser.add_option("-r", "--remove-lqjpeg", action="store_true",
                      dest="remove_lqjpeg",
                      help="removes the low quality jpeg (...00l.jpg) "
                            "example yyyymmdd-a00000-xy00l.jpg")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="Be verbose.")
    options, args = parser.parse_args(args=argv)

    logging.basicConfig(format="%(module)s: %(message)s")
    if options.verbose:
        logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger("exiconvert")

    filename_re = re.compile("^(\\d{8}(-\\d{6})?-.{3}\\d{4}-.{2})000\\.jpg$")
    for filename, percentage in filelist.Filelist(args):
        callback_filename = None
        logger.info("%3s%% %s", percentage, filename)
        if callable(callback):
            if callback(filename, filename, percentage):
                break
        try:
            newname = convert_file(filename)
        except IOError, msg:
            newname = os.path.basename(filename)
            logger.error("Skipping %s:\n%s\n", filename, msg)
        if options.remove_lqjpeg:
            keep_original = False
            mymatch = filename_re.match(newname)
            if mymatch:
                lqname = os.path.join(os.path.dirname(filename),
                                      mymatch.group(1) + "00l.jpg")
                if os.path.exists(lqname):
                    try:
                        os.remove(lqname)
                        callback_filename = lqname
                    except IOError, msg:
                        logger.error("Skipping remove of %s:\n%s\n",
                                     lqname, msg)
        else:
            callback_filename = filename
            keep_original = True

        if callback_filename is not None and callable(callback):
            if callback(callback_filename,
                        os.path.join(os.path.dirname(filename), newname),
                        percentage, keep_original=keep_original):
                break


if __name__ == "__main__":
    run(sys.argv[1:])
