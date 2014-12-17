/*
 * Copyright (c) 2014 ThoughtWorks, Inc.
   *
 * Pixelated is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Pixelated is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
 */

({
  baseUrl: '../app',
  wrap: true,
  almond: true,
  optimize: 'uglify',
  mainConfigFile: '../app/js/main.js',
  out: '../dist/app.min.js',
  include: [
    'bower_components/modernizr/modernizr',
    'bower_components/lodash/dist/lodash',
    'bower_components/jquery/dist/jquery',
    'js/lib/highlightRegex',
    'bower_components/handlebars/handlebars.min',
    'bower_components/typeahead.js/dist/typeahead.bundle.min',
    'bower_components/foundation/js/foundation',
    'bower_components/foundation/js/foundation/foundation.reveal',
    'bower_components/foundation/js/foundation/foundation.offcanvas',
    'js/main'
  ],
  name:'bower_components/almond/almond',

})

