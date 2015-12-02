
describeComponent('page/unread_count_title', function () {
  'use strict';
  describe('title bar', function () {
    beforeEach(function () {
      this.setupComponent('<span></span>');
    });

    it('should render template', function () {
      expect(this.$node).toExist();
      expect(this.$node.html()).toEqual('<span>(1)</span>');
    });
    
    it('should update count on mail read event', function () {
      this.component.trigger(Pixelated.events.mails.read);
        $(document).trigger(Pixelated.events.mail.read, { tags: ['someothertag'], mailbox: 'inbox' });
      expect(this.$node.html()).toEqual('<span>(1)</span>');
    });

  });
});
