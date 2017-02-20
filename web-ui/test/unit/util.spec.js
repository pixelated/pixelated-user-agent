import expect from 'expect';
import Util from 'src/util';

describe('Utils', () => {
  describe('.hasQueryParameter', () => {
    global.window = {
      location: {
        search: '?auth&lng=pt-BR'
      }
    };

    it('checks if param included in query parameters', () => {
      expect(Util.hasQueryParameter('auth')).toBe(true);
    });

    it('checks if param not included in query parameters', () => {
      expect(Util.hasQueryParameter('error')).toBe(false);
    });
  });
});
