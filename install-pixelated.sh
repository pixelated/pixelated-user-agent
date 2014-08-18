#!/bin/bash

# test dependencies
function check_installed() {
        which $1
        if [ $? -ne 0 ]; then
                echo "## You must have ${1} installed and in the PATH to run Pixelated-User-Agent"
                echo "## exiting..."
                exit 1
        fi
}

for dependency in node npm ruby bundle virtualenv; do
        check_installed $dependency     
done

# clone repo
git clone https://github.com/pixelated-project/pixelated-user-agent

# install web-ui dependencies
cd pixelated-user-agent/web-ui
npm install
node_modules/bower/bin/bower install
bundle install

# install service dependencies
cd ../service
virtualenv .virtualenv
source .virtualenv/bin/activate
easy_install leap.soledad.common
pip install -r requirements.txt

# run service
./go
