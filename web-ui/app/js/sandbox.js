(function () {
  'use strict';

  window.onmessage = function (e) {
    if (e.data.html) {
      document.body.innerHTML = e.data.html;
      var mainWindow = e.source;
      mainWindow.postMessage('data ok', e.origin);
    }
  };
})();
