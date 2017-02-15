import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { App } from 'src/login/app';

describe('App', () => {
  let app;

  beforeEach(() => {
    const mockTranslations = key => key;
    app = shallow(<App t={mockTranslations} />);
  });

  it('renders login form', () => {
    expect(app.find('form').props().action).toEqual('/login');
  });
});
