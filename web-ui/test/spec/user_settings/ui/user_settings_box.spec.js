describeComponent('user_settings/ui/user_settings_box', function () {
  'use strict';

  beforeEach(function () {
    Pixelated.mockBloodhound();
    this.setupComponent();
    this.component.render(null, {});
  });

  it('is extra high when the logout button is present', function() {
    var features = require('features');
    spyOn(features, 'isLogoutEnabled').and.returnValue(true);

    expect(this.$node.hasClass('extra-bottom-space')).toBe(true);
  });

  it('destroy it self when the close button is clicked', function () {
    var destroyEvent = spyOnEvent(document, Pixelated.events.userSettings.destroyPopup);

    this.$node.find('.fa-close').click();

    expect(destroyEvent).toHaveBeenTriggeredOn(document);
  });
});
