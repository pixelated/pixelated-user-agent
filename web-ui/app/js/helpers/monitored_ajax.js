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

define(['page/events', 'views/i18n', 'helpers/browser'], function (events, i18n, browser) {

  'use strict';

  var messages = {
    timeout: 'a timeout occurred',
    error: 'problems talking to server',
    parseerror: 'got invalid response from server'
  };

  function monitoredAjax(on, url, config) {
    config = config || {};
    config.timeout = 60 * 1000;

    var originalBeforeSend = config.beforeSend;
    config.beforeSend = function () {
      if (originalBeforeSend) {
        originalBeforeSend();
      }
    };

    config.headers = {'X-XSRF-TOKEN': browser.getCookie('XSRF-TOKEN')};

    var originalComplete = config.complete;
    config.complete = function () {
      if (originalComplete) {
        originalComplete();
      }
    };

    return $.ajax(url, config).fail(function (xmlhttprequest, textstatus, message) {
      if (!config.skipErrorMessage) {
        var msg = (xmlhttprequest.responseJSON && xmlhttprequest.responseJSON.message) ||
          messages[textstatus] ||
          'unexpected problem while talking to server';
        on.trigger(document, events.ui.userAlerts.displayMessage, {message: i18n(msg), class: 'error'});
      }

      if (xmlhttprequest.status === 302) {
        var redirectUrl = xmlhttprequest.getResponseHeader('Location');
        browser.redirect(redirectUrl);
      } else if (xmlhttprequest.status === 401) {
        browser.redirect('/');
      }

    }.bind(this));
  }

  return monitoredAjax;

});
