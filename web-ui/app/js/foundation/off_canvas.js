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
define(['flight/lib/component', 'page/events'], function (defineComponent, events) {

  return defineComponent(function() {

    this.toggleSlideContent = function (ev) {
      ev.preventDefault();
	  $('.left-off-canvas-toggle').click();
	  if ($('#custom-tag-list').hasClass('expanded')) {
	    $('#custom-tag-list').removeClass('expanded');
	  } else {
	    $('#custom-tag-list').addClass('expanded');
	  }
    }

    this.after('initialize', function () {
      this.on($('#middle-pane-container'), 'click', this.toggleSlideContent);
      this.on($('#right-pane'), 'click', this.toggleSlideContent);
      this.on($('.side-nav-toggle'), 'click', this.toggleSlideContent);
    });
  });
});
