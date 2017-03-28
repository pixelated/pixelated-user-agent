import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { AdminRecoveryCodeForm } from './admin_recovery_code_form';

describe('AdminRecoveryCodeForm', () => {
  let adminRecoveryCodeForm;
  let mockNext;

  beforeEach(() => {
    const mockTranslations = key => key;
    mockNext = expect.createSpy();
    adminRecoveryCodeForm = shallow(
      <AdminRecoveryCodeForm t={mockTranslations} next={mockNext} />
    );
  });

  it('renders title for admin recovery code', () => {
    expect(adminRecoveryCodeForm.find('h1').text()).toEqual('account-recovery.admin-form.title');
  });

  it('renders tips for retrieving recovery code', () => {
    expect(adminRecoveryCodeForm.find('li').length).toEqual(3);
  });

  it('renders input field for admin code', () => {
    expect(adminRecoveryCodeForm.find('InputField').props().name).toEqual('admin-code');
  });

  it('renders button for next step', () => {
    expect(adminRecoveryCodeForm.find('SubmitButton').props().buttonText).toEqual('account-recovery.admin-form.button');
  });

  it('submits form to next step', () => {
    adminRecoveryCodeForm.find('form').simulate('submit');
    expect(mockNext).toHaveBeenCalled();
  });
});
