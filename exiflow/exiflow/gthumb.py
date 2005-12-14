#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
"""
A class that handles reading and writing gthumb comment files for an image file.
"""

import os
import re
import sys
import gzip
import xml.dom.minidom

class Gthumb:

   def __init__(self, filename):
      """
      Create a Gthumb object for image filename.
      """
      self.fields = {}
      self.filename = os.path.abspath(filename)
      self.commentsdir = os.path.join(os.path.dirname(self.filename),
                                      ".comments")
      self.commentsfile = os.path.join(commentsdir,
                                       os.path.basename(self.filename) + ".xml")


   def read():
      """
      Read gthumb comment information for filename and return a dictionary
      containing the corresponding EXIF values.
      Translation of Exif values to gthumb sections:

          "Artist"            => "Note" line: "^Artist::.*"
          "Credit"            => "Note" line: "^Credit::.*"
          "Copyright"         => "Note" line: "^Copyright::.*"
          "CopyrightNotice"   => "Note" line: "^CopyrightNotice::.*"
          "UserComment"       => "Note" line: "^UserComment::.*"
          "ImageDescription"  => "Note" free text without "^\w+::"
          "Keywords"          => "Keywords" comma separated list
          "Location"          => "Place"
          "DateTimeOriginal"  => "Time" in seconds since 1970-01-01
          "XPTitle"           => First line of "Note", if any

      In fact, any line of "Note" that consists of a keyword followed by
      two colons and some random text is converted into it's EXIF equivalent.
      """
      if os.path.isfile(self.commentsfile):
         mydata = {}
         mydom = xml.dom.minidom.parse(gzip.open(myxmlfile))
         for field in ("Note", "Keywords", "Place", "Time"):
            mynodes = mydom.getElementsByTagName(field)
            if len(mynodes) > 0:
               mynodes = mynodes[0].childNodes
               if len(mynodes) > 0:
                  mydata[field] = mynodes[0].wholeText

         if "Time" in mydata:
            self.fields["DateTimeOriginal"] = mydata["Time"]
         if "Place" in mydata:
            self.fields["Location"] = mydata["Place"]
         if "Keywords" in mydata:
            self.fields["Keywords"] = mydata["Keywords"]
         if "Note" in mydata:
            note = []
            myregex = re.compile("(\w+)::(.+)$")
            for line in mydata["Note"].split("\n"):
               mymatch = myregex.match(line)
               if mymatch:
                  self.fields[mymatch.group(1)] = mymatch.group(2).strip()
               else:
                  note.append(line)
            if len(note) > 0:
               self.fields["XPTitle"] = note[0]
               self.fields["ImageDescription"] = "\n".join(note).strip()
         return True
      else:
         return False


