import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Footer } from 'src/common/footer/footer';

describe('Footer', () => {
  let footer;

  beforeEach(() => {
    const mockTranslations = key => key;
    footer = shallow(<Footer t={mockTranslations} />);
  });

  it('renders the footer content', () => {
    expect(footer.find('footer').text()).toContain('footer-text');
  });
});
