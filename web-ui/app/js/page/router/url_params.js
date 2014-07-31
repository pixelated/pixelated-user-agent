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
