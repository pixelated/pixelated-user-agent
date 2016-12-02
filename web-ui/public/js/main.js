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

requirejs.config({
  baseUrl: '../static/',
  paths: {
    'mail_list': 'js/mail_list',
    'page': 'js/page',
    'feedback': 'js/feedback',
    'flight': 'bower_components/flight',
    'DOMPurify': 'bower_components/DOMPurify/dist/purify.min',
    'he': 'bower_components/he/he',
    'hbs': 'js/generated/hbs',
    'helpers': 'js/helpers',
    'lib': 'js/lib',
    'views': 'js/views',
    'tags': 'js/tags',
    'mail_list_actions': 'js/mail_list_actions',
    'user_alerts': 'js/user_alerts',
    'mail_view': 'js/mail_view',
    'dispatchers': 'js/dispatchers',
    'services': 'js/services',
    'mixins': 'js/mixins',
    'search': 'js/search',
    'foundation': 'js/foundation',
    'features': 'js/features/features',
    'i18next': 'bower_components/i18next/i18next',
    'i18nextXHRBackend': 'bower_components/i18next-xhr-backend/i18nextXHRBackend',
    'i18nextBrowserLanguageDetector': 'bower_components/i18next-browser-languagedetector/i18nextBrowserLanguageDetector',
    'quoted-printable': 'bower_components/quoted-printable',
    'utf8': 'bower_components/utf8',
    'user_settings': 'js/user_settings'
  }
});

require([
  'flight/lib/compose',
  'flight/lib/debug'
], function(compose, debug){
  'use strict';
  debug.enable(true);
  debug.events.logAll();
});

require(
  [
    'flight/lib/compose',
    'flight/lib/registry',
    'flight/lib/advice',
    'flight/lib/logger',
    'flight/lib/debug',
    'page/events',
    'page/default',
    'js/monkey_patching/all'
  ],

  function(compose, registry, advice, withLogging, debug, events, initializeDefault, _monkeyPatched) {
    'use strict';

    window.Pixelated = window.Pixelated || {};
    window.Pixelated.events = events;

    compose.mixin(registry, [advice.withAdvice, withLogging]);

    debug.enable(true);
    debug.events.logAll();

    initializeDefault('');
  }
);
