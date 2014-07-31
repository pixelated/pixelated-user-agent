/*
 * origin window.postMessage fails with non serializable objects, so we fallback to console.log to do the job
 */
(function () {
  'use strict';

  var originalPostMessage = window.postMessage;
  window.postMessage = function(a, b) {
    try {
      originalPostMessage(a, b);
    } catch (e) {
      console.log(a, b);
    }
  };

}());
