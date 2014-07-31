/* global Smail */

describeComponent('mail_view/ui/draft_save_status', function () {
  'use strict';

  beforeEach(setupComponent);

  it('should be empty on initialization', function() {
    expect(this.$node.text()).toBe('');
  });

  it('should display status when saving a draft', function() {
    $(document).trigger(Smail.events.mail.saveDraft);
    expect(this.$node.text()).toBe('Saving to Drafts...');
  });

  it('should display status when draft is saved', function() {
    $(document).trigger(Smail.events.mail.draftSaved);
    expect(this.$node.text()).toBe('Draft Saved.');
  });

  it('should reset status when mail is changed since last save', function() {
    $(document).trigger(Smail.events.ui.mail.changedSinceLastSave);
    expect(this.$node.text()).toBe('');
  });
});
