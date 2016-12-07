
var tests = Object.keys(window.__karma__.files).filter(function (file) {
  'use strict';
  return (/\.spec\.js$/.test(file));
});

beforeEach(function() {
    'use strict';
    jasmine.Ajax.install();
});

afterEach(function() {
    'use strict';
    jasmine.Ajax.uninstall();
});

requirejs.config({

  baseUrl: '/base',

  paths: {
    'page': 'public/js/page',
    'js': 'public/js',
    'lib': 'public/js/lib',
    'hbs': 'public/js/generated/hbs',
    'flight': 'public/bower_components/flight',
    'DOMPurify': 'public/bower_components/DOMPurify/dist/purify.min',
    'he': 'public/bower_components/he/he',
    'views': 'public/js/views',
    'helpers': 'public/js/helpers',
    'feedback': 'public/js/feedback',
    'tags': 'public/js/tags',
    'mail_list': 'public/js/mail_list',
    'mail_list_actions': 'public/js/mail_list_actions',
    'user_alerts': 'public/js/user_alerts',
    'mail_view': 'public/js/mail_view',
    'dispatchers': 'public/js/dispatchers',
    'mixins': 'public/js/mixins',
    'services': 'public/js/services',
    'search': 'public/js/search',
    'monkey_patching': 'public/js/monkey_patching',
    'i18next': 'public/bower_components/i18next/i18next',
    'i18nextXHRBackend': 'public/bower_components/i18next-xhr-backend/i18nextXHRBackend',
    'i18nextBrowserLanguageDetector': 'public/bower_components/i18next-browser-languagedetector/i18nextBrowserLanguageDetector',
    'quoted-printable': 'public/bower_components/quoted-printable',
    'utf8': 'public/bower_components/utf8',
    'test': 'test',
    'features': 'test/features',
    'user_settings': 'public/js/user_settings'
  },

  deps: tests,

  callback: function () {
    'use strict';
    require(['page/events','test/test_data', 'views/i18n', 'i18next', 'i18nextXHRBackend', 'monkey_patching/array', 'views/recipientListFormatter', 'test/custom_matchers'],
      function (events, testData, i18n, i18next, i18n_backend, mp, recipientListFormatter, customMatchers) {
      window.Pixelated = window.Pixelated || {};
      window.Pixelated.events = events;
      window.Pixelated.testData = testData;
      window.Pixelated.mockBloodhound = function() {
        window.Bloodhound = function() {};
        window.Bloodhound.prototype.initialize = function() {};
        window.Bloodhound.prototype.ttAdapter = function() {};
        window.Bloodhound.prototype.clear = function() {};
        window.Bloodhound.prototype.clearPrefetchCache = function() {};
        window.Bloodhound.prototype.clearRemoteCache = function() {};
        $.fn.typeahead = function() {};
      };

      i18next
      .use(i18n_backend)
      .init({
        lng: 'en_US',
        backend: {
          loadPath: '/base/public/locales/en_US/translation.json'
        }
      });
      Handlebars.registerHelper('t', i18n.t);

      i18next.on('loaded', function() {
        window.__karma__.start();
      });
    });
  }
});
