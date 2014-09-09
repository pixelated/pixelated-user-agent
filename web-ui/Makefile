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

DESTDIR=target

compile:
	bundle install --path=~/pixelated-gems
	npm install
	node_modules/bower/bin/bower install
	./go package

clean:
	rm -Rf dist/ $(DESTDIR)/


install:
	install -d $(DESTDIR)/usr/share/pixelated-user-agent
	cp -r dist/* $(DESTDIR)/usr/share/pixelated-user-agent


all: clean compile install

.PHONY: clean compile install all

