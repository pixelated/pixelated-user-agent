import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { AuthError } from 'src/login/error/auth_error';

describe('AuthError', () => {
  let authError;
  const mockTranslations = key => key;

  beforeEach(() => {
    authError = shallow(<AuthError t={mockTranslations} />);
  });

  it('renders error message', () => {
    expect(authError.find('.auth-error').length).toEqual(1);
  });
});
