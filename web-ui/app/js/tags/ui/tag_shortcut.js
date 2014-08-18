define(
  [
    'flight/lib/component',
    'views/templates',
    'page/events',
    'tags/ui/tag_base',
    'flight/lib/utils'
  ],

  function (describeComponent, templates, events, tagBase, utils) {

    var TagShortcut =  describeComponent(tagShortcut, tagBase);

    TagShortcut.appendedTo = function (parent, data) {
      var res = new this();
      res.renderAndAttach(parent, data);
      return res;
    };

    return TagShortcut;

    function tagShortcut() {

      this.renderAndAttach = function (parent, options) {
        var linkTo = options.linkTo;

        var model = {
          tagName: linkTo.name,
          displayBadge: this.displayBadge(linkTo),
          badgeType: this.badgeType(linkTo),
          count: this.badgeType(linkTo) === 'total' ? linkTo.counts.total : (linkTo.counts.total - linkTo.counts.read),
          icon: iconFor[linkTo.name]
        };

        var rendered = templates.tags.shortcut(model);
        parent.append(rendered);

        this.initialize(parent.children().last(),options);
      };

      var iconFor = {
        'inbox': 'inbox',
        'sent': 'send',
        'drafts': 'pencil',
        'trash': 'trash-o',
        'all': 'archive'
      };

      this.selectTag = function (ev, data) {
        data.tag === this.attr.linkTo.name ? this.doSelect() : this.doUnselect();
      };

      this.doUnselect = function () {
        this.$node.removeClass('selected');
      };

      this.doSelect = function () {
        this.$node.addClass('selected');
      };

      this.doTeardown = function () {
        if (!jQuery.contains(document, this.$node[0])) {
          this.teardown();
        }
      };

      this.after('initialize', function () {
        this.on('click', function () { this.attr.trigger.triggerSelect(); });
        this.on(document, events.ui.tag.select, this.selectTag);
        this.on(document, events.tags.shortcuts.teardown, this.doTeardown);
      });

    }
  }
);
