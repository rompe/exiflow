#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
Rename a bunch of image files according to our holy file naming schema.

Given a camera that saves a file as:

dsc_1234.nef

we will rename that file to:

20050412-n001234-ur000.nef

At first there is 20050412. That's a date, telling us the
photo has been taken on 2005-04-12. This is determined by
looking it up in the image's EXIF information.

Then there is n001234. The "n00" part is read from a config
file as the three byte string to be put there for a given
camera model. In this case, the camera model information in
the EXIF header reads "Nikon D70", and the config section
for that model reads "n00", meaning an "n" as a model
indicator since I also own an HP camera for which I
configured "h00", and the "00" as a way to extend the
counting possibilities beyond 9999 pictures. Once the
camera switches from 9999 to 0000 I will change that string
to "n01". The "1234" part is just the numeric part of the
original filename.

At last there is ur000. "ur" are my initials; I have
simply configured "If it's a Nikon D70, the artist is me".
Of course there are possibilities to override that. The
"000" part is a revision number. This is an original,
untouched file, so it's revision is 000. An automatic
conversion to JPG would also have revision 000 since there
is no interaction and the files are still distinguishable
by their suffixes. Once I convert it with custom parameters
or do some kind of editing, I will save it as revision 100.
Another derivate of the original will get revision 200.
A derivate of revision 100 will get 110, a derivate of 110
will get 111 and another one will get 112. Got the idea?
Using this revision scheme lets you know about the basic
editing history (if there's any) by just looking at the
filename. If this is too complicated for your needs you
are free to use these three bytes in another way or to
leave them alone.

There's one exception regarding the initial "000" revision:
If the software detects the presence of a low quality JPG
accompanying a raw image, the raw file gets revision 000 as
usual, but the low quality file will get revision 00l so
that it can't be confused with an automatically converted
*000.jpg of high quality.
"""

__revision__ = "$Id$"

import os
import re
import sys
import time
import logging
import optparse
from . import exif
from . import filelist
from . import configfile


def get_exif_information(filename):
    """
    Read camera model and date from filename and return them.
    If The date isn't contained in EXIF, use the file's mtime.
    """
    exif_file = exif.Exif(filename)
    # read_exif may throw IOError. We leave the catching to our caller.
    exif_file.read_exif()
    model = exif_file.fields.get("Model", "all")
    date = exif_file.fields.get("DateTimeOriginal", "0")
    quality = exif_file.fields.get("Quality", "0")
    image_time = date
    if ":" in date:
        image_time = image_time[11:13] + image_time[14:16] + image_time[17:19]
        date = date[0:4] + date[5:7] + date[8:10]
    else:
        if date == "0":
            date = os.stat(filename).st_mtime
            image_time = date
        date = time.strftime("%Y%m%d", time.localtime(float(date)))
        image_time = time.strftime("%H%M%S", time.localtime(float(image_time)))
    return model, date, image_time, quality


def get_new_filename_parts(filename, my_filelist, quality):
    """
    Return a new name for filename according to our holy naming scheme.
    """
    leader, extension = os.path.splitext(filename)
    extension = extension.lower()
    number = "".join([char for char in leader[-4:] if char.isdigit()])
    revision = "000"
    # Look for high quality versions of this image. This is the case if we are
    # a .jpg, more than one file exists with the same prefix and the quality is
    # not "fine" or "high".
    if extension == ".jpg":
        versions = [vers[0] for vers in my_filelist
                    if vers[0].startswith(leader)]
        if len(versions) > 1:
            if quality.lower() not in ("fine", "high"):
                revision = "00l"
    if not number:
        raise IOError("Can't find a number in " + filename)
    return number.zfill(4), revision, extension


def rename_file(filename, my_filelist, with_time, cam_id=None,
                artist_initials=None):
    """
    Rename filename and return the newly generated name without dir.
    """
    logger = logging.getLogger("exirename.rename_file")
    match = re.match("^(\\d{8})(-(\\d{6}))?-(.{3})(\\d{4})-"
                     "((.{2})(.{3}))(\\.[^.]*)$",
                     os.path.basename(filename))
    # differentiate between getting values from existing filenames or getting
    # initial values from exif and config file
    if match:
        date = match.group(1)
        image_time = match.group(3)
        if cam_id is None:
            cam_id = match.group(4)
        number = match.group(5)
        if artist_initials is None:
            artist_initials = match.group(7)
        revision = match.group(8)
        extension = match.group(9)
        if with_time:
            if not image_time:
                image_time = get_exif_information(filename)[2]
            date += "-" + image_time
    else:
        model, date, image_time, quality = get_exif_information(filename)
        if with_time:
            date += "-" + image_time
        if cam_id is None or artist_initials is None:
            new_cam_id, new_artist_initials = configfile.get_options(
                "cameras", model, ("cam_id", "artist_initials"))
            cam_id = cam_id or new_cam_id
            artist_initials = artist_initials or new_artist_initials
        number, revision, extension = get_new_filename_parts(filename,
                                                             my_filelist,
                                                             quality)

    if len(cam_id) != 3 or len(artist_initials) != 2:
        logger.warning("Either cam_id or artist_initials is missing or of "
                       "wrong length. cam_id should be 3 characters and is "
                       "currently set to '%s', artist_initials should be 2 "
                       "characters and is set to '%s'. "
                       "Skipping %s.", cam_id, artist_initials, filename)
        return os.path.basename(filename)

    newbasename = (date + "-" + cam_id + number + "-" + artist_initials +
                   revision + extension)
    newname = os.path.join(os.path.dirname(filename), newbasename)
    if filename == newname:
        raise IOError("Filename does not change.")
    elif os.path.exists(newname):
        raise IOError("Can't rename %s to %s, it already exists." % (filename,
                                                                     newname))
    os.rename(filename, newname)
    return newbasename


def run(argv, callback=None):
    """
    Take an equivalent of sys.argv[1:] and optionally a callable.
    Parse options, rename files and optionally call the callable on every
    processed file with 3 arguments: filename, newname, percentage.
    If the callable returns True, stop the processing.
    """
    parser = optparse.OptionParser(usage="usage: %prog [options] "
                                         "<files or dirs>")
    parser.add_option("--cam_id", "-c", dest="cam_id",
                      help="ID string for the camera model. Should normally be"
                           " three characters long.")
    parser.add_option("--artist_initials", "-a", dest="artist_initials",
                      help="Initials of the artist. Should be two characters"
                           " long.")
    parser.add_option("-t", "--with_time", action="store_true",
                      dest="with_time",
                      help="Create filenames containing the image time, for "
                           "example 20071231-235959-n001234-xy000.jpg instead "
                           "of 20071231-n001234-xy000.jpg .")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="Be verbose.")
    options, args = parser.parse_args(args=argv)

    logging.basicConfig(format="%(module)s: %(message)s")
    if options.verbose:
        logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger("exirename")

    my_filelist = filelist.Filelist(args)
    for filename, percentage in my_filelist:
        try:
            newname = rename_file(filename, my_filelist, options.with_time,
                                  options.cam_id, options.artist_initials)
        except IOError, msg:
            newname = os.path.basename(filename)
            logger.error("Skipping %s:\n %s", filename, str(msg))
        logger.info("%3s%% %s -> %s", percentage, filename, newname)
        if callable(callback):
            if callback(filename,
                        os.path.join(os.path.dirname(filename), newname),
                        percentage):
                break


if __name__ == "__main__":
    run(sys.argv[1:])
