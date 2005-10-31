#!/usr/bin/env python2.4
# -*- coding: utf-8 -*-
import os
import sys
import stat
import time
import shutil
import optparse
import subprocess

extensions = (".jpg", ".nef", ".raw", ".gif")

# Parse command line.
parser = optparse.OptionParser()
parser.add_option("-m", "--mount", dest="mount",
                  help="Mountpoint of directory to import. Corresponds" \
                       " to %m in the gnome-volume-manager config dialog.")
parser.add_option("-t", "--target", dest="target",
                  help="Target directory. A subdirectory will be created" \
                       " in this directory.")
parser.add_option("-d", "--device", dest="device",
                  help="Mounted device file. If given, this device will be " \
                       "unmounted using pumount after the import. Corresponds" \
                       " to %d in the gnome-volume-manager config dialog.")
options, args = parser.parse_args()
if len(args) > 0 or not options.mount or not options.target:
    print >>sys.stderr, "Wrong syntax, call with --help for info."
    sys.exit(1)

# Build dictionary of images to import.
# Every entry has the complete path as the key and a corresponding stat object
# as it's value, so we can easily retrieve st_mtime or st_size from it.
images = {}
fullsize = 0
datedict = {}
for root, dirs, files in os.walk(options.mount):
    for name in files:
        if name.endswith(".dsc"):
            print "Skipping file:", name
        else:
            filepath = os.path.join(root, name)
            filestat = os.stat(filepath)
            images[filepath] = filestat
            datedict[time.strftime("%Y-%m-%d",
                                   time.localtime(filestat.st_mtime))] = True
            fullsize += filestat.st_size

# Cry if we found no images
if fullsize == 0:
    print >>sys.stderr, "No bytes to import, sorry."
    sys.exit(1)

# Make up daterange
tmpdates = datedict.keys()
tmpdates.sort()
daterange = tmpdates[0]
tmplen = len(tmpdates)
if tmplen > 1:
    daterange += "_-_" + tmpdates[tmplen - 1]

# Create targetdir
targetdir = os.path.join(options.target, daterange)
while os.path.exists(targetdir):
    targetdir += "+"
os.makedirs(targetdir)
print "Importing", fullsize / 1024 / 1024 , "MB to", targetdir

# Copy files
progress_size = 0
for file in images:
   progress_size += images[file].st_size
   print "%3s%% (%s)" % (100 * progress_size / fullsize, file)
   shutil.copy2(file, targetdir)
   os.chmod(os.path.join(targetdir, os.path.basename(file)), stat.S_IMODE(0644))

# Unmount card
if options.device:
   subprocess.call("pumount " + options.device, shell=True)

