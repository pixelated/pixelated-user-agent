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
/*global _ */

define(
  ['page/events',
   'views/i18n'],
  function(events, i18n) {
    function monitoredAjax(on, url, config) {
      if (config) {
        config.timeout = 5*1000;
      }
      return $.ajax(url, config).fail(function(xmlhttprequest, textstatus, message) {
        console.log("fails for reason: " + textstatus);
        msg = ""
        switch (textstatus) {
          case "timeout":
            msg = "a timeout occurred";
            break;
          case "error":
            msg = "problems talking to server";
            break;
          case "parseerror":
            msg = "got invalid response from server";
            break;
          default:
            msg = "unexpected problem while talking to server";
        }
        on.trigger(document, events.ui.userAlerts.displayMessage, { message: i18n(msg) });
      }.bind(this));  
    }

    return monitoredAjax;
  }
);
