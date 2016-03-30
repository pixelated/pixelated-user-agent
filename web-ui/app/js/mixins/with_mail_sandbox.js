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
define(
  ['helpers/view_helper', 'page/events'],
  function(viewHelpers, events) {
    'use strict';

    function withMailSandbox() {
      this.showMailOnSandbox = function(mail) {
        var that = this;
        var $iframe = $("#read-sandbox");
        var iframe = $iframe[0];
        var content = viewHelpers.formatMailBody(mail);

        window.addEventListener('message', function(e) {
          if (e.origin === 'null' && e.source === iframe.contentWindow) {
            that.trigger(document, events.ui.replyBox.showReplyContainer);
            that.trigger(document, events.search.highlightResults, {where: '.mail-read-view__header'});
          }
        });

        iframe.onload = function() {
          // use iframe-resizer to dynamically adapt iframe size to its content
          var config = {
            resizedCallback: scaleToFit,
            checkOrigin: false
          };
          $iframe.iFrameResize(config);

          // transform scale iframe to fit container width
          // necessary if iframe is wider than container
          function scaleToFit() {
              var parentWidth = $iframe.parent().width();
              var w = $iframe.width();
              var scale = 'none';

              // only scale html mails
              if (mail && mail.htmlBody && (w > parentWidth)) {
                  scale = parentWidth / w;
                  scale = 'scale(' + scale + ',' + scale + ')';
              }

              $iframe.css({
                  '-webkit-transform-origin': '0 0',
                  '-moz-transform-origin': '0 0',
                  '-ms-transform-origin': '0 0',
                  'transform-origin': '0 0',
                  '-webkit-transform': scale,
                  '-moz-transform': scale,
                  '-ms-transform': scale,
                  'transform': scale
              });
          }

          iframe.contentWindow.postMessage({
            html: content
          }, '*');
        };
      };
    }

    return withMailSandbox;
  }
);
