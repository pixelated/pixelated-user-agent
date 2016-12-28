#!/bin/bash
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

# prepare files for .deb package

set -e

export PIXELATED_BUILD='package'

mkdir -p dist

# initial npm tasks
./go build
./go imagemin
./go minify_html
./go minify_sandbox


# concat js files and minify for app.min.js
cat \
app/bower_components/modernizr/modernizr.js \
app/bower_components/lodash/dist/lodash.js \
app/bower_components/jquery/dist/jquery.js \
app/bower_components/jquery-ui/jquery-ui.js \
app/bower_components/jquery-file-upload/js/jquery.fileupload.js \
app/bower_components/handlebars/handlebars.js \
app/bower_components/typeahead.js/dist/typeahead.bundle.js \
app/bower_components/foundation/js/foundation.js \
app/bower_components/foundation/js/foundation/foundation.reveal.js \
app/bower_components/foundation/js/foundation/foundation.offcanvas.js \
app/bower_components/iframe-resizer/js/iframeResizer.js \
app/js/1.bundle.js \
app/js/bundle.js > dist/app.js
node_modules/.bin/minify dist/app.js > dist/app.min.js
rm dist/app.js

if [ ! -s dist/app.min.js ]
then
echo "Minification failed!"
exit 1;
fi

# concat js files and minify for sandbox.min.js
cat \
app/js/sandbox.js \
app/bower_components/iframe-resizer/js/iframeResizer.contentWindow.js > dist/sandbox.js
node_modules/.bin/minify dist/sandbox.js > dist/sandbox.min.js
rm dist/sandbox.js
