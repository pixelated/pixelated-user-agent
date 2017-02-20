import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { App } from 'src/login/app';

describe('App', () => {
  let app;
  const mockTranslations = key => key;

  beforeEach(() => {
    app = shallow(<App t={mockTranslations} />);
  });

  it('renders login form', () => {
    expect(app.find('form').props().action).toEqual('/login');
  });

  it('renders auth error message', () => {
    app = shallow(<App t={mockTranslations} authError />);
    expect(app.find('.error').length).toEqual(1);
  });

  it('does not render auth error message', () => {
    expect(app.find('.error').length).toEqual(0);
  });
});
