(function () {
  'use strict';

  window.onmessage = function (e) {
    if (e.data.html) {
      document.body.innerHTML = e.data.html;
    }
  };
})();
