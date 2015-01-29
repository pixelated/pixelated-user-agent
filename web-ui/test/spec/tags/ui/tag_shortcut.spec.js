/* global jasmine */
/* global Pixelated */

describeComponent('tags/ui/tag_shortcut', function () {
  'use strict';

  var parent, shortcut, component, TagShortcut;

  beforeEach(function () {
    TagShortcut = require('tags/ui/tag_shortcut');

    component = jasmine.createSpyObj('tagComponent', ['triggerSelect']);
    parent = $('<ul>');
    $('body').append(parent);
    shortcut = TagShortcut.appendedTo(parent, { tag: { name: 'inbox', counts: { total: 15 }}, trigger: component });
  });

  afterEach(function () {
    $('body')[0].removeChild(parent[0]);
  });

  it('renders the shortcut inside the parent', function () {
    expect(parent.html()).toMatch('<i class="fa fa-inbox"></i>');
    expect(parent.html()).toMatch('<div class="shortcut-label">inbox</div>');
  });

  it('selects and unselect on tag.select', function () {
    $(document).trigger(Pixelated.events.ui.tag.select, { tag: 'inbox'});

    expect(shortcut.$node).toHaveClass('selected');

    $(document).trigger(Pixelated.events.ui.tag.select, { tag: 'sent'});

    expect(shortcut.$node).not.toHaveClass('selected');
  });

  it('delegates the click to linked tag', function (){
    shortcut.$node.click();

    expect(component.triggerSelect).toHaveBeenCalled();
  });

  it('teardown shortcuts on event but only if they are not in the DOM', function () {
    parent.empty();
    var shortcutAddedAfterEmptyingParent = TagShortcut.appendedTo(parent, { tag: { name: 'inbox', counts: { total: 15 }}, trigger: component });
    // by now shorcut is not in the DOM anymore but shortcutAddedAfterEmptyingParent is

    spyOn(shortcut, 'teardown').and.callThrough();
    spyOn(shortcutAddedAfterEmptyingParent, 'teardown').and.callThrough();

    $(document).trigger(Pixelated.events.tags.shortcuts.teardown);

    expect(shortcut.teardown).toHaveBeenCalled();
    expect(shortcutAddedAfterEmptyingParent.teardown).not.toHaveBeenCalled();
  });
});

