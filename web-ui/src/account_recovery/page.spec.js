import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';

import { Page } from 'src/account_recovery/page';
import Header from 'src/common/header/header';
import Footer from 'src/common/footer/footer';

import AdminRecoveryCodeFormWrapper from './admin_recovery_code_form/admin_recovery_code_form';
import UserRecoveryCodeFormWrapper from './user_recovery_code_form/user_recovery_code_form';
import NewPasswordFormWrapper from './new_password_form/new_password_form';

describe('Account Recovery Page', () => {
  let page;

  beforeEach(() => {
    const mockTranslations = key => key;
    page = shallow(<Page t={mockTranslations} />);
  });

  it('renders account recovery page title', () => {
    expect(page.props().title).toEqual('account-recovery.page-title');
  });

  it('renders header without logout button', () => {
    expect(page.find(Header).props().renderLogout).toEqual(false);
  });

  it('renders footer', () => {
    expect(page.find(Footer).length).toEqual(1);
  });

  context('main content', () => {
    let pageInstance;

    beforeEach(() => {
      pageInstance = page.instance();
    });

    it('renders admin recovery code form as default form', () => {
      expect(page.find(AdminRecoveryCodeFormWrapper).length).toEqual(1);
      expect(page.find(UserRecoveryCodeFormWrapper).length).toEqual(0);
      expect(page.find(NewPasswordFormWrapper).length).toEqual(0);
    });

    it('renders user recovery code form when admin code submitted', () => {
      pageInstance.nextStep({ preventDefault: () => {} });

      expect(page.find(UserRecoveryCodeFormWrapper).length).toEqual(1);
    });

    it('returns to admin code form on user code form back link', () => {
      pageInstance.nextStep({ preventDefault: () => {} });
      pageInstance.previousStep();

      expect(page.find(AdminRecoveryCodeFormWrapper).length).toEqual(1);
    });

    it('renders new password form when user code submitted', () => {
      pageInstance.nextStep({ preventDefault: () => {} });
      pageInstance.nextStep({ preventDefault: () => {} });

      expect(page.find(NewPasswordFormWrapper).length).toEqual(1);
    });

    it('returns to user code form on new password form back link', () => {
      pageInstance.nextStep({ preventDefault: () => {} });
      pageInstance.nextStep({ preventDefault: () => {} });
      pageInstance.previousStep();

      expect(page.find(UserRecoveryCodeFormWrapper).length).toEqual(1);
    });
  });
});
