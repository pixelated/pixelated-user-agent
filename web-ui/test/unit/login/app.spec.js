import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { App } from 'src/login/app';
import AuthError from 'src/login/error/auth_error';
import GenericError from 'src/login/error/generic_error';

describe('App', () => {
  let app;
  const mockTranslations = key => key;

  it('renders login form', () => {
    app = shallow(<App t={mockTranslations} />);
    expect(app.find('form').props().action).toEqual('/login');
  });

  it('renders auth error message', () => {
    app = shallow(<App t={mockTranslations} authError />);
    expect(app.find(AuthError).length).toEqual(1);
  });

  it('renders generic error message', () => {
    app = shallow(<App t={mockTranslations} error />);
    expect(app.find(GenericError).length).toEqual(1);
  });

  it('does not render error message', () => {
    app = shallow(<App t={mockTranslations} />);
    expect(app.find(AuthError).length).toEqual(0);
    expect(app.find(GenericError).length).toEqual(0);
  });
});
