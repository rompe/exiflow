#!/bin/bash
set -e
#
# adopt version in ./exiflow/exigui.glade, ./setup.py
# set Ubuntu versions in DISTRIBUTION
#
DISTRIBUTIONS="lucid precise quantal raring saucy trusty"
if [ ${USER} == "ulf" ]; then
	export GPGKEY=643D8C7A
	export DEBEMAIL='launchpad.net@rompe.org'
	export DEBFULLNAME='Ulf Rompe'
else
	export GPGKEY=3E2898DA
	export DEBEMAIL='exiflow@sleif.de'
	export DEBFULLNAME='Sebastian Berthold'
fi
version=`grep -w "version=" setup.py | cut -d\' -f2`
if head -1 debian/changelog | grep -q $version; then
	echo "The file debian/changelog already contains version ${version}."
	echo "Did you forget to update version number in setup.py first?"
	read -p "Press Ctrl-C to stop, Enter to continue." bla
else
	dch -v ${version}-1 "Release Exiflow ${version}."
	git commit -m "Update debian changelog for ${version}." debian/changelog
	git push
fi
python setup.py bdist_rpm # For Sourceforge
python setup.py sdist
cp dist/Exiflow-${version}.tar.gz dist/exiflow_${version}.orig.tar.gz
mkdir dist/exiflow-${version}/
git archive master | tar -x -C dist/exiflow-${version}/
cd dist/exiflow-${version}
for dist in ${DISTRIBUTIONS}; do
	dch --distribution ${dist} -b -v ${version}-1ppa1~${dist}1 "Upload Exiflow ${version} for ${dist}."
	debuild -S -sa
	debuild -b
done
cd ..
rm -rf exiflow-${version}
for dist in ${DISTRIBUTIONS}; do
	dput ppa:exiflow/exiflow exiflow_${version}-1ppa1~${dist}1_source.changes
done

# Now some files for Sourceforge
rm -rf sourceforge
mkdir sourceforge
mv *.rpm *natty*.deb Exiflow-${version}.tar.gz sourceforge/
echo "Now upload dist/sourceforge to Sourceforge."

