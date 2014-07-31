'use strict';

var tests = Object.keys(window.__karma__.files).filter(function (file) {
  return (/\.spec\.js$/.test(file));
});

requirejs.config({

  baseUrl: '/base',

  paths: {
    'page': 'app/js/page',
    'js': 'app/js',
    'lib': 'app/js/lib',
    'hbs': 'app/js/generated/hbs',
    'flight': 'app/bower_components/flight',
    'views': 'app/js/views',
    'helpers': 'app/js/helpers',
    'tags': 'app/js/tags',
    'mail_list': 'app/js/mail_list',
    'mail_list_actions': 'app/js/mail_list_actions',
    'user_alerts': 'app/js/user_alerts',
    'mail_view': 'app/js/mail_view',
    'dispatchers': 'app/js/dispatchers',
    'mixins': 'app/js/mixins',
    'services': 'app/js/services',
    'search': 'app/js/search',
    'monkey_patching': 'app/js/monkey_patching',
    'i18next': 'app/bower_components/i18next/i18next.amd',
    'quoted-printable': 'app/bower_components/quoted-printable',
    'test': 'test'
  },


  deps: tests,

  callback: function () {
    require(['page/events','test/test_data', 'views/i18n', 'monkey_patching/array', 'views/recipientListFormatter'], function (events, testData, i18n, mp, recipientListFormatter) {
      window['Smail'] = window['Smail'] || {};
      window['Smail'].events = events;
      window['Smail'].testData = testData;
      window['Smail'].mockBloodhound = function() {
        window.Bloodhound = function() {};
        window.Bloodhound.prototype.initialize = function() {};
        window.Bloodhound.prototype.ttAdapter = function() {};
        window.Bloodhound.prototype.clear = function() {};
        window.Bloodhound.prototype.clearPrefetchCache = function() {};
        window.Bloodhound.prototype.clearRemoteCache = function() {};
        $.fn.typeahead = function() {};
      };

      i18n.init('/base/app/');
      // start test run, once Require.js is done
      window.__karma__.start();
    });
  }
});
