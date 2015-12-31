define([
  'flight/lib/component',
  'page/events'
],
function(defineComponent, events) {
'use strict';

  return defineComponent(shortcuts);

  function shortcuts() {
    function hasInputFieldFocused() {
      return $('input').is(':focus') || $('textarea').is(':focus');
    }

    function triggerOpenComposeBoxEvent() {
      if(!hasInputFieldFocused()){
        this.trigger(document, events.shortcuts.openComposeBox);
        event.preventDefault();
      }
    }

    function triggerCloseBoxEvent() {
      this.trigger(document, events.shortcuts.closeMail);
      event.preventDefault();
    }

    function focusSearchField() {
      if(!hasInputFieldFocused()) {
        this.trigger(document, events.shortcuts.focusSearchField);
        event.preventDefault();
      }
    }

    function addTag() {
      // TODO: refator to trigger an event that other component will handle
      if(!hasInputFieldFocused()) {
        event.preventDefault();
        $('#new-tag-button').click();
      }
    }

    function triggerReplyEvent() {
      if(!hasInputFieldFocused() && $('#reply-button').is(':visible')) {
        this.trigger(document, events.shortcuts.replyMail);
      }
    }

    function triggerReplyAllEvent() {
      if(!hasInputFieldFocused() && $('#reply-all-button').is(':visible')) {
        this.trigger(document, events.shortcuts.replyAllMail);
      }
    }

    function triggerForwardEvent() {
      if(!hasInputFieldFocused() && $('#forward-button').is(':visible')) {
        this.trigger(document, events.shortcuts.forwardMail);
      }
    }

    function deleteMail() {
      // TODO: refator to trigger an event that other component will handle
      $('#delete-button-top').click();
    }

    function sendMail() {
      // TODO: refator to trigger an event that other component will handle
      $('#send-button').click();
    }

    function previousMail() {
      if(!hasInputFieldFocused()) {
        // TODO: implement previous mail logic
        console.log('previous mail');
      }
    }

    function nextMail() {
      if(!hasInputFieldFocused()) {
        // TODO: implement next mail logic
        console.log('next mail');
      }
    }

    var SPECIAL_CHARACTERES = {
      13: 'ENTER',
      27: 'ESC',
      33: 'PAGE-UP',
      34: 'PAGE-DOWN',
      37: 'LEFT',
      38: 'UP',
      39: 'RIGHT',
      40: 'DOWN',
      191: '/'
    };

    var SHORTCUT_MAP =  {
      'C': triggerOpenComposeBoxEvent,
      'ESC': triggerCloseBoxEvent,
      '/': focusSearchField,
      'S': focusSearchField,
      'T': addTag,
      'R': triggerReplyEvent,
      'A': triggerReplyAllEvent,
      'F': triggerForwardEvent,
      'SHIFT+3': deleteMail,
      'CTRL+ENTER': sendMail,
      'J': previousMail,
      'UP': previousMail,
      'K': nextMail,
      'DOWN': nextMail
    };

    this.convertCodeToShortcut = function(event) {
      var shortcut = '';
      if(event.ctrlKey) {
        shortcut += 'CTRL+';
      }
      if(event.altKey) {
        shortcut += 'ALT+';
      }
      if(event.shiftKey) {
        shortcut += 'SHIFT+';
      }

      if(SPECIAL_CHARACTERES.hasOwnProperty(event.which)) {
        shortcut += SPECIAL_CHARACTERES[event.which];
      } else {
        shortcut += String.fromCharCode(event.which);
      }

      return shortcut;
    };

    this.riseEventFromShortcut = function(event) {
      var shortcut = this.convertCodeToShortcut(event);

      if(SHORTCUT_MAP.hasOwnProperty(shortcut)) {
        SHORTCUT_MAP[shortcut].apply(this);
      }
    };

    this.after('initialize', function() {
      this.on(document, 'keydown', this.riseEventFromShortcut);
    });
  }
});
