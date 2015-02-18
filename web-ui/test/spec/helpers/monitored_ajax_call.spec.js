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
  });
});