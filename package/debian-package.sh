#!/bin/bash
#
# Copyright (c) 2014 ThoughtWorks Deutschland GmbH
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.

set -e

#mv service/debian .
#
#if [ -n "$GO_PIPELINE_COUNTER" ]; then
#        echo "USING COUNTER NUMBER: $GO_PIPELINE_COUNTER"
#        git-dch -a -S --snapshot-number=$GO_PIPELINE_COUNTER
#else
#        echo "NO COUNTER NUMBER PRESENT"
#        git-dch -a -S
#fi

#mv debian service

pushd service

python setup.py sdist

TEMP_DIR=$(mktemp -d)

cp dist/pixelated-user-agent*.tar.gz $TEMP_DIR/

pushd $TEMP_DIR
cp pixelated-user-agent*.tar.gz pixelated-user-agent_0.1.orig.tar.gz
tar -xzf pixelated-user-agent-0.1.tar.gz
cd pixelated*

dpkg-buildpackage -rfakeroot -uc -us

# manual build
#mkdir pkg-root
#python setup.py install --root=pkg-root --install-layout=deb
#fakeroot dpkg --build pkg-root ../python-pixelated-dispatcher_0.1-1_all.deb

cp $TEMP_DIR/python-pixelated-user-agent*all.deb /tmp/

popd
popd

rm -Rf $TEMP_DIR

