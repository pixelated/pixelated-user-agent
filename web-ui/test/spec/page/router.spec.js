describeComponent('page/router', function () {
  'use strict';

  var fakeHistory;

  describe('on router:pushState coming from a tag selection', function () {
    beforeEach(function () {
      fakeHistory = jasmine.createSpyObj('history', ['pushState']);
      this.setupComponent({history: fakeHistory});
    });

    it('pushes the state with the tag and the url', function () {
      $(document).trigger(Pixelated.events.router.pushState, { tag: 'inbox'});

      expect(fakeHistory.pushState).toHaveBeenCalledWith(jasmine.objectContaining({ tag: 'inbox' }), '', '/#/inbox');
    });

    it('pushes the state with mailIdent', function () {
      $(document).trigger(Pixelated.events.router.pushState, { tag: 'inbox', mailIdent: 1});

      expect(fakeHistory.pushState).toHaveBeenCalledWith(jasmine.objectContaining({ tag: 'inbox', mailIdent: 1 }), '', '/#/inbox/mail/1');
    });

    it('pushes the state with mailIdent even if mail ident is 0 (that happens for drafts)', function () {
      $(document).trigger(Pixelated.events.router.pushState, { tag: 'inbox', mailIdent: 0});

      expect(fakeHistory.pushState).toHaveBeenCalledWith(jasmine.objectContaining({ tag: 'inbox', mailIdent: 0 }), '', '/#/inbox/mail/0');
    });

    it('pushes the state with the displayNoMessage boolean forwarded from the event', function () {
      $(document).trigger(Pixelated.events.router.pushState, { tag: 'inbox', mailIdent: 0});

      expect(fakeHistory.pushState).toHaveBeenCalledWith(jasmine.objectContaining({ isDisplayNoMessageSelected: false}), '', '/#/inbox/mail/0');

      $(document).trigger(Pixelated.events.router.pushState, { tag: 'inbox', mailIdent: 0, isDisplayNoMessageSelected: true});

      expect(fakeHistory.pushState).toHaveBeenCalledWith(jasmine.objectContaining({ isDisplayNoMessageSelected: true}), '', '/#/inbox/mail/0');
    });

    it('when popping a state with no tag should select tag from url', function () {
      var urlParams = require('page/router/url_params');
      spyOn(urlParams, 'getTag').and.returnValue('tag');

      var selectTagEvent = spyOnEvent(document, Pixelated.events.ui.tag.select);

      this.component.popState({ state: {tag: undefined} });

      expect(selectTagEvent).toHaveBeenTriggeredOnAndWith(document, jasmine.objectContaining({ tag: 'tag'}));
    });

    it('when popping a state triggers the displayNoMessage pane if required', function () {
      var urlParams = require('page/router/url_params');
      spyOn(urlParams, 'getTag').and.returnValue('tag');

      var displayNoMessageEvent = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openNoMessageSelectedWithoutPushState);

      this.component.popState({ state: {tag: undefined, isDisplayNoMessageSelected: false} });

      expect(displayNoMessageEvent).not.toHaveBeenTriggeredOn(document);

      this.component.popState({ state: {tag: undefined, isDisplayNoMessageSelected: true} });

      expect(displayNoMessageEvent).toHaveBeenTriggeredOn(document);
    });

  });

});
