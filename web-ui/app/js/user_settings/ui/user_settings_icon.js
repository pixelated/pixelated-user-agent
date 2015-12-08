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
define(
  [
    'flight/lib/component',
    'views/templates',
    'page/events',
    'user_settings/ui/user_settings_box'
  ], function (defineComponent, templates, events, userSettingsBox) {
  'use strict';

  return defineComponent(function () {
    this.defaultAttrs({
      userSettingsBox: $('#user-settings-box')
    });

    this.render = function () {
      this.$node.html(templates.page.userSettingsIcon());
    };

    this.toggleUserSettingsBox = function() {
      if(this.attr.userSettingsBox.children().length === 0) {
        var div = $('<div>');
        $(this.attr.userSettingsBox).append(div);
        userSettingsBox.attachTo(div);
        this.attr.userSettingsInfo = userSettingsBox;
      } else {
        this.trigger(document, events.userSettings.destroyPopup);
      }
    };

    this.triggerToggleUserSettingsBox = function(e) {
      this.trigger(document, events.ui.userSettingsBox.toggle);
      e.stopPropagation();
    };

    this.after('initialize', function () {
      this.render();
      this.on('click', this.triggerToggleUserSettingsBox);
      this.on(document, events.ui.userSettingsBox.toggle, this.toggleUserSettingsBox);
    });
  });
});
