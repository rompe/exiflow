#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
import optparse
import subprocess
import os
import sys
import gzip
import xml.dom.minidom
import re
import exiflow.exif


def read_gthumb(filename):
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
   myexif = {}
   filename = os.path.abspath(filename)
   myxmlfile = os.path.join(os.path.dirname(filename),
                            ".comments",
                            os.path.basename(filename) + ".xml")
   if os.path.isfile(myxmlfile):
      mydata = {}
      mydom = xml.dom.minidom.parse(gzip.open(myxmlfile))
      for field in ("Note", "Keywords", "Place", "Time"):
         mynodes = mydom.getElementsByTagName(field)
         if len(mynodes) > 0:
            mynodes = mynodes[0].childNodes
            if len(mynodes) > 0:
               mydata[field] = mynodes[0].wholeText

      if "Time" in mydata:
         myexif["DateTimeOriginal"] = mydata["Time"]
      if "Place" in mydata:
         myexif["Location"] = mydata["Place"]
      if "Keywords" in mydata:
         myexif["Keywords"] = mydata["Keywords"]
      if "Note" in mydata:
         note = []
         myregex = re.compile("(\w+)::(.+)$")
         for line in mydata["Note"].split("\n"):
            mymatch = myregex.match(line)
            if mymatch:
               myexif[mymatch.group(1)] = mymatch.group(2).strip()
            else:
               note.append(line)
         if len(note) > 0:
            myexif["XPTitle"] = note[0]
            myexif["ImageDescription"] = "\n".join(note).strip()
   return myexif


def write_gthumb(filename, myexif, myaddfields, mytemplate):
   """
   Write Exif information from myexif into gthumb comment file.
   Apply reverse mapping of read_gthumb().
   """
   exiffields = ["Artist", "Credit", "Copyright", "CopyrightNotice", "UserComment"]
   filename = os.path.abspath(filename)
   commentsdir = os.path.join(os.path.dirname(filename), ".comments")
   myxmlfile = os.path.join(commentsdir, os.path.basename(filename) + ".xml")
   mydata = {}
   mydata["Place"] = myexif.get("Location", "")
   mydata["Time"] = myexif.get("DateTimeOriginal", "")
   mydata["Note"] = myexif.get("ImageDescription", "")
   tmpkeywords = []
   for keyword in myexif.get("Keywords", "").split(","):
      tmpkeywords.append(keyword.strip())
   mydata["Keywords"] = ",".join(tmpkeywords)

# Add XPTitle to Note if Note doesn't contain it already
   mytitle = myexif.get("XPTitle", "")
   if len(mytitle) > 0 and not mytitle in mydata["Note"].splitlines():
      mydata["Note"] = myexif["XPTitle"] + "\n" + mydata["Note"]
   if myaddfields or mytemplate:
      mydata["Note"] += "\n"
      for field in exiffields:
         fieldvalue = myexif.get(field, "")
         if mytemplate or len(fieldvalue) > 0:
            mydata["Note"] += "\n" + field + ":: " + fieldvalue

   mydom = xml.dom.minidom.Document()
   comment = mydom.createElement("Comment")
   comment.setAttribute("format", "2.0")
   mydom.appendChild(comment)

   for name in ("Place", "Time", "Note", "Keywords"):
      element = mydom.createElement(name)
      text = mydom.createTextNode(mydata[name])
      element.appendChild(text)
      comment.appendChild(element)

   if not os.path.isdir(commentsdir):
      os.makedirs(commentsdir)
   gzip.open(myxmlfile, "wb").write(mydom.toxml(encoding="utf-8"))

   
def autogate_gthumb(filename, myoptions):
   """
   Decide if we gate from gthumb to Exif or vice versa by looking at the
   time stamps of the comment and the Exif file.
   Run read and write functions accordingly.
   """
   filename = os.path.abspath(filename)
   myxmlfile = os.path.join(os.path.dirname(filename),
                            ".comments",
                            os.path.basename(filename) + ".xml")
   filetimestamp = os.path.getmtime(filename)
   if os.path.isfile(myxmlfile):
      xmltimestamp = os.path.getmtime(myxmlfile)
   else:
      xmltimestamp = 0
   if xmltimestamp > filetimestamp:
      if myoptions.verbose:
         print "Updating", filename, "from comment file"
      try:
         gthumb = read_gthumb(filename)
      except IOError, msg:
         print "Error reading gthumb comment:\n", myxmlfile, "\n", msg
         return False
      exif_file = exiflow.exif.Exif(filename)
      exif_file.fields = gthumb
      try:
         exif_file.write_exif()
      except IOError, msg:
         print "Error writing EXIF data:\n", filename, "\n", msg
         return False
# TODO: Find out why we intruduced this line. Seems odd...
      #write_gthumb(filename, gthumb, myoptions.addfields,
      #             myoptions.template)
      os.utime(myxmlfile, (filetimestamp, filetimestamp))
      os.utime(filename, (filetimestamp, filetimestamp))
   elif filetimestamp > xmltimestamp or myoptions.template:
      if myoptions.verbose:
         print "Updating comment file from", filename
      exif_file = exiflow.exif.Exif(filename)
      try:
         exif_file.read_exif()
      except IOError, message:
         if myoptions.verbose:
            print "Skipping %s: %s" % (filename, message)
         return 1
      write_gthumb(filename, exif_file.fields, myoptions.addfields, myoptions.template)
      os.utime(myxmlfile, (filetimestamp, filetimestamp))
   else:
      if myoptions.verbose:
         print filename, "is in sync with comment file"
   return True




def run(argv):
   parser = optparse.OptionParser(usage="usage: %prog [options] <files or dirs>")
   parser.add_option("--gthumb", action="store_true", dest="gthumb",
                     help="Gateway to/from gthumb comment files." \
                          "This is the default.")
   parser.add_option("--additional-fields", "-a", action="store_true",
                     dest="addfields",
                     help="When gating from Exif to gthumb, combine additional" \
                          "Exif fields into the comment.")
   parser.add_option("--template", "-t", action="store_true", dest="template",
                     help="Like --additional-fields, but also combine empty" \
                          "fields as templates into the comment.")
# TODO: 
#parser.add_option("--merge", action="store_true", dest="merge",
#                  help="Merge data instead of just using the newest version "\
#                       "to overwrite the older one.")
#parser.add_option("--cleanup", action="store_true", dest="cleanup",
#                  help="The opposite of --additional-fields, that is, remove" \
#                       "additional fields from gthumb comments.")
   parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                     help="Be verbose.")
   myoptions, args = parser.parse_args(argv)

   imagefiles = []
   for arg in args:
      if os.path.isfile(arg):
         imagefiles.append(arg)
      elif os.path.isdir(arg):
         for root, dirs, files in os.walk(arg):
            for myfile in files:
               imagefiles.append(os.path.join(root, myfile))
      else:
         print arg + " is not a regular file or directory."
         sys.exit(1)

   for imagefile in imagefiles:
      autogate_gthumb(imagefile, myoptions)


if __name__ == "__main__":
   run(sys.argv[1:])


