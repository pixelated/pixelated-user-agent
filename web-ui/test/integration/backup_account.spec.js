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

    context('with valid email', () => {
      beforeEach(() => {
        backupAccountPage.find('input').simulate('change', {target: {value: 'test@test.com'}});
      });

      it('shows no validation error', () => {
        expect(backupAccountPage.find('InputField').props().errorText).toEqual('');
      });

      it('submit button is enabled', () => {
        expect(backupAccountPage.find('SubmitButton').props().disabled).toEqual(false);
      });
    });

    context('with invalid email', () => {
      beforeEach(() => {
        backupAccountPage.find('input').simulate('change', {target: {value: 'test'}});
      });

      it('shows validation error', () => {
        expect(backupAccountPage.find('InputField').props().errorText).toEqual('Please enter a valid email address');
      });

      it('disables submit button', () => {
        expect(backupAccountPage.find('SubmitButton').props().disabled).toEqual(true);
      });
    });

    context('with empty email', () => {
      beforeEach(() => {
        backupAccountPage.find('input').simulate('change', {target: {value: ''}});
      });

      it('shows no validation error', () => {
        expect(backupAccountPage.find('InputField').props().errorText).toEqual('');
      });

      it('disables submit button', () => {
        expect(backupAccountPage.find('SubmitButton').props().disabled).toEqual(true);
      });
    });
  });
});
