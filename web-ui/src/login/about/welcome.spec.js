import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Welcome } from 'src/login/about/welcome';

describe('Welcome', () => {
  let welcome;
  const mockTranslations = key => key;

  beforeEach(() => {
    welcome = shallow(<Welcome t={mockTranslations} />);
  });

  it('renders welcome component', () => {
    expect(welcome.find('.welcome').length).toEqual(1);
  });
});
