import { mount } from 'enzyme';
import expect from 'expect';
import React from 'react';
import App from 'src/common/app';
import AccountRecoveryPage from 'src/account_recovery/page';
import BackupAccountPage from 'src/backup_account/page';
import LoginPage from 'src/login/page';
import testI18n from './i18n';

describe('Translations', () => {
  context('Account Recovery Page', () => {
    it('translates all keys on admin recovery code step', () => {
      const app = mount(<App i18n={testI18n} child={<AccountRecoveryPage />} />);
      expect(app.text()).toNotContain('untranslated', 'Unstranslated message found in the text: ' + app.text());
    });

    it('translates all keys on user recovery code step', () => {
      const app = mount(<App i18n={testI18n} child={<AccountRecoveryPage />} />);
      app.find('form.admin-code').simulate('submit');

      expect(app.text()).toNotContain('untranslated', 'Unstranslated message found in the text: ' + app.text());
    });

    it('translates all keys on new password step', () => {
      const app = mount(<App i18n={testI18n} child={<AccountRecoveryPage />} />);
      app.find('form.admin-code').simulate('submit');
      app.find('form.user-code').simulate('submit');

      expect(app.text()).toNotContain('untranslated', 'Unstranslated message found in the text: ' + app.text());
    });

    it('translates all keys on backup account step', () => {
      const app = mount(<App i18n={testI18n} child={<AccountRecoveryPage />} />);
      app.find('form.admin-code').simulate('submit');
      app.find('form.user-code').simulate('submit');
      app.find('input[name="new-password"]').simulate('change', {target: {value: '11'}});
      app.find('input[name="confirm-password"]').simulate('change', {target: {value: '11'}});
      app.find('form.new-password').simulate('submit');

      expect(app.text()).toNotContain('untranslated', 'Unstranslated message found in the text: ' + app.text());
    });
  });

  context('Backup Account Page', () => {
    it('translates all key', () => {
      const app = mount(<App i18n={testI18n} child={<BackupAccountPage />} />);
      expect(app.text()).toNotContain('untranslated', 'Unstranslated message found in the text: ' + app.text());
    });
  });

  context('Login Page', () => {
    it('translates all key', () => {
      const app = mount(<App i18n={testI18n} child={<LoginPage />} />);
      expect(app.text()).toNotContain('untranslated', 'Unstranslated message found in the text: ' + app.text());
    });
  });
});
