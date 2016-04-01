describeMixin('mixins/with_mail_sandbox', function() {
  'use strict';

  beforeEach(function() {
    this.setupComponent('<iframe id="read-sandbox" sandbox="allow-popups allow-scripts" src scrolling="no"></iframe>');
    var iframe = document.querySelector('iframe');
    var template = ['',
      '<!DOCTYPE html>',
      '<html>',
      '<head>',
      '<meta charset="utf-8">',
      '<script>(function () {',
        '\'use strict\'',
        ';window.onmessage = function (e) {',
          'if (e.data.html) {',
            'var mainWindow = e.source;',
            'mainWindow.postMessage(\'data ok\', e.origin);',
          '}',
        '};',
      '})();',
    '</script>',
    '</head>',
    '<body>',
    '</body>',
    '</html>'].join('');
    iframe.src = URL.createObjectURL(new Blob([template], {type: "text/html"}));
  });

  it('should open reply container', function (done) {
    var showContainerEvent = spyOnEvent(document, Pixelated.events.ui.replyBox.showReplyContainer);
    this.component.showMailOnSandbox(Pixelated.testData().parsedMail.html);
    setTimeout(function() {
      expect(showContainerEvent).toHaveBeenTriggeredOn(document);
      done();
    }, 200);
  });

});
