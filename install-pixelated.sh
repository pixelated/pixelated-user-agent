#!/bin/bash
#
# Copyright (c) 2014 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.

# test dependencies
function check_installed() {
        which $1
        if [ $? -ne 0 ]; then
                echo "## You must have ${1} installed and in the PATH to run Pixelated-User-Agent"
                echo "## exiting..."
                exit 1
        fi
}

for dependency in node npm ruby bundle virtualenv git gpg; do
        check_installed $dependency
done

# install web-ui dependencies
cd web-ui
npm install
node_modules/bower/bin/bower install --config.interactive=false
bundle install
LC_ALL=en_US.UTF-8 ./go build

# install service dependencies
cd ../service
virtualenv .virtualenv
source .virtualenv/bin/activate
./go develop --always-unzip
pip uninstall -y gnupg; pip install gnupg

# print usage
cat <<EOF

###############

## You will need an account in a LEAP provider. You may find some at http://bitmask.net/

## Once you have it, modify the service/pixelated.example file and move it to ~/.pixelated

## You might also need to add your LEAP provider ssl certificate to the pixelated/certificates folder, named as your provider domain name (in case it uses TLS):
##      - example: your.leapprovider.org.crt

## Once you are done, just run:
##        pixelated-user-agent

EOF
