#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""Handle reading and writing gthumb comment files."""
__revision__ = "$Id$"

import os
import re
import gzip
from typing import Dict, List, Union
import xml.dom.minidom


class Gthumb(object):
    """Read and write gthumb comment files for an image."""

    def __init__(self, filename: str):
        """Create a Gthumb object for image filename."""
        self.fields: Dict[str, str] = {}
        self.filename = os.path.abspath(filename)
        self.commentsdir = os.path.join(os.path.dirname(self.filename),
                                        ".comments")
        self.commentsfile = os.path.join(self.commentsdir,
                                         os.path.basename(self.filename) +
                                         ".xml")

    def read(self) -> bool:
        r"""
        Read gthumb comment information for filename.

        Fill the dictionary self.fields with the corresponding EXIF values.
        Return True on success and False if no comment file exists.

        Translation of Exif values to gthumb sections:

            "Artist"            => "Note" line: "^Artist::.*"
            "Credit"            => "Note" line: "^Credit::.*"
            "Copyright"         => "Note" line: "^Copyright::.*"
            "CopyrightNotice"   => "Note" line: "^CopyrightNotice::.*"
            "UserComment"       => "Note" line: "^UserComment::.*"
            "ImageDescription"  => "Note" free text without "^\\w+::"
            "Keywords"          => "Keywords" comma separated list
            "Location"          => "Place"
            "DateTimeOriginal"  => "Time" in seconds since 1970-01-01
            "XPTitle"           => First line of "Note", if any

        In fact, any line of "Note" that consists of a keyword followed by
        two colons and some random text is converted into it's EXIF equivalent.
        """
        gthumb_to_exif = {"Time": "DateTimeOriginal",
                          "Place": "Location",
                          "Keywords": "Keywords"}

        if os.path.isfile(self.commentsfile):
            mydata: Dict[str, str] = {}
            mydom: xml.dom.minidom.Document = \
                xml.dom.minidom.parse(  # type: ignore
                    gzip.open(self.commentsfile))
            for field in ("Note", "Keywords", "Place", "Time"):
                mynodes: List[xml.dom.minidom.Element] = \
                    mydom.getElementsByTagName(field)  # type: ignore
                if len(mynodes) > 0:
                    mynodes = mynodes[0].childNodes
                    if len(mynodes) > 0:
                        mydata[field] = mynodes[0].wholeText  # type: ignore

            for key, value in gthumb_to_exif.items():
                if key in mydata:
                    self.fields[value] = mydata[key]
            if "Note" in mydata:
                note: List[str] = []
                myregex = re.compile("(\\w+)::(.*)$")
                for line in mydata["Note"].split("\n"):
                    match = myregex.match(line)
                    if match:
                        self.fields[match.group(1)] = match.group(2).strip()
                    else:
                        note.append(line)
                if len(note) > 0:
                    self.fields["XPTitle"] = note[0]
                    self.fields["ImageDescription"] = "\n".join(note).strip()
            return True
        return False

    def write(self, myaddfields: bool = False,
              mytemplate: bool = False) -> None:
        """
        Write Exif information from self.fields into gthumb comment file.

        Apply reverse mapping of self.read().

        myaddfields: Write some additional fields.
        mytemplate: Write empty fields as well.
        """
        exiffields = ["Artist", "Credit", "Copyright", "CopyrightNotice",
                      "UserComment"]
        mydata: Dict[str, str] = {}
        mydata["Place"] = self.fields.get("Location", "")
        mydata["Time"] = self.fields.get("DateTimeOriginal", "")
        mydata["Note"] = self.fields.get("ImageDescription", "")
        tmpkeywords: List[str] = []
        for keyword in self.fields.get("Keywords", "").split(","):
            tmpkeywords.append(keyword.strip())
        mydata["Keywords"] = ",".join(tmpkeywords)

        # Add XPTitle to Note if Note doesn't contain it already
        mytitle = self.fields.get("XPTitle", "")
        if len(mytitle) > 0 and mytitle not in mydata["Note"].splitlines():
            mydata["Note"] = self.fields["XPTitle"] + "\n" + mydata["Note"]
        if myaddfields or mytemplate:
            mydata["Note"] += "\n"
            for field in exiffields:
                fieldvalue = self.fields.get(field, "")
                if mytemplate or len(fieldvalue) > 0:
                    mydata["Note"] += "\n" + field + ":: " + fieldvalue

        mydom = xml.dom.minidom.Document()
        comment: xml.dom.minidom.Element = \
            mydom.createElement("Comment")  # type: ignore
        comment.setAttribute("format", "2.0")  # type: ignore
        mydom.appendChild(comment)  # type: ignore

        for name in ("Place", "Time", "Note", "Keywords"):
            element = mydom.createElement(name)  # type: ignore
            text = mydom.createTextNode(mydata[name])  # type: ignore
            element.appendChild(text)  # type: ignore
            comment.appendChild(element)  # type: ignore

        if not os.path.isdir(self.commentsdir):
            os.makedirs(self.commentsdir)
        gzip.open(self.commentsfile, "wb").write(
            mydom.toxml(encoding="utf-8"))  # type: ignore

    def get_mtime(self) -> int:
        """Get modification time of comment file or 0 if it doesn't exist."""
        mtime = 0
        if os.path.isfile(self.commentsfile):
            mtime = int(os.path.getmtime(self.commentsfile))
        return mtime

    def set_mtime(self, mtime: Union[float, int]) -> bool:
        """
        Set modification time of comment file to mtime.

        Returns True on success and False if no comment file exists.
        """
        if os.path.isfile(self.commentsfile):
            os.utime(self.commentsfile, (mtime, mtime))
            return True
        else:
            return False

    def cleanup(self):
        """
        Remove additional fields from gthumb comments.

        (other fields than Note, Keywords, Place, Time)
        Return True if a file is cleaned, False otherwise.
        """
        if self.read():
            for field in self.fields:
                if field not in ("ImageDescription", "Location",
                                 "DateTimeOriginal", "Keywords", "XPTitle"):
                    mtime = self.get_mtime()
                    self.write()
                    self.set_mtime(mtime)
                    return True
        return False
