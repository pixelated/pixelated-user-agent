define(['flight/lib/component', 'page/events', 'page/router/url_params'], function (defineComponent, events, urlParams) {
  'use strict';

  return defineComponent(function () {
    this.defaultAttrs({
      history: window.history
    });

    function createHash(data) {
      var hash = "/#/" + data.tag;
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

    this.smailPushState = function (ev, data) {
      if (!data.fromPopState) {
        var nextState = createState(data, this.attr.history.state);
        this.attr.history.pushState(nextState, '', createHash(nextState));
      }
    };

    this.smailPopState = function (ev) {
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
      this.on(document, events.router.pushState, this.smailPushState);
      window.onpopstate = this.smailPopState.bind(this);
    });
  });
});
