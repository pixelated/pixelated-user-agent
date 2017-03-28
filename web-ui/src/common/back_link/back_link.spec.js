import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import BackLink from 'src/common/back_link/back_link';

describe('BackLink', () => {
  let backLink;

  beforeEach(() => {
    backLink = shallow(<BackLink text='Back to inbox' href='/' />);
  });

  it('renders link with text', () => {
    expect(backLink.find('a').text()).toEqual('Back to inbox');
  });

  it('adds link action', () => {
    expect(backLink.find('a').props().href).toEqual('/');
  });
});
