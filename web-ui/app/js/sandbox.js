(function () {
  'use strict';

  window.addEventListener('message', function(e) {
    var mainWindow = e.source;
    mainWindow.postMessage('data ok', e.origin);
  });

  window.onmessage = function (e) {
    if (e.data.html) {
      document.body.innerHTML = e.data.html;
    }
  };
})();
