define([], function() {
  'use strict';

  return function(that, event, data, on) {
    return function() {
      if(on) {
        that.trigger(on, event, data || {});
      } else {
        that.trigger(event, data || {});
      }
    };
  };
});
