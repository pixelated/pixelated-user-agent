/*
 * Copyright (c) 2014 ThoughtWorks, Inc.
 *
 * Pixelated is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Pixelated is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
 */
'use strict';

define([
    'flight/lib/component',
    'page/events',
    'features'
  ],
  function (defineComponent, events, features) {

    function recipientsInput() {
      var EXIT_KEY_CODE_MAP = {
          8: 'backspace',
          37: 'left'
        },
        ENTER_ADDRESS_KEY_CODE_MAP = {
          9: 'tab',
          186: 'semicolon',
          188: 'comma',
          13: 'enter',
          27: 'esc',
          32: 'space'
        },
        EVENT_FOR = {
          8: events.ui.recipients.deleteLast,
          37: events.ui.recipients.selectLast
        },
        self;

      var simpleAddressMatch = /[^<\w,;]?([^\s<;,]+@[^\s>;,]+)/;
      var canonicalAddressMatch = /([^,;\s][^,;@]+<[^\s;,]+@[^\s;,]+>)/;
      var emailAddressMatch = new RegExp([simpleAddressMatch.source, '|', canonicalAddressMatch.source].join(''), 'g');

      var extractContactNames = function (response) {
          return _.map(response, function(a) { return { value: a }; });
      };

      function createEmailCompleter() {
        var emailCompleter = new Bloodhound({
          datumTokenizer: function (d) {
            return [d.value];
          },
          queryTokenizer: function (q) {
            return [q.trim()];
          },
          remote: {
            url: '/contacts?q=%QUERY',
            filter: extractContactNames
          }
        });
        emailCompleter.initialize();
        return emailCompleter;
      }

      function reset(node) {
        node.typeahead('val', '');
      }

      function caretIsInTheBeginningOfInput(input) {
        return input.selectionStart === 0;
      }

      function isExitKey(keyPressed) {
        return EXIT_KEY_CODE_MAP.hasOwnProperty(keyPressed);
      }

      function isEnterAddressKey(keyPressed) {
        return ENTER_ADDRESS_KEY_CODE_MAP.hasOwnProperty(keyPressed);
      }

      this.processSpecialKey = function (event) {
        var keyPressed = event.which;

        if (isExitKey(keyPressed) && caretIsInTheBeginningOfInput(this.$node[0])) {
          this.trigger(EVENT_FOR[keyPressed]);
          return;
        }

        if (!event.shiftKey && isEnterAddressKey(keyPressed)) {
          this.tokenizeRecipient(event);

          if ((keyPressed !== 9 /* tab */)) {
            event.preventDefault();
          }
        }

      };

      this.tokenizeRecipient = function (event) {
        if (_.isEmpty(this.$node.val().trim())) {
          return;
        }

        this.recipientSelected(null, {value: this.$node.val() });
        event.preventDefault();
      };

      this.recipientSelected = function (event, data) {
        var value = (data && data.value) || this.$node.val();
        var that = this;

        function triggerEventForEach(addresses, event) {
          _.each(addresses, function(address) {
            if (!_.isEmpty(address.trim())) {
              that.trigger(that.$node, event, { name: that.attr.name, address: address.trim() });
            }
          });
        }

        var validAddresses = this.extractValidAddresses(value);
        var invalidAddresses = this.extractInvalidAddresses(value);

        triggerEventForEach(validAddresses, events.ui.recipients.entered);
        triggerEventForEach(invalidAddresses, events.ui.recipients.enteredInvalid);

        reset(this.$node);
      };

      this.extractValidAddresses = function(rawAddresses) {
        return rawAddresses.match(emailAddressMatch);
      };

      this.extractInvalidAddresses = function(rawAddresses) {
        return rawAddresses.replace(emailAddressMatch, '').split(' ');
      };

      this.init = function () {
        this.$node.typeahead({
          hint: true,
          highlight: true,
          minLength: 1
        }, {
          source: createEmailCompleter().ttAdapter(),
          templates: {
              suggestion: function (o) { return _.escape(o.value); }
          }
        });
      };

      this.attachAndReturn = function (node, name) {
        var input = new this.constructor();
        input.initialize(node, { name: name});
        return input;
      };

      this.warnSendButtonOfInputState = function () {
        var toTrigger = _.isEmpty(this.$node.val()) ? events.ui.recipients.inputFieldIsEmpty : events.ui.recipients.inputFieldHasCharacters;
        this.trigger(document, toTrigger, { name: this.attr.name });
      };

      this.after('initialize', function () {
        self = this;
        this.init();
        this.on('typeahead:selected typeahead:autocompleted', this.recipientSelected);
        this.on(this.$node, 'blur', this.tokenizeRecipient);
        this.on(this.$node, 'keydown', this.processSpecialKey);
        this.on(this.$node, 'keyup', this.warnSendButtonOfInputState);

        this.on(document, events.dispatchers.rightPane.clear, this.teardown);
      });
    }

    return defineComponent(recipientsInput);

  }
);
