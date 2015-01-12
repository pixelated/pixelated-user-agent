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
'use strict';

define(['helpers/monitored_ajax'], function(monitoredAjax) {
  var cachedDisabledFeatures;
  var cachedDispatcherFeatures;

  function getDisabledFeatures() {
    cachedDisabledFeatures = cachedDisabledFeatures || fetchFeatures().disabled_features;
    return cachedDisabledFeatures;
  }

  function getDispatcherFeatures() {
    cachedDispatcherFeatures = cachedDispatcherFeatures || fetchFeatures().dispatcher_features;
    return cachedDispatcherFeatures;
  }

  function fetchFeatures() {
    var features;
    monitoredAjax(this, '/features', {
      async: false,
      success: function (results){
	features = results;
      },
      error: function () {
        console.error('Could not load feature toggles');
      }
    });
    return features;
  }

  return {
    isEnabled: function (featureName) {
      return ! _.contains(getDisabledFeatures(), featureName);
    },
    isAutoRefreshEnabled: function () {
      return this.isEnabled('autoRefresh');
    },
    isLogoutEnabled: function () {
      return _.has(getDispatcherFeatures(), 'logout');
    },
    getLogoutUrl: function () {
      return getDispatcherFeatures().logout;
    }
  };
});
