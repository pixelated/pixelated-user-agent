/*global Handlebars */

define(['i18next'], function(i18n) {
  'use strict';

  var self = function(str) {
    return i18n.t(str);
  };

  self.get = self;

  self.init = function(path) {
    i18n.init({detectLngQS: 'lang', fallbackLng: 'en', lowerCaseLng: true, getAsync: false, resGetPath: path + 'locales/__lng__/__ns__.json'});
    Handlebars.registerHelper('t', self.get.bind(self));
  };

  return self;
});
