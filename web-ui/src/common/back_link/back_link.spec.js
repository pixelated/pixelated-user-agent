import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import BackLink from 'src/common/back_link/back_link';

describe('BackLink', () => {
  context('as link', () => {
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

  context('as button', () => {
    let backLink;
    let mockClick;

    beforeEach(() => {
      mockClick = expect.createSpy();
      backLink = shallow(<BackLink text='Back to inbox' onClick={mockClick} />);
    });

    it('renders button with text', () => {
      expect(backLink.find('button').text()).toEqual('Back to inbox');
    });

    it('adds button click event', () => {
      backLink.find('button').simulate('click');
      expect(mockClick).toHaveBeenCalled();
    });
  });
});
