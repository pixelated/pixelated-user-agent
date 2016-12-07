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

set -e

# concat js files and minify for app.min.js
cat \
public/bower_components/modernizr/modernizr.js \
public/bower_components/lodash/dist/lodash.js \
public/bower_components/jquery/dist/jquery.js \
public/bower_components/jquery-ui/jquery-ui.js \
public/bower_components/jquery-file-upload/js/jquery.fileupload.js \
public/js/lib/highlightRegex.js \
public/bower_components/handlebars/handlebars.js \
public/bower_components/typeahead.js/dist/typeahead.bundle.js \
public/bower_components/foundation/js/foundation.js \
public/bower_components/foundation/js/foundation/foundation.reveal.js \
public/bower_components/foundation/js/foundation/foundation.offcanvas.js \
public/js/foundation/initialize_foundation.js \
public/bower_components/iframe-resizer/js/iframeResizer.js \
.tmp/app.concatenated.js | node_modules/.bin/minify --js > public/app.min.js
