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
      for path in pathes:
         if os.path.isfile(path):
            self.add_file(path)
         elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
               for basefile in files:
                  self.add_file(os.path.join(root, basefile))
         else:
            raise IOError, path + " is not a regular file or directory."


   def add_file(self, filename):
      """
      Add a filename either to _files or _skippedfiles, depending on
      it's extension and the value of self._process_unknown_types.
      Return True for files to process and False for skipped files.
      """
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
