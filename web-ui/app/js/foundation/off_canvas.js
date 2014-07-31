define(['flight/lib/component', 'page/events'], function (defineComponent, events) {

  return defineComponent(function() {

    this.toggleSlider = function (){
      $('.off-canvas-wrap').foundation('offcanvas', 'toggle', 'move-right');
    };

    this.closeSlider = function (){
      if ($('.off-canvas-wrap').attr('class').indexOf('move-right') > -1) {
        $('.off-canvas-wrap').foundation('offcanvas', 'toggle', 'move-right');
      }
    };

    this.after('initialize', function () {
      this.on($('.left-off-canvas-toggle'), 'click', this.toggleSlider);
      this.on($('#middle-pane-container'), 'click', this.closeSlider);
      this.on($('#right-pane'), 'click', this.closeSlider);
    });
  });
});
