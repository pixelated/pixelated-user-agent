import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { App } from 'src/login/app';
import AuthError from 'src/login/error/auth_error';
import GenericError from 'src/login/error/generic_error';
import PixelatedWelcome from 'src/login/about/pixelated_welcome';

describe('App', () => {
  let app;
  const mockTranslations = key => key;

  it('renders login form', () => {
    app = shallow(<App t={mockTranslations} />);
    expect(app.find('form').props().action).toEqual('/login');
  });

  it('renders welcome message when no error', () => {
    app = shallow(<App t={mockTranslations} />);
    expect(app.find(PixelatedWelcome).length).toEqual(1);
  });

  it('renders auth error message', () => {
    app = shallow(<App t={mockTranslations} authError />);
    expect(app.find(AuthError).length).toEqual(1);
  });

  it('renders generic error message when error', () => {
    app = shallow(<App t={mockTranslations} error />);
    expect(app.find(GenericError).length).toEqual(1);
  });

  it('does not render welcome message when error', () => {
    app = shallow(<App t={mockTranslations} error />);
    expect(app.find(PixelatedWelcome).length).toEqual(0);
  });

  it('does not render error message', () => {
    app = shallow(<App t={mockTranslations} />);
    expect(app.find(AuthError).length).toEqual(0);
    expect(app.find(GenericError).length).toEqual(0);
  });

  it('adds small logo class when error', () => {
    app = shallow(<App t={mockTranslations} error />);
    expect(app.find('.logo').props().className).toEqual('logo small-logo');
  });

  it('does not add small logo class when no error', () => {
    app = shallow(<App t={mockTranslations} />);
    expect(app.find('.logo').props().className).toEqual('logo');
  });

});
