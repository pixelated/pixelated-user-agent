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
define([], function () {

  function defaultTag() {
    return 'inbox';
  }

  function getDocumentHash() {
    return document.location.hash.replace(/\/$/, '');
  }

  function hashTag(hash) {
    if (hasMailIdent(hash)) {
      return /\/(.+)\/mail\/\d+$/.exec(getDocumentHash())[1];
    }
    return hash.substring(2);
  }


  function getTag() {
    if (document.location.hash !== '') {
      return hashTag(getDocumentHash());
    }
    return defaultTag();
  }

  function hasMailIdent() {
    return getDocumentHash().match(/mail\/\d+$/);
  }

  function getMailIdent() {
    return /mail\/(\d+)$/.exec(getDocumentHash())[1];
  }

  return {
    getTag: getTag,
    hasMailIdent: hasMailIdent,
    getMailIdent: getMailIdent,
    defaultTag: defaultTag
  };
});
