#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4
"""
Import files from given directories to your photo folder.

Optionally unmounts source media after successfull import.
"""
__revision__ = "$Id$"

import os
import sys
import stat
import shutil
import logging
import argparse
import subprocess
from typing import Callable, Optional, Sequence
from . import filelist as exiflow_filelist


def run(argv: Sequence[str],
        callback: Optional[Callable[[str, str, float, bool], bool]] = None):
    """
    Take an equivalent of sys.argv[1:] and optionally a callable.

    Parse options, import files and optionally call the callable on every
    processed file with 3 arguments: filename, newname, percentage.
    If the callable returns True, stop the processing.
    """
    # Parse command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mount", dest="mount",
                        help="Mountpoint of directory to import. Corresponds"
                             " to %m in the gnome-volume-manager config "
                             "dialog.")
    parser.add_argument("-t", "--target", dest="target",
                        help="Target directory. A subdirectory will be created"
                             " in this directory.")
    parser.add_argument("-d", "--device", dest="device",
                        help="(Ignored for backwards compatibility.)")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                        help="Be verbose.")
    options = parser.parse_args(argv)
    logging.basicConfig(format="%(module)s: %(message)s")
    if options.verbose:
        logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger("exiimport")
    if not options.mount or not options.target:
        return "Wrong syntax.\n" + parser.format_help()

    # Build file list whithout skipping unknown files
    filelist = exiflow_filelist.Filelist([])
    filelist.process_unknown_types()
    filelist.add_files([options.mount])

    # Cry if we found no images
    if filelist.get_filecount() == 0:
        return "No files to import, sorry."

    # Create targetdir
    targetdir = os.path.join(options.target, filelist.get_daterange())
    # TODO: find a better solution than just appendings "+" chars.
    while os.path.exists(targetdir):
        targetdir += "+"
    os.makedirs(targetdir)
    logger.warning("Importing %s MB in %s files to %s",
                   filelist.get_fullsize() / 1024 / 1024,
                   filelist.get_filecount(), targetdir)

    # Copy files
    for filename, percentage in filelist:
        logger.info("%3s%% %s", percentage, filename)
        if callable(callback):
            if callback("", os.path.join(targetdir,
                                         os.path.basename(filename)),
                        percentage, True):
                break

        shutil.copy2(filename, targetdir)
        os.chmod(os.path.join(targetdir, os.path.basename(filename)),
                 stat.S_IMODE(0o644))

    # Unmount card
    with subprocess.Popen("mount", universal_newlines=True,
                          stdout=subprocess.PIPE) as mount:
        stdout = mount.communicate()[0]
    for line in stdout.splitlines():
        # Example line:
        # /dev/sdc1 on /media/NIKON D70 type vfat (rw,nosuid,n[...]
        line_parts = line.split(" type", 1)[0].split(None, 2)
        if (len(line_parts) == 3 and line_parts[1] == "on" and
           os.path.realpath(options.mount) == os.path.realpath(line_parts[2])):
            logger.warning("Trying to unmount %s.", line_parts[0])
            subprocess.call(["umount", line_parts[0]])


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
