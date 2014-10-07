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
define(['flight/lib/component', 'page/events', 'helpers/triggering'], function(defineComponent, events, triggering) {
  'use strict';

  return defineComponent(function() {
    this.defaultAttrs({
      middlePane: '#middle-pane'
    });

    this.refreshMailList =  function (ev, data) {
      this.trigger(document, events.ui.mails.fetchByTag, data);
    };

    this.cleanSelected = function(ev, data) {
      this.trigger(document, events.ui.mails.cleanSelected);
    };

    this.resetScroll = function() {
      this.select('middlePane').scrollTop(0);
    };

    this.updateMiddlePaneHeight = function() {
        var vh = $(window).height();
        var top = $('#main').outerHeight() + $('#top-pane').outerHeight();
        this.select('middlePane').css({height: (vh - top) + 'px'});
    };

    this.after('initialize', function () {
      this.on(document, events.dispatchers.middlePane.refreshMailList, this.refreshMailList);
      this.on(document, events.dispatchers.middlePane.cleanSelected, this.cleanSelected);
      this.on(document, events.dispatchers.middlePane.resetScroll, this.resetScroll);

      this.updateMiddlePaneHeight();
      $(window).on('resize', this.updateMiddlePaneHeight.bind(this));
    });
  });
});
