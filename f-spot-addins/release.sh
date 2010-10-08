#!/bin/bash
set -e
DISTRIBUTIONS="maverick"
PACKAGE="f-spot-extension-exiflow"
export GPGKEY=3E2898DA
export DEBEMAIL='ubuntu@sleif.de'
export DEBFULLNAME='Sebastian Berthold'
version=`grep -w "version=" ExiflowCreateVersion/ExiflowCreateVersion.addin.xml | cut -d\" -f2 | head -1`
if head -1 debian/changelog | grep -q $version; then
	echo "The file debian/changelog already contains version ${version}."
	echo "Did you forget to update version number in setup.py firsti?"
	read -p "Press Ctrl-C to stop, Enter to continue." bla
else
	dch -v ${version}-1 "Release F-spot Exiflow extensions ${version}."
	svn commit -m "Update debian changelog for ${version}." debian/changelog
fi

mkdir dist
svn export . dist/${PACKAGE}-${version}
cd dist
tar cfz ${PACKAGE}_${version}.orig.tar.gz ${PACKAGE}-${version}
cd ${PACKAGE}-${version}
for dist in ${DISTRIBUTIONS}; do
	dch --distribution ${dist} -b -v ${version}-1ppa1~${dist}1 "Upload Exiflow ${version} for ${dist}."
	debuild -S -sa
done
cd ..
rm -rf ${PACKAGE}-${version}
for dist in ${DISTRIBUTIONS}; do
    dput ppa:exiflow/exiflow ${PACKAGE}_${version}-1ppa1~${dist}1_source.changes
done
