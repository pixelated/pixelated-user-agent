/*global _ */

'use strict';

define(['lib/html-sanitizer'], function (htmlSanitizer) {
  var tagAndAttributeWhitelist = {
    'p': ['style'],
    'div': ['style'],
    'a': ['href', 'style'],
    'span': ['style'],
    'font': ['face', 'size', 'style'],
    'img': ['title'],
    'em': [],
    'b': [],
    'strong': ['style'],
    'table': ['style'],
    'tr': ['style'],
    'td': ['style'],
    'th': ['style'],
    'tbody': ['style'],
    'thead': ['style'],
    'dt': ['style'],
    'dd': ['style'],
    'dl': ['style'],
    'h1': ['style'],
    'h2': ['style'],
    'h3': ['style'],
    'h4': ['style'],
    'h5': ['style'],
    'h6': ['style'],
    'br': [],
    'blockquote': ['style'],
    'label': ['style'],
    'form': ['style'],
    'ol': ['style'],
    'ul': ['style'],
    'li': ['style'],
    'input': ['style', 'type', 'name', 'value']
  };

  function filterAllowedAttributes (tagName, attributes) {
    var i, attributesAndValues = [];

    for (i = 0; i < attributes.length; i++) {
      if (tagAndAttributeWhitelist[tagName] &&
        _.contains(tagAndAttributeWhitelist[tagName], attributes[i])) {
        attributesAndValues.push(attributes[i]);
        attributesAndValues.push(attributes[i+1]);
      }
    };

    return attributesAndValues;
  };

  function tagPolicy (tagName, attributes) {
    if (!tagAndAttributeWhitelist[tagName]) {
      return null;
    }

    return {
      tagName: tagName,
      attribs: filterAllowedAttributes(tagName, attributes)
    };
  }

  return {
    tagPolicy: tagPolicy,
    sanitize: htmlSanitizer.html.sanitizeWithPolicy
  };
});
