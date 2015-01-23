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

PROVISIONING_PATH=$(dirname $0)
USER_AGENT_DIR="$PROVISIONING_PATH/.."

PACKAGE_FILE="hackday-pixelated-user-agent.box"
BOX_NAME="hackaday-pixelated-user-agent"

pushd $USER_AGENT_DIR

# clear old boxes
vagrant destroy -f source
vagrant destroy -f hackday
vagrant box remove $BOX_NAME
rm "$USER_AGENT_DIR/$PACKAGE_FILE"

# build from scratch
vagrant up source && \
vagrant package --output="$USER_AGENT_DIR/$PACKAGE_FILE" && \
vagrant box add $BOX_NAME $PACKAGE_FILE

SUCCESS=$?

popd

if [ $SUCCESS -eq 0 ] ; then
	echo
	echo "Created hackday box $PACKAGE_FILE"
	echo "If you want to test it, run"
	echo
	echo "vagrant up hackday"
else
	echo "Error while building hackday box" 1>&2
fi

exit $SUCCESS

