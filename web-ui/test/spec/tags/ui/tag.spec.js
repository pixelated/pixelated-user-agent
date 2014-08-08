/*global Pixelated */
/*global _ */

describeComponent('tags/ui/tag', function () {
  'use strict';

  describe('inbox tag', function() {
    beforeEach(function () {
      setupComponent('<li></li>', {
        tag: {
          name: 'inbox',
          ident: '1',
          counts: {
            total: 100,
            read: 0
          }
        }
      });
    });

    it('selects the tag on click', function () {
      var tagSelectEvent = spyOnEvent(document, Pixelated.events.ui.tag.select);
      var cleanSelectedEvent = spyOnEvent(document, Pixelated.events.ui.mails.cleanSelected);

      this.component.$node.click();

      expect(this.component.attr.selected).toBeTruthy();
      expect(this.$node.attr('class')).toMatch('selected');
      expect(tagSelectEvent).toHaveBeenTriggeredOnAndWith(document, { tag: 'inbox' });
      expect(cleanSelectedEvent).toHaveBeenTriggeredOn(document);
    });

    it('should remove selected class when selecting a different tag', function () {
      this.$node.click();

      $(document).trigger(Pixelated.events.ui.tag.select, {tag: 'drafts'});

      expect(this.$node).not.toHaveClass('selected');
    });

    it('triggers tag selected on tag select', function () {
      var tagSelectedEvent = spyOnEvent(document, Pixelated.events.ui.tag.select);

      $(document).trigger(Pixelated.events.ui.tag.select, { tag: 'drafts'});

      expect(tagSelectedEvent).toHaveBeenTriggeredOnAndWith(document, { tag: 'drafts'});
    });

    it('increases the read count when there is an email read and the email has that tag', function () {
      $(document).trigger(Pixelated.events.mail.read, { tags: ['inbox'] });

      expect(this.component.attr.tag.counts.read).toEqual(1);
      expect(this.$node.html()).toMatch('<span class="unread-count">99</span>');
    });

    it('doesnt increase the read count when the read email doesnt have the tag', function () {
      $(document).trigger(Pixelated.events.mail.read, { tags: ['amazing']});

      expect(this.component.attr.tag.counts.read).toEqual(0);
      expect(this.$node.html()).not.toMatch('<span class="unread-count">99</span>');
    });

    it('doesnt display the unread count when there are no unreads', function () {
      this.component.attr.tag.counts.read = 100;
      $(document).trigger(Pixelated.events.mail.read, { tags: ['inbox']});
      expect(this.$node.html()).not.toMatch('"unread-count"');
    });
  });

  describe('drafts tag', function () {
    var containerFordrafts;
    beforeEach(function () {
      setupComponent('<li></li>', {
        tag: {
          name: 'drafts',
          ident: '42',
          counts: {
            total: 100,
            read: 50
          }
        }
      });
    });

    it('shows the total count instead of the unread count', function () {
      $(document).trigger(Pixelated.events.mail.read, { tags: ['drafts']});
      expect(this.$node.html()).toMatch('<span class="total-count">100</span>');
      expect(this.$node.html()).not.toMatch('"unread-count"');
    });
  });

  describe('all tag', function(){
    beforeEach(function () {
      setupComponent('<li></li>', {
        tag: {
          name: 'all',
          ident: '45',
          counts: {
            total: 100,
            read: 50
          }
        }
      });
    });

    it('adds searching class when user is doing a search', function(){
      $(document).trigger(Pixelated.events.search.perform, {});
      expect(this.$node.attr('class')).toMatch('searching');
    });

    it('removes searching class when user searches for empty string', function(){
      $(document).trigger(Pixelated.events.search.perform, {});
      $(document).trigger(Pixelated.events.search.empty);
      expect(this.$node.attr('class')).not.toMatch('searching');
    });

    it('removes searching class when user clicks in any tag', function(){
      $(document).trigger(Pixelated.events.search.perform, {});
      this.$node.click();
      expect(this.$node.attr('class')).not.toMatch('searching');
    });

  });

  _.each(['sent', 'trash'], function(tag_name) {
    describe(tag_name + ' tag', function() {
      beforeEach(function () {
        setupComponent('<li></li>', {
          tag: {
            name: tag_name,
            ident: '42',
            counts: {
              total: 100,
              read: 50
            }
          }
        });
      });

      it('doesn\'t display unread count for special folder', function () {
        $(document).trigger(Pixelated.events.mail.read, { tags: [tag_name]});
        expect(this.$node.html()).not.toMatch('unread-count');
      });

      it('doesn\'t display read count for special folder', function () {
        $(document).trigger(Pixelated.events.mail.read, { tags: [tag_name]});
        expect(this.$node.html()).not.toMatch('total-count');
      });
    });
  });
});
