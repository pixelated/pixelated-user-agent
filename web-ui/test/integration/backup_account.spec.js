import { mount } from 'enzyme';
import expect from 'expect';
import React from 'react';
import App from 'src/common/app';
import BackupAccountPage from 'src/backup_account/page';
import testI18n from './i18n';

describe('Backup account email validation', () => {
  context('Backup Account Page', () => {
    let app, backupAccountPage;

    beforeEach(() => {
      app = mount(<App i18n={testI18n} child={<BackupAccountPage />} />);
      backupAccountPage = app.find('Page');
    });

    it('shows no error and enables submit button when a valid email is entered', () => {
      backupAccountPage.find('input').simulate('change', {target: {value: 'test@test.com'}});
      expect(backupAccountPage.find('InputField').props().errorText).toEqual('');
      expect(backupAccountPage.find('SubmitButton').props().disabled).toEqual(false);
    });

    it('shows error and disables submit button on invalid email', () => {
      backupAccountPage.find('input').simulate('change', {target: {value: 'test'}});
      expect(backupAccountPage.find('InputField').props().errorText).toEqual('Your email is invalid');
      expect(backupAccountPage.find('SubmitButton').props().disabled).toEqual(true);
    });

    it('shows no error and disables submit button when email is empty', () => {
      backupAccountPage.find('input').simulate('change', {target: {value: ''}});
      expect(backupAccountPage.find('InputField').props().errorText).toEqual('');
      expect(backupAccountPage.find('SubmitButton').props().disabled).toEqual(true);
    });
  });
});
