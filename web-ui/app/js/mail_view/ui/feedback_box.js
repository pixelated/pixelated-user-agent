/*
 * Copyright (c) 2015 ThoughtWorks, Inc.
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

define(['flight/lib/component', 'views/templates', 'page/events', 'features'],
    function (defineComponent, templates, events, features) {
  'use strict';

  return defineComponent(function () {
     this.defaultAttrs({
       'closeButton': '.close-mail-button'
     });

    this.render = function () {
      this.$node.html(templates.compose.feedback());
    };

    this.openFeedbackBox = function() {
      var stage = this.reset('feedback-box');
      this.attachTo(stage);
      this.enableFloatlabel('input.floatlabel');
      this.enableFloatlabel('textarea.floatlabel');
    };

    this.showNoMessageSelected = function() {
      this.trigger(document, events.dispatchers.rightPane.openNoMessageSelected);
    };

    this.after('initialize', function () {
      if (features.isEnabled('feedback')) {
          this.render();
          this.on(document, events.dispatchers.rightPane.openFeedbackBox, this.openFeedbackBox);
          this.on(this.select('closeButton'), 'click', this.showNoMessageSelected);
      }
    });

  });
});
