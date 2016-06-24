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
define(['i18next',
        'i18nextXHRBackend',
        'i18nextBrowserLanguageDetector'],
function(i18n, i18n_backend, I18n_detector) {
  'use strict';

  var detector = new I18n_detector();
  var detect = detector.detect.bind(detector);

  detector.detect = function(detectionOrder)  {
    var result = detect(detectionOrder);
    return result.replace('-', '_');
  };

  function t(i18n_key) {
    var result = i18n.t(i18n_key);
    var safe_string = new Handlebars.SafeString(result);
    return safe_string.string;
  }

  function loaded(callback) {
    i18n.on('loaded', function(loaded) {
        callback();
    });
  }

  function init(path) {
    i18n
      .use(i18n_backend)
      .use(detector)
      .init({
        fallbackLng: 'en_US',
        backend: {
          loadPath: path + 'locales/{{lng}}/{{ns}}.json'
        }
      });
    // Handlebars.registerHelper('t', self.bind(self));
    Handlebars.registerHelper('t', t);
  }

  return {
    t: t,
    init: init,
    loaded: loaded
  };
});
