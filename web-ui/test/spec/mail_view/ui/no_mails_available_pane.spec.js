describeComponent('mail_view/ui/no_mails_available_pane', function () {
    'use strict';

    describe('after initialization', function () {
        it('renders template', function () {
            this.setupComponent({tag: 'inbox'});
            expect(this.$node.html()).toMatch('<div class="text">NO EMAILS IN \'INBOX\'.</div>');
        });
    });
});
