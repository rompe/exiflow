#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
Generate lists of files given as names or searched in directories.

Provide an iterable interface to them.
"""
__revision__ = "$Id$"

import os
import time
import logging
from typing import Dict, Iterable, List
from . import configfile


class Filelist(object):
    """An iterable class that hosts information about files."""

    def __init__(self, pathes: Iterable[str]):
        """
        Create FileList object.

        Call add_files() with all arguments.
        If process_unknown_types is given, then no files will be skipped.
        """
        self._files: List[str] = []
        self._skippedfiles: List[str] = []
        self._filedates: Dict[str, str] = {}
        self._filestats: Dict[str, os.stat_result] = {}
        self._fullsize = 0
        self._process_unknown_types = False
        for path in pathes:
            self.add_files([path])

    def add_files(self, pathes: Iterable[str]) -> bool:
        """
        Add filenames found in pathes either to _files or _skippedfiles.

        (Depending on their extension and the value of _process_unknown_types.)
        Return False if files are skipped or no files are processed,
        True otherwise.
        Raises IOError on access errors.
        """
        logger = logging.getLogger("filelist.add_files")
        settings = configfile.parse("settings")
        unwanted_dirs = settings.get("all", "unwantend_dirs").split()
        for path in pathes:
            if path.startswith("file:///"):
                path = path[7:]
            if os.path.isfile(path):
                self._add_file(path)
            elif os.path.isdir(path):
                for root, dirs, files in os.walk(path, True):
                    for unwanted_dir in unwanted_dirs:
                        if unwanted_dir in dirs:
                            logger.info("Skipping unwanted dir %s.",
                                        os.path.join(root, unwanted_dir))
                            dirs.remove(unwanted_dir)
                    for basefile in files:
                        self._add_file(os.path.join(root, basefile))
            else:
                logger.warning("%s is not a regular file or directory. "
                               "Skipping.", path)
        return bool(self._files and not self._skippedfiles)

    def _add_file(self, filename: str) -> bool:
        """
        Add filename and all it's data to the filelist.

        Return True if the file is added, False otherwise.
        """
        logger = logging.getLogger("filelist._add_file")
        settings = configfile.parse("settings")
        image_extensions = settings.get("all", "image_extensions").split()
        unwanted_files = settings.get("all", "unwantend_files").split()
        basefilename = os.path.basename(filename).lower()
        if ((self._process_unknown_types
             or os.path.splitext(basefilename)[1] in image_extensions)
                and basefilename not in unwanted_files):
            self._files.append(filename)
            filestat = os.stat(filename)
            self._filestats[filename] = filestat
            self._fullsize += filestat.st_size
            self._filedates[filename] = \
                time.strftime("%Y-%m-%d", time.localtime(filestat.st_mtime))
            return True
        logger.info("Skipping %s.", filename)
        self._skippedfiles.append(filename)
        return False

    def process_unknown_types(self) -> None:
        """
        Set _process_unknown_types to True.

        This means that following method calls should work on every file except
        those listed in "unwanted_files" in the config file. Typical usage will
        be to call the constructor without arguments, then call this method,
        and then call add_files().
        """
        self._process_unknown_types = True

    def __iter__(self):
        """
        Iterate through filelist and update percentage.

        Yield (filename, percentage) pairs on each iteration.
        """
        size_so_far = 0
        for filename in self._files:
            size_so_far += self._filestats[filename].st_size
            yield(filename, 100 * size_so_far / self._fullsize)

    def get_daterange(self) -> str:
        """
        Get the date range of the files as a string.

        The strings has the form  YYYY-MM-DD_-_YYYY-MM-DD
        or  YYYY-MM-DD  if only one date available.
        """
        dates = sorted(set(self._filedates.values()))
        range_string = dates[0]
        if len(dates) > 1:
            range_string += "_-_" + dates.pop()
        return range_string

    def get_date(self, filename: str) -> str:
        """Get modification date for filename."""
        return self._filedates[filename]

    def get_fullsize(self):
        """Get cumulated bytes of files."""
        return self._fullsize

    def get_filecount(self):
        """Get number of files."""
        return len(self._files)

    def get_files(self):
        """Get al list of all files."""
        return self._files
