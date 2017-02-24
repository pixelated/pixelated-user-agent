import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { GenericError } from 'src/login/error/generic_error';

describe('GenericError', () => {
  let genericError;
  const mockTranslations = key => key;

  beforeEach(() => {
    genericError = shallow(<GenericError t={mockTranslations} />);
  });

  it('renders error message', () => {
    expect(genericError.find('.generic-error').length).toEqual(1);
  });
});
