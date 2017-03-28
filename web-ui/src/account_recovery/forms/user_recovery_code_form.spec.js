import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { UserRecoveryCodeForm } from 'src/account_recovery/forms/user_recovery_code_form';

describe('UserRecoveryCodeForm', () => {
  let userRecoveryCodeForm;

  beforeEach(() => {
    const mockTranslations = key => key;
    userRecoveryCodeForm = shallow(
      <UserRecoveryCodeForm t={mockTranslations} />
    );
  });

  it('renders title for user recovery code', () => {
    expect(userRecoveryCodeForm.find('h1').text()).toEqual('account-recovery.user-form.title');
  });
});
