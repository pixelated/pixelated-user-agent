describeComponent('page/pix_logo', function () {
  'use strict';

  describe('pix logo', function () {
    it('should spin when loading another mail box', function () {
      this.setupComponent('<polygon id="clock1" class="logo-part-animation-off"></polygon>');
      var eventSpy = spyOnEvent(document, Pixelated.events.ui.page.spinLogo);
      $(document).trigger(Pixelated.events.ui.tag.select);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(this.component.$node.hasClass('logo-part-animation-on')).toBe(true);
    });

    it('should stop spinning after mail box is loaded', function (done) {
      this.setupComponent('<polygon id="clock1" class="logo-part-animation-on"></polygon>');
      var eventSpy = spyOnEvent(document, Pixelated.events.ui.page.stopSpinningLogo);
      $(document).trigger(Pixelated.events.mails.available);

      var component = this.component;

      setTimeout(function() {
          expect(eventSpy).toHaveBeenTriggeredOn(document);
          expect(component.$node.hasClass('logo-part-animation-off')).toBe(true);
          done();
      }, 600);
    });

    it('should spin when saving draft', function () {
      this.setupComponent('<polygon id="clock1" class="logo-part-animation-off"></polygon>');
      var eventSpy = spyOnEvent(document, Pixelated.events.ui.page.spinLogo);
      $(document).trigger(Pixelated.events.mail.saveDraft);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(this.component.$node.hasClass('logo-part-animation-on')).toBe(true);
    });

    it('should stop spinning after draft is saved', function (done) {
      this.setupComponent('<polygon id="clock1" class="logo-part-animation-on"></polygon>');
      var eventSpy = spyOnEvent(document, Pixelated.events.ui.page.stopSpinningLogo);
      $(document).trigger(Pixelated.events.mail.draftSaved);

      var component = this.component;

      setTimeout(function() {
          expect(eventSpy).toHaveBeenTriggeredOn(document);
          expect(component.$node.hasClass('logo-part-animation-off')).toBe(true);
          done();
      }, 600);
    });

    it('should spin when opening a mail message', function () {
      this.setupComponent('<polygon id="clock1" class="logo-part-animation-off"></polygon>');
      var eventSpy = spyOnEvent(document, Pixelated.events.ui.page.spinLogo);
      $(document).trigger(Pixelated.events.ui.mail.open);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(this.component.$node.hasClass('logo-part-animation-on')).toBe(true);
    });

    it('should spin when opening a draft', function () {
      this.setupComponent('<polygon id="clock1" class="logo-part-animation-off"></polygon>');
      var eventSpy = spyOnEvent(document, Pixelated.events.ui.page.spinLogo);
      $(document).trigger(Pixelated.events.dispatchers.rightPane.openDraft);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(this.component.$node.hasClass('logo-part-animation-on')).toBe(true);
    });

    it('should stop spinning after mail message is loaded', function (done) {
      this.setupComponent('<polygon id="clock1" class="logo-part-animation-on"></polygon>');
      var eventSpy = spyOnEvent(document, Pixelated.events.ui.page.stopSpinningLogo);
      $(document).trigger(Pixelated.events.mail.display);

      var component = this.component;

      setTimeout(function() {
          expect(eventSpy).toHaveBeenTriggeredOn(document);
          expect(component.$node.hasClass('logo-part-animation-off')).toBe(true);
          done();
      }, 600);
    });

    it('should spin when doing a search', function () {
      this.setupComponent('<polygon id="clock1" class="logo-part-animation-off"></polygon>');
      var eventSpy = spyOnEvent(document, Pixelated.events.ui.page.spinLogo);
      $(document).trigger(Pixelated.events.search.perform);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(this.component.$node.hasClass('logo-part-animation-on')).toBe(true);
    });
  });
});
