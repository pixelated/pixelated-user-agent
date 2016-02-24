require(['page/router/url_params'], function (urlParams) {
  'use strict';

  describe('urlParams', function () {

    beforeEach(function () {
      //preventing the hash change to fire the onpopstate event in other components
      //in this case in the router component
      window.onpopstate = function () {};
    });

    afterEach(function () {
      document.location.hash = '';
    });

    describe('getTag', function () {
      it('returns inbox if there is no tag in the url hash', function () {
        expect(urlParams.getTag()).toEqual('inbox');
      });

      it('returns the tag in the hash if there is one', function () {
        document.location.hash = '#/Drafts';

        expect(urlParams.getTag()).toEqual('Drafts');
      });

      it('returns tag with slash', function () {
        document.location.hash = '#/Events/2011';

        expect(urlParams.getTag()).toEqual('Events/2011');
      });

      it('returns tag even if there is an mail ident', function () {
        document.location.hash = '#/events/2011/mail/M-123_abc';

        expect(urlParams.getTag()).toEqual('events/2011');
      });

      it('returns the tag even if there is a trailing slash', function () {
        document.location.hash = '#/Events/';

        expect(urlParams.getTag()).toEqual('Events');
      });
    });

    describe('hasMailIdent', function () {
      it('is true if hash has mailIdent', function () {
        document.location.hash = '#/inbox/mail/M-123_abc';

        expect(urlParams.hasMailIdent()).toBeTruthy();
      });

      it('is false if hash has no mail ident', function () {
        document.location.hash = '#/Drafts';

        expect(urlParams.hasMailIdent()).toBeFalsy();
      });
    });

    describe('getMailIdent', function () {
      it('returns the mail ident that is in the hash', function () {
        document.location.hash = '#/inbox/mail/M-123_abc';

        expect(urlParams.getMailIdent()).toEqual('M-123_abc');
      });

      it('supports uppercase letters and numbers as mail id', function () {
        document.location.hash = '#/inbox/mail/123ASDADA';

        expect(urlParams.getMailIdent()).toEqual('123ASDADA');
      });
    });
  });

});
