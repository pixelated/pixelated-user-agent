import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import fetchMock from 'fetch-mock';
import { NewPasswordForm } from './new_password_form';

describe('NewPasswordForm', () => {
  let newPasswordForm;
  let mockPrevious;
  let mockNext;
  let mockTranslations;

  beforeEach(() => {
    mockTranslations = key => key;
    mockPrevious = expect.createSpy();
    newPasswordForm = shallow(
      <NewPasswordForm t={mockTranslations} previous={mockPrevious} userCode='def234' username='alice' />
    );
  });

  it('renders title for new password form', () => {
    expect(newPasswordForm.find('h1').text()).toEqual('account-recovery.new-password-form.title');
  });

  it('renders input for new password', () => {
    expect(newPasswordForm.find('InputField').at(0).props().type).toEqual('password');
    expect(newPasswordForm.find('InputField').at(0).props().label).toEqual('account-recovery.new-password-form.input-label1');
  });

  it('renders input to confirm new password', () => {
    expect(newPasswordForm.find('InputField').at(1).props().type).toEqual('password');
    expect(newPasswordForm.find('InputField').at(1).props().label).toEqual('account-recovery.new-password-form.input-label2');
  });

  it('renders submit button', () => {
    expect(newPasswordForm.find('SubmitButton').props().buttonText).toEqual('account-recovery.button-next');
  });

  it('returns to previous step on link click', () => {
    newPasswordForm.find('BackLink').simulate('click');
    expect(mockPrevious).toHaveBeenCalled();
  });

  describe('Submit', () => {
    beforeEach((done) => {
      mockNext = expect.createSpy().andCall(() => done());
      newPasswordForm = shallow(
        <NewPasswordForm t={mockTranslations} previous={mockPrevious} userCode='def234' next={mockNext} username='alice' />
      );
      fetchMock.post('/account-recovery', 200);
      newPasswordForm.find('InputField[name="new-password"]').simulate('change', { target: { value: '123' } });
      newPasswordForm.find('InputField[name="confirm-password"]').simulate('change', { target: { value: '456' } });
      newPasswordForm.find('form').simulate('submit', { preventDefault: expect.createSpy() });
    });

    it('posts to account recovery', () => {
      expect(fetchMock.called('/account-recovery')).toBe(true, 'POST was not called');
    });

    it('sends username as content', () => {
      expect(fetchMock.lastOptions('/account-recovery').body).toContain('"username":"alice"');
    });

    it('sends user code as content', () => {
      expect(fetchMock.lastOptions('/account-recovery').body).toContain('"userCode":"def234"');
    });

    it('sends password as content', () => {
      expect(fetchMock.lastOptions('/account-recovery').body).toContain('"password":"123"');
    });

    it('sends confirm password as content', () => {
      expect(fetchMock.lastOptions('/account-recovery').body).toContain('"confirmPassword":"456"');
    });
  });

  describe('Password validation', () => {
    let newPasswordFormInstance;

    beforeEach(() => {
      newPasswordFormInstance = newPasswordForm.instance();
    });

    it('verifies initial state', () => {
      expect(newPasswordFormInstance.state.errorPassword).toEqual('');
      expect(newPasswordFormInstance.state.errorConfirmPassword).toEqual('');
      expect(newPasswordForm.find('SubmitButton').props().disabled).toBe(true);
    });

    context('with valid fields', () => {
      beforeEach(() => {
        newPasswordFormInstance.validatePassword('12345678', '12345678');
      });

      it('does not set error in state', () => {
        expect(newPasswordFormInstance.state.errorPassword).toEqual('');
        expect(newPasswordFormInstance.state.errorConfirmPassword).toEqual('');
      });

      it('enables submit button', () => {
        expect(newPasswordForm.find('SubmitButton').props().disabled).toBe(false);
      });
    });

    context('with invalid password', () => {
      beforeEach(() => {
        newPasswordFormInstance.validatePassword('1234', '');
      });

      it('sets password error in state', () => {
        expect(newPasswordFormInstance.state.errorPassword).toEqual('account-recovery.new-password-form.error.invalid-password');
      });

      it('disables submit button', () => {
        expect(newPasswordForm.find('SubmitButton').props().disabled).toBe(true);
      });
    });

    context('with invalid confirm password', () => {
      beforeEach(() => {
        newPasswordFormInstance.validatePassword('12345678', '1234');
      });

      it('sets confirm password error in state', () => {
        expect(newPasswordFormInstance.state.errorConfirmPassword).toEqual('account-recovery.new-password-form.error.invalid-confirm-password');
      });

      it('disables submit button', () => {
        expect(newPasswordForm.find('SubmitButton').props().disabled).toBe(true);
      });
    });

    context('with empty fields', () => {
      it('does not set error in state if both empty', () => {
        newPasswordFormInstance.validatePassword('', '');
        expect(newPasswordFormInstance.state.errorPassword).toEqual('');
        expect(newPasswordFormInstance.state.errorConfirmPassword).toEqual('');
      });

      it('does not set confirm password error in state if empty', () => {
        newPasswordFormInstance.validatePassword('12345678', '');
        expect(newPasswordFormInstance.state.errorConfirmPassword).toEqual('');
      });

      it('sets confirm password error in state if not empty', () => {
        newPasswordFormInstance.validatePassword('', '12345678');
        expect(newPasswordFormInstance.state.errorConfirmPassword).toEqual('account-recovery.new-password-form.error.invalid-confirm-password');
      });

      it('disables submit button if empty confirm password', () => {
        newPasswordFormInstance.validatePassword('12345678', '');
        expect(newPasswordForm.find('SubmitButton').props().disabled).toBe(true);
      });

      it('disables submit button if empty password', () => {
        newPasswordFormInstance.validatePassword('', '12345678');
        expect(newPasswordForm.find('SubmitButton').props().disabled).toBe(true);
      });
    });

    it('calls next handler on success', () => {
      expect(mockNext).toHaveBeenCalled();
    });
  });
});
