define(['helpers/monitored_ajax'], function (monitoredAjax) {
  'use strict';
  describe('monitoredAjaxCall', function () {

    describe('default configs', function () {

     it('should always attach the xsrf token in the header', function () {
       var component = { trigger: function () {}};
       var d = $.Deferred();
       spyOn($, 'ajax').and.returnValue(d);
       document.cookie = 'XSRF-TOKEN=ff895ffc45a4ce140bfc5dda6c61d232; i18next=en-us';
       var anyUrl = '/';

       monitoredAjax(component, anyUrl, {});

       expect($.ajax.calls.mostRecent().args[1].headers).toEqual({ 'X-XSRF-TOKEN' : 'ff895ffc45a4ce140bfc5dda6c61d232' });

     });

     });

    describe('when dealing with errors', function () {

      _.each(
        {
         timeout: 'a timeout occurred',
         error: 'problems talking to server',
         parseerror: 'got invalid response from server'
        }, function (errorMessage, errorType) {
        it('shows message for a server ' + errorType, function () {
          var component = { trigger: function () {}};
          spyOn(component, 'trigger');
          var d = $.Deferred();
          spyOn($, 'ajax').and.returnValue(d);

          monitoredAjax(component, '/', {});
          d.reject({ responseJSON: {}}, errorType, '');

          expect(component.trigger).toHaveBeenCalledWith(document, Pixelated.events.ui.userAlerts.displayMessage,
              { message: errorMessage, class: 'error' });
        });
      });

      it('shows the error message sent by the server if it exists', function () {
        var component = { trigger: function () {}};
        spyOn(component, 'trigger');
        var d = $.Deferred();
        spyOn($, 'ajax').and.returnValue(d);

        monitoredAjax(component, '/', {});
        d.reject({ responseJSON: { message: 'Server Message'}}, 'error', '');

        expect(component.trigger).toHaveBeenCalledWith(document, Pixelated.events.ui.userAlerts.displayMessage,
            { message: 'Server Message', class: 'error' });
      });
    });

    describe('when user seems to be logged out', function () {
      var component, browser;

      beforeEach(function () {
        component = { trigger: function () {}};
        browser = require('helpers/browser');

      });

      it('will redirect the browser to the location specified', function () {
        var redirectUrl = '/some/redirect/url';
        var deferred = $.Deferred();
        spyOn($, 'ajax').and.returnValue(deferred);
        var spyRedirect = spyOn(browser, 'redirect').and.returnValue($.Deferred());

        monitoredAjax(component, '/some/url', {});

        deferred.reject({status: 302, getResponseHeader: function (_) {return redirectUrl;}}, '', '');

        expect(spyRedirect).toHaveBeenCalled();
        expect(spyRedirect.calls.mostRecent().args[0]).toEqual(redirectUrl);
      });

      it ('will redirect the browser to root if authentication is required', function () {
        var redirectUrl = '/';
        var deferred = $.Deferred();
        spyOn($, 'ajax').and.returnValue(deferred);
        var spyRedirect = spyOn(browser, 'redirect').and.returnValue($.Deferred());

        monitoredAjax(component, '/some/url', {});

        deferred.reject({status: 401}, '', '');

        expect(spyRedirect).toHaveBeenCalled();
        expect(spyRedirect.calls.mostRecent().args[0]).toEqual(redirectUrl);
      });

    });
  });
});
