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
./go develop --always-unzip

# run service
cat <<EOF

###############

## You will need an account in a LEAP provider. You may find some at http://bitmask.net/

## Once you have it, modify the service/pixelated.example file and move it to ~/.pixelated

## You might also need to add your LEAP provider ssl certificate to the pixelated/certificates folder, named as your provider domain name (in case it uses TLS):
##      - example: your.leapprovider.org.crt

## Once you are done, just run:
##        pixelated-user-agent

EOF
