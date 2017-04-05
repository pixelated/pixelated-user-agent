import { mount } from 'enzyme';
import expect from 'expect';
import React from 'react';
import App from 'src/common/app';
import AccountRecoveryPage from 'src/account_recovery/page';
import testI18n from './i18n';

describe('Account Recovery Page', () => {
  context('New password validation', () => {
    let app;
    let accountRecoveryPage;

    beforeEach(() => {
      app = mount(<App i18n={testI18n} child={<AccountRecoveryPage />} />);
      accountRecoveryPage = app.find('Page');
      accountRecoveryPage.find('form').simulate('submit');
      accountRecoveryPage.find('form').simulate('submit');
    });

    it('shows no validation error with valid password', () => {
      accountRecoveryPage.find('input[name="new-password"]').simulate('change', { target: { value: '12345678' } });
      // workaround because of an enzyme bug https://github.com/airbnb/enzyme/issues/534
      const inputField = accountRecoveryPage.findWhere(element => element.props().name === 'new-password').find('InputField');
      expect(inputField.props().errorText).toEqual('');
    });

    it('shows validation error with invalid password', () => {
      accountRecoveryPage.find('input[name="new-password"]').simulate('change', { target: { value: '1234' } });
      const inputField = accountRecoveryPage.findWhere(element => element.props().name === 'new-password').find('InputField');
      expect(inputField.props().errorText).toEqual('A better password has at least 8 characters');
    });

    it('shows no validation error with valid confirm password', () => {
      accountRecoveryPage.find('input[name="new-password"]').simulate('change', { target: { value: '12345678' } });
      accountRecoveryPage.find('input[name="confirm-password"]').simulate('change', { target: { value: '12345678' } });
      const inputField = accountRecoveryPage.findWhere(element => element.props().name === 'confirm-password').find('InputField');
      expect(inputField.props().errorText).toEqual('');
    });

    it('shows validation error with invalid confirm password', () => {
      accountRecoveryPage.find('input[name="new-password"]').simulate('change', { target: { value: '12345678' } });
      accountRecoveryPage.find('input[name="confirm-password"]').simulate('change', { target: { value: '1234' } });
      const inputField = accountRecoveryPage.findWhere(element => element.props().name === 'confirm-password').find('InputField');
      expect(inputField.props().errorText).toEqual('Password and confirmation don\'t match');
    });

    it('disables button if empty fields', () => {
      accountRecoveryPage.find('input[name="new-password"]').simulate('change', { target: { value: '' } });
      accountRecoveryPage.find('input[name="confirm-password"]').simulate('change', { target: { value: '' } });
      expect(accountRecoveryPage.find('SubmitButton').props().disabled).toEqual(true);
    });

    it('enables button if valid fields', () => {
      accountRecoveryPage.find('input[name="new-password"]').simulate('change', { target: { value: '12345678' } });
      accountRecoveryPage.find('input[name="confirm-password"]').simulate('change', { target: { value: '12345678' } });
      expect(accountRecoveryPage.find('SubmitButton').props().disabled).toEqual(false);
    });
  });
});
