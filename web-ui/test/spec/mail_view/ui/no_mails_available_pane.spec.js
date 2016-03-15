describeComponent('mail_view/ui/no_mails_available_pane', function () {
    'use strict';

    describe('after initialization', function () {
        it('renders template', function () {
            this.setupComponent({tag: 'inbox'});
            expect(this.$node.html()).toMatch('<div class="no-mails-available-pane">\n    NO EMAILS IN \'INBOX\'.\n</div>');
        });

        it('show different message for search with no results', function () {
            this.setupComponent({tag: 'all', forSearch: 'search'});
            expect(this.$node.html()).toMatch('<div class="no-mails-available-pane">\n    NO RESULTS FOR: \'SEARCH\'.\n</div>');
        });

        it('show only tag information when listing all mails', function () {
            this.setupComponent({tag: 'all', forSearch: 'in:all'});
            expect(this.$node.html()).toMatch('<div class="no-mails-available-pane">\n    NO EMAILS IN \'ALL\'.\n</div>');
        });
    });
});
