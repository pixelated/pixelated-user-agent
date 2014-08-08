/*global _*/
/*global Bloodhound */
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
          32: 'space',
          13: 'enter',
          27: 'esc'
        },
        EVENT_FOR = {
          8: events.ui.recipients.deleteLast,
          37: events.ui.recipients.selectLast
        },
        self;

      var extractContactNames = function (response) {
        return _.flatten(response.contacts, function (contact) {
          var filterCriteria = contact.name ?
            function (e) {
              return { value: contact.name + ' <' + e + '>' };
            } :
            function (e) {
              return { value: e };
            };

          return _.map(contact.addresses, filterCriteria);
        });
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
        if(features.isEnabled('contacts')) {
          emailCompleter.initialize();
        }
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

        if (isEnterAddressKey(keyPressed)) {
          if (!_.isEmpty(this.$node.val())) {
            this.recipientSelected(null, { value: this.$node.val() });
            event.preventDefault();
          }
          if((keyPressed !== 9 /* tab */)) {
            event.preventDefault();
          }
        }

      };

      this.recipientSelected = function (event, data) {
        var value = (data && data.value) || this.$node.val();

        this.trigger(this.$node, events.ui.recipients.entered, { name: this.attr.name, address: value });
        reset(this.$node);
      };

      this.init = function () {
        this.$node.typeahead({
          hint: true,
          highlight: true,
          minLength: 1
        }, {
          source: createEmailCompleter().ttAdapter()
        });
      };

      this.attachAndReturn = function (node, name) {
        var input = new this.constructor();
        input.initialize(node, { name: name});
        return input;
      };

      this.warnSendButtonOfInputState = function () {
        var toTrigger = _.isEmpty(this.$node.val()) ? events.ui.recipients.inputHasNoMail : events.ui.recipients.inputHasMail;
        this.trigger(document, toTrigger, { name: this.attr.name });
      };


      this.after('initialize', function () {
        self = this;
        this.init();
        this.on('typeahead:selected typeahead:autocompleted', this.recipientSelected);
        this.on(this.$node, 'keydown', this.processSpecialKey);
        this.on(this.$node, 'keyup', this.warnSendButtonOfInputState);

        this.on(document, events.dispatchers.rightPane.clear, this.teardown);
      });
    }

    return defineComponent(recipientsInput);

  }
);
