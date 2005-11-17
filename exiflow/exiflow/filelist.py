#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
An (iterable!) class that hosts information about files given in it's contructor.
"""

import os
import time

class Filelist:

   knownextensions = (".jpg", ".nef", ".raw", ".crw", ".tif")

   def __init__(self, process_unknown_types=False, *pathes):
      """
      Create FileList object and set _process_unknown_types to given value.
      Call add_files() with all remaining arguments.
      If process_unknown_types is given, then no files will be skipped.
      """
      self._files = []
      self._skippedfiles = []
      self._filedates = {}
      self._filestats = {}
      self._fullsize = 0
      self._process_unknown_types = process_unknown_types
      self.add_files(pathes)


   def add_files(self, pathes):
      """
      Add filenames found in pathes either to _files or _skippedfiles,
      depending on their extension and the value of _process_unknown_types.
      Return False if files are skipped or no files are processed,
      True otherwise.
      Raises IOError on access errors.
      """
      found_known = False
      found_unknown = False
      filelist = []
      for path in pathes:
         print "path:", path
         if os.path.isfile(path):
            filelist.append(path)
         elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
               for basefile in files:
                  filelist.append(os.path.join(root, basefile))
         else:
            raise IOError, path + " is not a regular file or directory."
      for filename in filelist:
         if self._process_unknown_types == True or \
            os.path.splitext(filename)[1] in self.knownextensions:
            found_known = True
            self._files.append(filename)
            filestat = os.stat(filename)
            self._filestats[filename] = filestat
            self._fullsize += filestat.st_size
            filedate = time.strftime("%Y-%m-%d", time.localtime(filestat.st_mtime))
            self._filedates[filename] = filedate
         else:
            found_unknown = True
            self._skippedfiles.append(filename)
      return found_known and not found_unknown


   def __iter__(self):
      """
      Iterate through filelist and update percentage.
      Returns (filename, percentage) pairs on each iteration.
      """
      size_so_far = 0
      for filename in self._files:
         size_so_far += self._filestats[filename].st_size
         yield(filename, 100 * size_so_far / self._fullsize)


   def get_daterange(self):
      """
      Get the date range of the files as a string in the form
      YYYY-MM-DD_-_YYYY-MM-DD   or  YYYY-MM-DD  if only one date available.
      """
      dates = sorted(set(self._filedates.values()))
      range_string = dates[0]
      if len(dates) > 1:
         range_string += "_-_" + dates.pop()
      return range_string


   def get_date(self, filename):
      """
      Get modification date for filename.
      """
      return self._filedates[filename]


   def get_fullsize(self):
      """
      Get cumulated bytes of files.
      """
      return self._fullsize


   def get_filecount(self):
      """
      Get number of files.
      """
      return len(self._files)

