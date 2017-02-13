import { mount } from 'enzyme';
import expect from 'expect';
import React from 'react';
import App from 'src/backup_account/app';
import testI18n from './i18n'

describe('App', () => {
  let app;

  beforeEach(() => {
    app = mount(<App i18n={testI18n} />);
  });

  it('renders translated header logout text', () => {
    expect(app.find('header').text()).toContain('Logout');
  });

  it('renders translated footer text', () => {
    expect(app.find('footer').text()).toContain('Product in development. Feedback and issues to team@pixelated-project.org');
  });
});
