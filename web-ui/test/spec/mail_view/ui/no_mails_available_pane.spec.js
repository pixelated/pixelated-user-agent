describeComponent('mail_view/ui/no_mails_available_pane', function () {
    'use strict';

    describe('after initialization', function () {
        beforeEach(function () {
            this.setupComponent();
        });

        it('renders template', function () {
            expect(this.$node.html()).toMatch('<div class="text">NO MAILS AVAILABLE.</div>');
        });
    });
});
