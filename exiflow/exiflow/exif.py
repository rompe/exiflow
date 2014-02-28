#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
A module for reading and writing EXIF information.
"""
__revision__ = "$Id$"

import re
import locale
import logging
import subprocess


class Exif(object):
    """
    A class for reading and writing EXIF information.
    """

    def __init__(self, filename):
        """
        Create an Exif object for filename.
        """
        self.filename = filename
        self.fields = {}

    def read_exif(self):
        """
        Read EXIF information from self.filename into self.fields
        Raises IOError on errors.
        """
        exiftool = subprocess.Popen(["exiftool", "-d", "%s", "-S",
                                     self.filename],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        stdout, stderr = exiftool.communicate()
        # exiftool doesn't necessarily use stderr on errors...
        for line in stdout.splitlines():
            if line.startswith("Error:"):
                stderr += line
        if len(stderr) > 0:
            raise IOError(stderr)
        else:
            for line in stdout.splitlines():
                if ": " in line:
                    key, value = line.split(": ", 1)
                    self.fields[key] = value.strip()
            # We have to read the ImageDescription binary because it may
            # contain things like line breaks.
            self.fields["ImageDescription"] = \
                "".join(subprocess.Popen(["exiftool", "-b",
                                          "-ImageDescription",
                                          self.filename],
                                         stdout=subprocess.PIPE).stdout)
            # We don't need an empty "ImageDescription" for any merge
            # operations.
            if self.fields["ImageDescription"] == "":
                del self.fields["ImageDescription"]
        # Be sure to have proper UTF8 strings
        for key in self.fields:
            self.fields[key] = self._decode(self.fields[key])

    @staticmethod
    def _decode(field):
        """
        Decode string "field" by trying these encodings:

        UTF-8, Current locale, Latin1

        If none of these succeeds, just despair and return "???".
        """
        encodings = ['utf-8']
        #
        # next we add anything we can learn from the locale
        try:
            encodings.append(locale.nl_langinfo(locale.CODESET))
        except AttributeError:
            pass
        try:
            encodings.append(locale.getlocale()[1])
        except (AttributeError, IndexError):
            pass
        try:
            encodings.append(locale.getdefaultlocale()[1])
        except (AttributeError, IndexError):
            pass
        #
        # we try 'latin-1' last
        encodings.append('latin-1')
        for enc in encodings:
            # some of the locale calls
            # may have returned None
            if not enc:
                continue
            try:
                decoded = unicode(field, enc)
            except (UnicodeError, LookupError):
                decoded = unicode("???", "utf-8")
            else:
                break

        return decoded

    def write_exif(self):
        """
        Write Exif Information from self.fields into self.filename.
        Raises IOError on errors.
        """
        logger = logging.getLogger("exif.write_exif")
        command = ["exiftool", "-overwrite_original", "-P"]
        for field in self.fields.keys():
            if field == "Keywords":
                for keyword in self.fields[field].split(","):
                    command.append("-%s=%s" % (field, keyword.strip()))
            elif field == "DateTimeOriginal":
                # TODO: Writing back DateTimeOriginal seems to be a bad idea
                # since gthumb drops seconds and there is some confusion with
                # time strings and epoch.
                continue
            else:
                command.append("-%s=%s" % (field, self.fields[field]))
        command.append(self.filename)
        logger.debug("Calling: %s", command)
        exiftool = subprocess.Popen(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        # exiftool doesn't reflect errors in it's return code, so we have to
        # assume an error if something is written to stderr.
        errors = exiftool.stderr.readlines()
        if len(errors) > 0:
            raise IOError("".join(errors + exiftool.stdout.readlines()))
        return exiftool.wait()

    def update_exif(self, sourcefile):
        """
        Copy Exif Information from sourcefile into destfile and merge in values
        from myexif. The fields used for merging have to be defined in
        exiffields.
        Raises IOError on errors.
        """
        logger = logging.getLogger("exif.update_exif")
        # Fields we want to keep
        exiffields = ["Artist", "Credit", "Copyright", "CopyrightNotice",
                      "ImageDescription", "Keywords", "Location",
                      "UserComment", "XPTitle"]
        command = ["exiftool", "-overwrite_original", "-x", "Orientation",
                   "-P", "-TagsFromFile", sourcefile, "--Keywords"]
        for field in exiffields:
            if field in self.fields:
                if field == "Keywords":
                    for keyword in self.fields[field].split(","):
                        command.append("-%s=%s" % (field, keyword.strip()))
                else:
                    command.append("-%s=%s" % (field, self.fields[field]))
        command.append(self.filename)
        logger.debug("Calling: %s", command)
        exiftool = subprocess.Popen(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        # exiftool doesn't reflect errors in it's return code, so we have to
        # assume an error if something is written to stderr but ignore
        # warnings too.
        errors = exiftool.stderr.readlines()
        if len(errors) > 0:
            myregex = re.compile("^Warning: \\[minor\\] .* Fixed.")
            mymatch = myregex.match(errors[0])
            if mymatch:
                logger.info("%s", errors)
            else:
                raise IOError("".join(errors + exiftool.stdout.readlines()))
        return exiftool.wait()
