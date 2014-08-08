describeComponent("tags/ui/tag_shortcut", function () {

  var parent, shortcut, component, TagShortcut;

  beforeEach(function () {
    TagShortcut = require('tags/ui/tag_shortcut');

    component = jasmine.createSpyObj('tagComponent', ['triggerSelect']);
    parent = $("<ul>");
    shortcut = TagShortcut.appendedTo(parent, { linkTo: { name: 'inbox', counts: { total: 15 }}, trigger: component });
  });

  it('renders the shortcut inside the parent', function () {
    expect(parent.html()).toMatch('<a title="inbox">');
    expect(parent.html()).toMatch('<i class="fa fa-inbox"></i>');
    expect(parent.html()).toMatch('<div class="shortcut-label">inbox</div>');
  });

  it('selects and unselect on tag.select', function () {
    $(document).trigger(Pixelated.events.ui.tag.select, { tag: 'inbox'});

    expect(shortcut.$node).toHaveClass("selected");

    $(document).trigger(Pixelated.events.ui.tag.select, { tag: 'sent'});

    expect(shortcut.$node).not.toHaveClass("selected");
  });

  it('delegates the click to linked tag', function (){
    shortcut.$node.click();

    expect(component.triggerSelect).toHaveBeenCalled();
  });

});
