#!/bin/bash
version=`grep -w "version=" setup.py | cut -d\' -f2`
if head -1 debian/changelog | grep -q $version; then
	echo "The file debian/changelog already contains version ${version}."
	echo "Please update version number in setup.py first."
	exit 1
fi
dch -v ${version}
python setup.py sdist
mv dist/Exiflow-${version}.tar.gz dist/exiflow_${version}.orig.tar.gz
svn export . dist/exiflow-${version}
cd dist/exiflow-${version}
debuild -S
cd ..
dput ppa:rompe/exiflow exiflow_${version}_source.changes
