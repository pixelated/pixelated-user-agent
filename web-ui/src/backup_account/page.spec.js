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

    it('should set error in state and disabled submit button when email is invalid', () => {
      pageInstance.validateEmail({ target: { value: 'test' } });
      expect(pageInstance.state.error).toEqual('Your email is invalid');
      expect(page.find('SubmitButton').props().disabled).toEqual(true);
    });

    it('should not set error in state and submit button is enabled when email is valid', () => {
      pageInstance.validateEmail({ target: { value: 'test@test.com' } });
      expect(pageInstance.state.error).toEqual('');
      expect(page.find('SubmitButton').props().disabled).toEqual(false);
    });

    it('should not set error in state and disable submit button when email is empty', () => {
      pageInstance.validateEmail({ target: { value: '' } });
      expect(pageInstance.state.error).toEqual('');
      expect(page.find('SubmitButton').props().disabled).toEqual(true);
    });
  });
});
