#!/bin/bash
export GPGKEY=643D8C7A
export DEBEMAIL='launchpad.net@rompe.org'
export DEBFULLNAME='Ulf Rompe'
version=`grep -w "version=" setup.py | cut -d\' -f2`
if head -1 debian/changelog | grep -q $version; then
	echo "The file debian/changelog already contains version ${version}."
	echo "Did you forget to update version number in setup.py firsti?"
	read -p "Press Ctrl-C to stop, Enter to continue." bla
else
	dch -v ${version}-1 "Release Exiflow ${version}."
	svn commit -m "Update debian changelog for ${version}." debian/changelog
fi
python setup.py bdist_rpm # For Sourceforge
python setup.py sdist
cp dist/Exiflow-${version}.tar.gz dist/exiflow_${version}.orig.tar.gz
svn export . dist/exiflow-${version}
cd dist/exiflow-${version}
for dist in maverick lucid; do
	dch --distribution ${dist} -b -v ${version}-1ppa1~${dist}1 "Upload Exiflow ${version} for ${dist}."
	debuild -S -sa
	debuild -b
done
cd ..
rm -rf exiflow-${version}
#dput ppa:rompe/exiflow exiflow_${version}-1ppa1~maverick1_source.changes
#dput ppa:rompe/exiflow exiflow_${version}-1ppa1~lucid1_source.changes

# Now some files for Sourceforge
rm -rf sourceforge
mkdir sourceforge
mv *.rpm *.deb Exiflow-${version}.tar.gz sourceforge/
echo "Now upload dist/sourceforge to Sourceforge."

