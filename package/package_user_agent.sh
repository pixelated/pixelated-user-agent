#!/bin/bash

set -x 

BUILD_PATH=/tmp/pix-user-agent-build
PIXELATED_LIB_PATH=$BUILD_PATH/var/lib/pixelated
PIXELATED_WEB_LIB_PATH=$PIXELATED_LIB_PATH/web-ui/app
PIXELATED_VIRTUALENV_PATH=$PIXELATED_LIB_PATH/virtualenv
BIN_PATH=$BUILD_PATH/usr/local/bin

# create build folder
[[ ! -d "$BUILD_PATH" ]] && mkdir $BUILD_PATH
rm -rf $BUILD_PATH/*

# create internal folders
mkdir -p $BIN_PATH
mkdir -p $PIXELATED_LIB_PATH
mkdir -p $PIXELATED_WEB_LIB_PATH
mkdir -p $BUILD_PATH

# build web-ui code
cd web-ui 
bundle install --path=~/pixelated-gems
npm install
node_modules/bower/bin/bower install
./go package
cd ..

# copy code
cp -rf service $PIXELATED_LIB_PATH
cp -rf web-ui/dist/* $PIXELATED_WEB_LIB_PATH

# build virtual env
virtualenv $PIXELATED_VIRTUALENV_PATH
. $PIXELATED_VIRTUALENV_PATH/bin/activate
easy_install leap.soledad.common
pip install -r service/requirements.txt
deactivate

cp package/pixelated-user-agent $BIN_PATH

cd $BUILD_FOLDER
gem install fpm
fpm -s dir  -t deb -n pixelated-user-agent -C . .
