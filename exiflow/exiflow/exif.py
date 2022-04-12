#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""A module for reading and writing EXIF information."""
__revision__ = "$Id$"

import re
import logging
import subprocess
from typing import Dict


class Exif(object):
    """A class for reading and writing EXIF information."""

    def __init__(self, filename: str):
        """Create an Exif object for filename."""
        self.filename = filename
        self.fields: Dict[str, str] = {}

    def read_exif(self) -> None:
        """
        Read EXIF information from self.filename into self.fields.

        Raises IOError on errors.
        """
        with subprocess.Popen(["exiftool", "-d", "%s", "-S",
                               self.filename],
                              universal_newlines=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as exiftool:
            stdout, stderr = exiftool.communicate()
        # exiftool doesn't necessarily use stderr on errors...
        for line in stdout.splitlines():
            if line.startswith("Error:"):
                stderr += line
        if len(stderr) > 0:
            raise IOError(stderr)
        for line in stdout.splitlines():
            if ": " in line:
                key, value = line.split(": ", 1)
                self.fields[key] = value.strip()
        # We have to read the ImageDescription binary because it may
        # contain things like line breaks.
        with subprocess.Popen(["exiftool", "-b",
                               "-ImageDescription",
                               self.filename],
                              universal_newlines=True,
                              stdout=subprocess.PIPE) as exiftool:
            self.fields["ImageDescription"] = exiftool.communicate()[0]
        # We don't need an empty "ImageDescription" for any merge
        # operations.
        if self.fields["ImageDescription"] == "":
            del self.fields["ImageDescription"]

    def write_exif(self) -> int:
        """
        Write Exif Information from self.fields into self.filename.

        Raises IOError on errors.
        """
        logger = logging.getLogger("exif.write_exif")
        command = ["exiftool", "-overwrite_original", "-P"]
        for field, value in self.fields.items():
            if field == "Keywords":
                for keyword in value.split(","):
                    command.append(f"-{field}={keyword.strip()}")
            elif field == "DateTimeOriginal":
                # TODO: Writing back DateTimeOriginal seems to be a bad idea
                # since gthumb drops seconds and there is some confusion with
                # time strings and epoch.
                continue
            else:
                command.append(f"-{field}={self.fields[field]}")
        command.append(self.filename)
        logger.debug("Calling: %s", command)
        with subprocess.Popen(command, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True) as exiftool:
            stdout, stderr = exiftool.communicate()
            result = exiftool.wait()
        # exiftool doesn't reflect errors in it's return code, so we have
        # to assume an error if something is written to stderr.
        if len(stderr) > 0:
            raise IOError(stderr + stdout)
        return result

    def update_exif(self, sourcefile: str) -> int:
        """
        Copy Exif info from sourcefile to destfile, merge values from myexif.

        The fields used for merging have to be defined in exiffields.
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
                        command.append(f"-{field}={keyword.strip()}")
                else:
                    command.append(f"-{field}={self.fields[field]}")
        command.append(self.filename)
        logger.debug("Calling: %s", command)
        with subprocess.Popen(command, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True) as exiftool:
            stdout, stderr = exiftool.communicate()
            result = exiftool.wait()
        # exiftool doesn't reflect errors in it's return code, so we have to
        # assume an error if something is written to stderr but ignore
        # warnings too.
        if len(stderr) > 0:
            myregex = re.compile("^Warning: \\[minor\\] .* Fixed.")
            mymatch = myregex.match(stderr.splitlines()[0])
            if mymatch:
                logger.info(stderr)
            else:
                raise IOError(stderr + stdout)
        return result
