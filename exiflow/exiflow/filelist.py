#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
An (iterable!) class that hosts information about files given in it's contructor.
"""

import os
import sys
import time
import exiflow.configfile

class Filelist:

   def __init__(self, *pathes):
      """
      Create FileList object.
      Call add_files() with all arguments.
      If process_unknown_types is given, then no files will be skipped.
      """
      self._files = []
      self._skippedfiles = []
      self._filedates = {}
      self._filestats = {}
      self._fullsize = 0
      self._process_unknown_types = False
      settings = exiflow.configfile.parse("settings")
      self._image_extensions = settings.get("all", "image_extensions").split()
      self._unwanted_files = settings.get("all", "unwantend_files").split()
      self._unwanted_dirs = settings.get("all", "unwantend_dirs").split()
      for path in pathes:
         self.add_files(path)


   def add_files(self, *pathes):
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
         if os.path.isfile(path):
            filelist.append(path)
         elif os.path.isdir(path):
            for root, dirs, files in os.walk(path, True):
               for unwanted_dir in self._unwanted_dirs:
                  if unwanted_dir in dirs:
                     dirs.remove(unwanted_dir)
               for basefile in files:
                  filelist.append(os.path.join(root, basefile))
         else:
            print >> sys.stderr, "WARNING: " + path + \
                  " is not a regular file or directory. Skipping."
      for filename in filelist:
         basefilename = os.path.basename(filename).lower()
         if (self._process_unknown_types == True or \
             os.path.splitext(basefilename)[1] in self._image_extensions) and \
            not basefilename in self._unwanted_files:
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


   def process_unknown_types(self):
      """
      Set _process_unknown_types to True, meaning that following method calls
      should work on every file except those listed in "unwanted_files" in
      the config file. Typical usage will be to call the constructor without
      arguments, then call this method, and then call add_files().
      """
      self._process_unknown_types = True


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

