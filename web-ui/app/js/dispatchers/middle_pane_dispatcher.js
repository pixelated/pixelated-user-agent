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
        var top = $("#main").outerHeight() + $("#top-pane").outerHeight();
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
