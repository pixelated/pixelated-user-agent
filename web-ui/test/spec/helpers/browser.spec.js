define(['helpers/browser'], function (browser) {
  'use strict';

    describe('browser ', function() {
      it('gets cookie', function() {
        document.cookie = 'TWISTED_SESSION=ff895ffc45a4ce140bfc5dda6c61d232; i18next=en-us';
        expect(browser.getCookie('TWISTED_SESSION')).toEqual('ff895ffc45a4ce140bfc5dda6c61d232');
        expect(browser.getCookie('i18next')).toEqual('en-us');
      });

    });
});
