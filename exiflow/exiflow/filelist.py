#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
A class that hosts information about files given in it's contructor.
"""

import os

class Filelist:

   knownextensions = (".jpg", ".nef", ".raw", ".crw", ".tif")

   def __init__(self, process_unknown_types=False, *pathes)
      """
      Walk through directories and files given as arguments and call
      add_file() for all found files.
      If process_unknown_types is given, then no files will be skipped.
      Raises IOError on access errors.
      """
      self._files = []
      self._skippedfiles = []
      self._filedates = {}
      self._filestats = {}
      self._fullsize = 0
      self._process_unknown_types = process_unknown_types
      self.add_files(pathes)


   def add_files(self, *pathes):
      """
      Add filenames found in *pathes either to _files or _skippedfiles,
      depending on their extension and the value of _process_unknown_types.
      Return False if files are skipped or no files are processed,
      True otherwise.
      """
      for path in pathes:
         if os.path.isfile(path):
            self.add_file(path)
         elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
               for basefile in files:
                  self.add_file(os.path.join(root, basefile))
         else:
            raise IOError, path + " is not a regular file or directory."
      if self._process_unknown_types == True or \
         os.path.splitext(filename)[1] in self.knownextensions:
         self._files.append(filename)
         filestat = os.stat(filename)
         self._filestats[filename] = filestat
         self._fullsize += filestat.st_size
         filedate = time.strftime("%Y-%m-%d", time.localtime(filestat.st_mtime))
         self._filedates[filename] = filedate
         return True
      else:
         self._skippedfiles.append(filename)
         return False


   def __iter__(self):
      """
      Iterate through filelist and update percentage.
      Returns (filename, percentage) pairs on each iteration.
      """
      size_so_far = 0
      for filename in self._files:
         size_so_far += self.filestats[filename].st_size
         yield(filename, 100 / self._fullsize * size_so_far)


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


