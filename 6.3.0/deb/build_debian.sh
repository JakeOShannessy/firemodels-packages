repo=fds-smv_deprecated
commit=f7f414800cb6e0829433ad150b0da71d4074ed9d
version=6.3.0
cp ../version.patch fds-${version}/debian/patches/version || true
wget https://github.com/firemodels/${repo}/archive/${commit}.zip
unzip ${commit}.zip
pushd ${repo}-${commit}
tar -czvf ../fds-${version}_${version}.orig.tar.gz .
popd
pushd fds-${version}
tar -xzvf ../fds-${version}_${version}.orig.tar.gz
debuild --no-sign