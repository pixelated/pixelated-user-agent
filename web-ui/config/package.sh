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
./go clean
./go compass
./go handlebars
./go imagemin
./go minify_html
./go minify_sandbox
./go add_git_version
./go buildmain


# copy files
cd app
cp --parents \
404.html \
fonts/* \
locales/**/* \
bower_components/font-awesome/css/font-awesome.min.css \
bower_components/jquery-file-upload/css/jquery.fileupload.css \
bower_components/font-awesome/fonts/* \
../dist
cd -

# concat js files and minify for app.min.js
cat \
app/bower_components/modernizr/modernizr.js \
app/bower_components/lodash/dist/lodash.js \
app/bower_components/jquery/dist/jquery.js \
app/bower_components/jquery-ui/jquery-ui.min.js \
app/bower_components/jquery-file-upload/js/jquery.fileupload.js \
app/js/lib/highlightRegex.js \
app/bower_components/handlebars/handlebars.min.js \
app/bower_components/typeahead.js/dist/typeahead.bundle.min.js \
app/bower_components/foundation/js/foundation.js \
app/bower_components/foundation/js/foundation/foundation.reveal.js \
app/bower_components/foundation/js/foundation/foundation.offcanvas.js \
app/js/foundation/initialize_foundation.js \
app/bower_components/iframe-resizer/js/iframeResizer.min.js \
.tmp/app.concatenated.js > dist/app.js
mv dist/app.js dist/app.min.js

# concat js files and minify for sandbox.min.js
cat \
app/js/sandbox.js \
app/bower_components/iframe-resizer/js/iframeResizer.contentWindow.min.js > dist/sandbox.js
node_modules/.bin/minify dist/sandbox.js > dist/sandbox.min.js
rm dist/sandbox.js
