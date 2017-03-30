import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { UserRecoveryCodeForm } from './user_recovery_code_form';

describe('UserRecoveryCodeForm', () => {
  let userRecoveryCodeForm;
  let mockNext;
  let mockPrevious;

  beforeEach(() => {
    const mockTranslations = key => key;
    mockNext = expect.createSpy();
    mockPrevious = expect.createSpy();
    userRecoveryCodeForm = shallow(
      <UserRecoveryCodeForm
        t={mockTranslations} next={mockNext} previous={mockPrevious}
      />
    );
  });

  it('renders title for user recovery code', () => {
    expect(userRecoveryCodeForm.find('h1').text()).toEqual('account-recovery.user-form.title');
  });

  it('renders description', () => {
    expect(userRecoveryCodeForm.find('p').text()).toEqual('account-recovery.user-form.description');
  });

  it('renders input for user code', () => {
    expect(userRecoveryCodeForm.find('InputField').props().label).toEqual('account-recovery.user-form.input-label');
  });

  it('renders submit button', () => {
    expect(userRecoveryCodeForm.find('SubmitButton').props().buttonText).toEqual('account-recovery.button-next');
  });

  it('submits form to next step', () => {
    userRecoveryCodeForm.find('form').simulate('submit');
    expect(mockNext).toHaveBeenCalled();
  });

  it('returns to previous step on link click', () => {
    userRecoveryCodeForm.find('BackLink').simulate('click');
    expect(mockPrevious).toHaveBeenCalled();
  });
});
