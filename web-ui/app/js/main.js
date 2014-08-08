'use strict';

requirejs.config({
  baseUrl: '../',
  paths: {
    'mail_list': 'js/mail_list',
    'page': 'js/page',
    'flight': 'bower_components/flight',
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
    'i18next': 'bower_components/i18next/i18next.amd',
    'quoted-printable': 'bower_components/quoted-printable',
    'features': 'js/features/features'
  }
});

require([
  'flight/lib/compose',
  'flight/lib/debug'
], function(compose, debug){
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
    window.Pixelated = window.Pixelated || {};
    window.Pixelated.events = events;

    compose.mixin(registry, [advice.withAdvice, withLogging]);

    debug.enable(true);
    debug.events.logAll();

    initializeDefault('');
  }
);
