import expect from 'expect';
import Util from 'src/common/util';

describe('Utils', () => {
  describe('.hasQueryParameter', () => {
    global.window = {
      location: {
        search: '?auth-error&lng=pt-BR'
      }
    };

    it('checks if param included in query parameters', () => {
      expect(Util.hasQueryParameter('auth-error')).toBe(true);
    });

    it('checks if param not included in query parameters', () => {
      expect(Util.hasQueryParameter('error')).toBe(false);
    });
  });
});
