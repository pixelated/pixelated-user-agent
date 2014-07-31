'use strict';

define(['flight/lib/component', 'page/events'], function (describeComponent, events) {

  return describeComponent(paneContractExpand);

  function paneContractExpand() {
    this.defaultAttrs({
      RIGHT_PANE_EXPAND_CLASSES: 'small-7 medium-7 large-7 columns',
      RIGHT_PANE_CONTRACT_CLASSES: 'small-7 medium-4 large-4 columns',
      MIDDLE_PANE_EXPAND_CLASSES: 'small-5 medium-8 large-8 columns no-padding',
      MIDDLE_PANE_CONTRACT_CLASSES: 'small-5 medium-5 large-5 columns no-padding'
    });

    this.expandMiddlePaneContractRightPane = function () {
      $('#middle-pane-container').attr('class', this.attr.MIDDLE_PANE_EXPAND_CLASSES);
      $('#right-pane').attr('class', this.attr.RIGHT_PANE_CONTRACT_CLASSES);
    };

    this.contractMiddlePaneExpandRightPane = function () {
      $('#middle-pane-container').attr('class', this.attr.MIDDLE_PANE_CONTRACT_CLASSES);
      $('#right-pane').attr('class', this.attr.RIGHT_PANE_EXPAND_CLASSES);
    };

    this.after('initialize', function () {
      this.on(document, events.ui.mail.open, this.contractMiddlePaneExpandRightPane);
      this.on(document, events.dispatchers.rightPane.openComposeBox, this.contractMiddlePaneExpandRightPane);
      this.on(document, events.dispatchers.rightPane.openDraft, this.contractMiddlePaneExpandRightPane);
      this.on(document, events.dispatchers.rightPane.openNoMessageSelected, this.expandMiddlePaneContractRightPane);
      this.expandMiddlePaneContractRightPane()
    });

  }
});
