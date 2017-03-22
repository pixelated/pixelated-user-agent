import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Header } from 'src/common/header/header';

describe('Header', () => {
  let header;

  beforeEach(() => {
    const mockTranslations = key => key;
    header = shallow(<Header t={mockTranslations} />);
  });

  it('renders the header content', () => {
    expect(header.find('header').text()).toContain('Logout');
  });
});
