import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Page } from 'src/login/page';
import AuthError from 'src/login/error/auth_error';
import GenericError from 'src/login/error/generic_error';
import Welcome from 'src/login/about/welcome';

describe('Page', () => {
  let page;
  const mockTranslations = key => key;

  it('renders login form', () => {
    page = shallow(<Page t={mockTranslations} />);
    expect(page.find('form').props().action).toEqual('/login');
  });

  it('renders welcome message when no error', () => {
    page = shallow(<Page t={mockTranslations} />);
    expect(page.find(Welcome).length).toEqual(1);
  });

  it('renders auth error message', () => {
    page = shallow(<Page t={mockTranslations} authError />);
    expect(page.find(AuthError).length).toEqual(1);
  });

  it('renders generic error message when error', () => {
    page = shallow(<Page t={mockTranslations} error />);
    expect(page.find(GenericError).length).toEqual(1);
  });

  it('does not render welcome message when error', () => {
    page = shallow(<Page t={mockTranslations} error />);
    expect(page.find(Welcome).length).toEqual(0);
  });

  it('does not render error message', () => {
    page = shallow(<Page t={mockTranslations} />);
    expect(page.find(AuthError).length).toEqual(0);
    expect(page.find(GenericError).length).toEqual(0);
  });

  it('adds small logo class when error', () => {
    page = shallow(<Page t={mockTranslations} error />);
    expect(page.find('.logo').props().className).toEqual('logo small-logo');
  });

  it('does not add small logo class when no error', () => {
    page = shallow(<Page t={mockTranslations} />);
    expect(page.find('.logo').props().className).toEqual('logo');
  });
});
