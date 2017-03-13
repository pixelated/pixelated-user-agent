import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Page } from 'src/backup_account/page';

describe('BackupAccount', () => {
  let page;

  beforeEach(() => {
    const mockTranslations = key => key;
    page = shallow(<Page t={mockTranslations} />);
  });

  it('renders backup email page title', () => {
    expect(page.find('h1').text()).toEqual('backup-account.title');
  });

  it('renders backup account email input field', () => {
    expect(page.find('InputField').props().name).toEqual('email');
  });

  it('renders backup account submit button', () => {
    expect(page.find('SubmitButton').props().buttonText).toEqual('backup-account.button');
  });

  describe('Email validation', () => {
    let pageInstance;

    beforeEach(() => {
      pageInstance = page.instance();
    });

    it('verify initial state', () => {
      expect(pageInstance.state.error).toEqual('');
      expect(page.find('SubmitButton').props().disabled).toEqual(true);
    });

    context('with invalid email', () => {
      beforeEach(() => {
        pageInstance.validateEmail({ target: { value: 'test' } });
      });

      it('sets error in state', () => {
        expect(pageInstance.state.error).toEqual('backup-account.error.invalid-email');
      });

      it('disables submit button', () => {
        expect(page.find('SubmitButton').props().disabled).toEqual(true);
      });
    });

    context('with valid email', () => {
      beforeEach(() => {
        pageInstance.validateEmail({ target: { value: 'test@test.com' } });
      });

      it('does not set error in state', () => {
        expect(pageInstance.state.error).toEqual('');
      });

      it('submit button is enabled', () => {
        expect(page.find('SubmitButton').props().disabled).toEqual(false);
      });
    });

    context('with empty email', () => {
      beforeEach(() => {
        pageInstance.validateEmail({ target: { value: '' } });
      });

      it('not set error in state', () => {
        expect(pageInstance.state.error).toEqual('');
      });

      it('disables submit button', () => {
        expect(page.find('SubmitButton').props().disabled).toEqual(true);
      });
    });
  });
});
