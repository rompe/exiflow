#!/bin/sh -e

version=`grep -w "version=" setup.py | cut -d\' -f2`

# Build RPM as well as src.rpm
./setup.py bdist_rpm --build-requires=python,python-setuptools,perl-Image-ExifTool --requires=python,perl-Image-ExifTool
# Test src.rpm in chroot like copr does
mock --rebuild dist/Exiflow-$version-1.src.rpm

# Upload src.rpm to web server
publish_in_outgoing.sh dist/Exiflow-$version-1.src.rpm
# Trigger copr build
copr-cli build exiflow http://rompe.net/outgoing/Exiflow-$version-1.src.rpm

# Upload to pypi as well
twine upload dist/Exiflow-${version}.tar.gz
