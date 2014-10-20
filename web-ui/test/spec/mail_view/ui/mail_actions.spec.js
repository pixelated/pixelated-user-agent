/*global Pixelated */

describeComponent('mail_view/ui/mail_actions', function () {
  'use strict';

  var testData;

  beforeEach(function(){
    testData = Pixelated.testData();
    this.setupComponent(testData.rawMail);
  });

  it('verifies if more actions list is hidden when rendering mail view', function() {

    var moreActionsComponent = this.component.select('moreActions');
    expect(moreActionsComponent.attr('style').trim()).toEqual('display: none;');

  });

  it('show more actions list when click on view more actions button', function(){

    this.component.select('viewMoreActions').click();

    var moreActionsComponent = this.component.select('moreActions');
    expect(moreActionsComponent.attr('style').trim()).not.toEqual('display: none;');
  });

  it('triggers a show reply box event when clicking on reply-button-top', function(){

    var showReplyBoxEvent = spyOnEvent(document, Pixelated.events.ui.replyBox.showReply);

    this.component.select('replyButtonTop').click();

    expect(showReplyBoxEvent).toHaveBeenTriggeredOn(document);
  });

  it('triggers a show reply all box event when clicking on reply-button-top and hide more actions list', function(){

    var showReplyAllEvent = spyOnEvent(document, Pixelated.events.ui.replyBox.showReplyAll);

    this.component.select('viewMoreActions').click();
    this.component.select('replyAllButtonTop').click();

    expect(showReplyAllEvent).toHaveBeenTriggeredOn(document);

    var moreActionsComponent = this.component.select('moreActions');
    expect(moreActionsComponent.attr('style').trim()).toEqual('display: none;');
  });

  it('triggers a delete event when clicking on delete-button-top', function(){
    var deleteEvent = spyOnEvent(document, Pixelated.events.ui.mail.delete);

    this.component.select('viewMoreActions').click();
    this.component.select('deleteButtonTop').click();

    expect(deleteEvent).toHaveBeenTriggeredOnAndWith(document, {mail: testData.rawMail.mail});

    var moreActionsComponent = this.component.select('moreActions');
    expect(moreActionsComponent.attr('style').trim()).toEqual('display: none;');
  });

});
