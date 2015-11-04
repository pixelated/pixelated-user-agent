define(['helpers/monitored_ajax'], function (monitoredAjax) {
  'use strict';
  describe('monitoredAjaxCall', function () {
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
              { message: errorMessage });
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
            { message: 'Server Message' });
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