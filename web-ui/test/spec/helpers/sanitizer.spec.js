define(['helpers/sanitizer'], function (sanitizer) {
  'use strict';

  describe('sanitizer', function () {

    describe('sanitizer.addLineBreaks', function () {
      it('should add line breaks', function () {
        var expectedOutput = 'foo<br/>bar';
        var output = sanitizer.addLineBreaks('foo\nbar');
        expect(output).toEqual(expectedOutput);
      });
    });

    describe('sanitizer.purifyHtml', function () {
      it('should fire up DOMPurify', function () {
        var expectedOutput = '123<a target="_blank">I am a dolphin!</a>';
        var output = sanitizer.purifyHtml('123<a href="javascript:alert(1)">I am a dolphin!</a>');
        expect(output).toEqual(expectedOutput);
      });
    });

    describe('sanitizer.purifyText', function () {
      it('should escape HTML', function () {
        var expectedOutput = '&#x31;&#x32;&#x33;&#x3C;&#x61;&#x3E;&#x61;&#x73;&#x64;&#x3C;&#x2F;&#x61;&#x3E;';
        var output = sanitizer.purifyText('123<a>asd</a>');
        expect(output).toEqual(expectedOutput);
      });

      it('should leave highlighted text untouched', function () {
        var expectedOutput = '<em class="search-highlight">&#x31;&#x32;&#x33;&#x3C;&#x61;&#x3E;&#x61;&#x73;&#x64;&#x3C;&#x2F;&#x61;&#x3E;</em>';
        var output = sanitizer.purifyText('<em class="search-highlight">123<a>asd</a></em>');
        expect(output).toEqual(expectedOutput);
      });
    });

    describe('sanitizer.sanitize', function () {
      it('should sanitize a plaintext mail', function () {
        var expectedOutput = '&#x31;&#x32;&#x33;&#x3C;&#x61;&#x3E;&#x61;&#x73;&#x64;&#x3C;&#x2F;&#x61;&#x3E;';
        var output = sanitizer.sanitize({
          textPlainBody: '123<a>asd</a>'
        });
        expect(output).toEqual(expectedOutput);
      });

      it('should sanitize an html mail', function () {
        var expectedOutput = '<div>123<a target="_blank">I am a dolphin!</a>foobar</div>';
        var output = sanitizer.sanitize({
          htmlBody: '<div>123<a href="javascript:alert(1)">I am a dolphin!</a>foobar</div>'
        });
        expect(output).toEqual(expectedOutput);
      });
    });

  });
});
