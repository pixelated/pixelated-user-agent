/*
 * Copyright (c) 2016 ThoughtWorks, Inc.
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

define(['DOMPurify', 'he'], function (DOMPurify, he) {
  'use strict';

  /**
   * Sanitizes a mail body to safe-to-display HTML
   */
  var sanitizer = {};

  sanitizer.whitelist = [{
    // highlight tag open
    pre: '&#x3C;&#x65;&#x6D;&#x20;&#x63;&#x6C;&#x61;&#x73;&#x73;&#x3D;&#x22;&#x73;&#x65;&#x61;&#x72;&#x63;&#x68;&#x2D;&#x68;&#x69;&#x67;&#x68;&#x6C;&#x69;&#x67;&#x68;&#x74;&#x22;&#x3E;',
    post: '<em class="search-highlight">'
  }, {
    // highlight tag close
    pre: '&#x3C;&#x2F;&#x65;&#x6D;&#x3E;',
    post: '</em>'
  }];

  /**
   * Adds html line breaks to a plaintext with line breaks (incl carriage return)
   *
   * @param {string} textPlainBody Plaintext input
   * @returns {string} Plaintext with HTML line breals (<br/>)
   */
  sanitizer.addLineBreaks = function (textPlainBody) {
    return textPlainBody.replace(/(\r)?\n/g, '<br/>').replace(/(&#xD;)?&#xA;/g, '<br/>');
  };

  /**
   * Runs a given dirty body through DOMPurify, thereby removing
   * potentially hazardous XSS attacks. Please be advised that this
   * will not act as a privacy leak prevention. Contained contents
   * will still point to remote sources.
   *
   * For future reference: Running DOMPurify with these parameters
   * can help mitigate some of the most widely used privacy leaks.
   * FORBID_TAGS: ['style', 'svg', 'audio', 'video', 'math'],
   * FORBID_ATTR: ['src']
   *
   * @param  {string} dirtyBody The unsanitized string
   * @return {string} Safe-to-display HTML string
   */
  sanitizer.purifyHtml = function (dirtyBody) {
    return DOMPurify.sanitize(dirtyBody, {
      SAFE_FOR_JQUERY: true,
      SAFE_FOR_TEMPLATES: true
    });
  };

  /**
   * Runs a given dirty body through he, thereby encoding everything
   * as HTML entities.
   *
   * @param  {string} dirtyBody The unsanitized string
   * @return {string} Safe-to-display HTML string
   */
  sanitizer.purifyText = function (dirtyBody) {
    var escapedBody = he.encode(dirtyBody, {
      encodeEverything: true
    });

    this.whitelist.forEach(function(entry) {
      while (escapedBody.indexOf(entry.pre) > -1) {
        escapedBody = escapedBody.replace(entry.pre, entry.post);
      }
    });

    return escapedBody;
  };

  /**
   * Calls #purify and #addLineBreaks to turn untrusted mail body content
   * into safe-to-display HTML.
   *
   * NB: HTML content is preferred to plaintext content.
   *
   * @param  {object} mail Pixelated Mail Object
   * @return {string} Safe-to-display HTML string
   */
  sanitizer.sanitize = function (mail) {
    var body;

    if (mail.htmlBody) {
      body = this.purifyHtml(mail.htmlBody);
    } else {
      body = this.purifyText(mail.textPlainBody);
      body = this.addLineBreaks(body);
    }

    return body;
  };

  /**
   * Add hooks to DOMPurify for opening links in new windows
   */
  DOMPurify.addHook('afterSanitizeAttributes', function (node) {
    // set all elements owning target to target=_blank
    if ('target' in node) {
      node.setAttribute('target', '_blank');
    }

    // set non-HTML/MathML links to xlink:show=new
    if (!node.hasAttribute('target') && (node.hasAttribute('xlink:href') || node.hasAttribute('href'))) {
      node.setAttribute('xlink:show', 'new');
    }
  });

  return sanitizer;
});
