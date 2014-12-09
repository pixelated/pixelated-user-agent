#!/bin/bash

# prepare files for .deb package
export PIXELATED_BUILD='package'

mkdir -p dist

# initial npm tasks
./go clean
./go compass
./go handlebars
./go imagemin
./go minify_html
./go buildmain


# copy files
cd app
cp --parents 404.html fonts/* locales/**/* bower_components/font-awesome/css/font-awesome.min.css bower_components/font-awesome/fonts/* ../dist
cd -

# concat js files and minify
cat \
app/bower_components/modernizr/modernizr.js \
app/bower_components/lodash/dist/lodash.js \
app/bower_components/jquery/dist/jquery.js \
app/js/lib/highlightRegex.js \
app/bower_components/handlebars/handlebars.min.js \
app/bower_components/typeahead.js/dist/typeahead.bundle.min.js \
app/bower_components/foundation/js/foundation.js \
app/bower_components/foundation/js/foundation/foundation.reveal.js \
app/bower_components/foundation/js/foundation/foundation.offcanvas.js \
.tmp/app.concatenated.js > dist/app.js
node_modules/.bin/minify dist/app.js > dist/app.min.js
rm dist/app.js

