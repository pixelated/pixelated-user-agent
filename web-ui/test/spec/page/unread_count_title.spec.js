
describeComponent('page/unread_count_title', function () {
  'use strict';
  describe('unread count on title bar', function () {

    beforeEach(function () {
      document.title = 'example@pixelated-project.org';
      this.setupComponent();
    });

    it('listens to mails available event', function () {
      this.component.trigger(Pixelated.events.mails.available, {mails: [], tag: 'inbox'});
      expect(this.component.getTitleText()).toEqual('Inbox - example@pixelated-project.org');
    });

    it('only considers unread mails', function () {
      var readMail = {'status': ['read']};
      this.component.trigger(Pixelated.events.mails.available, {mails: [readMail], tag: 'inbox'});
      expect(this.component.getTitleText()).toEqual('Inbox - example@pixelated-project.org');
    });

    it('update for one unread email', function () {
      var mails = [{'status': ['read']}, {'status': []}];
      this.component.trigger(Pixelated.events.mails.available, {mails: mails, tag: 'inbox'});
      expect(this.component.getTitleText()).toEqual('Inbox (1) - example@pixelated-project.org');
    });

    it('update for more than one unread email', function () {
      var mails = [{'status': ['read']}, {'status': []}, {'status': []}];
      this.component.trigger(Pixelated.events.mails.available, {mails: mails, tag: 'inbox'});
      expect(this.component.getTitleText()).toEqual('Inbox (2) - example@pixelated-project.org');
    });

    it('update for more than one unread email', function () {
      var mails = [{'status': ['read']}, {'status': []}, {'status': []}];
      this.component.trigger(Pixelated.events.mails.available, {mails: mails, tag: 'inbox'});
      expect(this.component.getTitleText()).toEqual('Inbox (2) - example@pixelated-project.org');
    });

    it('decreases unread count', function () {
      document.title = 'Inbox (2) - example@pixelated-project.org';
      var mails = [{'status': ['read']}, {'status': ['read']}];
      this.component.trigger(Pixelated.events.mails.available, {mails: mails, tag: 'inbox'});
      expect(this.component.getTitleText()).toEqual('Inbox - example@pixelated-project.org');
    });
  });
});
