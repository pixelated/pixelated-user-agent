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
define(['flight/lib/component', 'page/events', 'page/router/url_params'], function (defineComponent, events, urlParams) {
  'use strict';

  return defineComponent(function () {
    this.defaultAttrs({
      history: window.history
    });

    function createHash(data) {
      var hash = '/#/' + data.tag;
      if (!_.isUndefined(data.mailIdent)) {
        hash += '/mail/' + data.mailIdent;
      }
      return hash;
    }

    function createState(data, previousState) {
      return {
        tag: data.tag || (previousState && previousState.tag) || urlParams.defaultTag(),
        mailIdent: data.mailIdent,
        isDisplayNoMessageSelected: !!data.isDisplayNoMessageSelected
      };
    }

    this.pushState = function (ev, data) {
      if (!data.fromPopState) {
        var nextState = createState(data, this.attr.history.state);
        this.attr.history.pushState(nextState, '', createHash(nextState));
      }
    };

    this.popState = function (ev) {
      var state = ev.state || {};

      this.trigger(document, events.ui.tag.select, {
        tag: state.tag || urlParams.getTag(),
        mailIdent: state.mailIdent,
        fromPopState: true
      });

      if (ev.state.isDisplayNoMessageSelected) {
        this.trigger(document, events.dispatchers.rightPane.openNoMessageSelectedWithoutPushState);
      }
    };

    this.after('initialize', function () {
      this.on(document, events.router.pushState, this.pushState);
      window.onpopstate = this.popState.bind(this);
    });
  });
});
