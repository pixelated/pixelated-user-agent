import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import fetchMock from 'fetch-mock';
import { BackupEmail } from 'src/backup_account/backup_email/backup_email';
import browser from 'helpers/browser';

describe('BackupEmail', () => {
  let backupEmail;
  let mockOnSubmit;
  let mockTranslations;

  beforeEach(() => {
    mockOnSubmit = expect.createSpy();

    mockTranslations = key => key;
    backupEmail = shallow(<BackupEmail t={mockTranslations} onSubmit={mockOnSubmit} />);
  });

  it('renders backup email title', () => {
    expect(backupEmail.find('h1').text()).toEqual('backup-account.backup-email.title');
  });

  it('renders backup account email input field', () => {
    expect(backupEmail.find('InputField').props().name).toEqual('email');
  });

  it('renders backup account submit button', () => {
    expect(backupEmail.find('SubmitButton').props().buttonText).toEqual('backup-account.backup-email.button');
  });

  describe('Email validation', () => {
    let backupEmailInstance;

    beforeEach(() => {
      backupEmailInstance = backupEmail.instance();
    });

    it('verify initial state', () => {
      expect(backupEmailInstance.state.error).toEqual('');
      expect(backupEmail.find('SubmitButton').props().disabled).toBe(true);
    });

    context('with invalid email', () => {
      beforeEach(() => {
        backupEmailInstance.validateEmail({ target: { value: 'test' } });
      });

      it('sets error in state', () => {
        expect(backupEmailInstance.state.error).toEqual('backup-account.backup-email.error.invalid-email');
      });

      it('disables submit button', () => {
        expect(backupEmail.find('SubmitButton').props().disabled).toBe(true);
      });
    });

    context('with valid email', () => {
      beforeEach(() => {
        backupEmailInstance.validateEmail({ target: { value: 'test@test.com' } });
      });

      it('does not set error in state', () => {
        expect(backupEmailInstance.state.error).toEqual('');
      });

      it('submit button is enabled', () => {
        expect(backupEmail.find('SubmitButton').props().disabled).toBe(false);
      });
    });

    context('with empty email', () => {
      beforeEach(() => {
        backupEmailInstance.validateEmail({ target: { value: '' } });
      });

      it('not set error in state', () => {
        expect(backupEmailInstance.state.error).toEqual('');
      });

      it('disables submit button', () => {
        expect(backupEmail.find('SubmitButton').props().disabled).toBe(true);
      });
    });
  });

  describe('Submit', () => {
    let preventDefaultSpy;

    beforeEach(() => {
      preventDefaultSpy = expect.createSpy();
    });

    context('on success', () => {
      beforeEach((done) => {
        mockOnSubmit = expect.createSpy().andCall(() => done());
        expect.spyOn(browser, 'getCookie').andReturn('abc123');

        fetchMock.post('/backup-account', 204);
        backupEmail = shallow(<BackupEmail t={mockTranslations} onSubmit={mockOnSubmit} />);
        backupEmail.find('form').simulate('submit', { preventDefault: preventDefaultSpy });
      });

      it('posts backup email', () => {
        expect(fetchMock.called('/backup-account')).toBe(true, 'Backup account POST was not called');
      });

      it('sends csrftoken as content', () => {
        expect(fetchMock.lastOptions('/backup-account').body).toContain('"csrftoken":["abc123"]');
      });

      it('sends content-type header', () => {
        expect(fetchMock.lastOptions('/backup-account').headers['Content-Type']).toEqual('application/json');
      });

      it('sends same origin headers', () => {
        expect(fetchMock.lastOptions('/backup-account').credentials).toEqual('same-origin');
      });

      it('prevents default call to refresh page', () => {
        expect(preventDefaultSpy).toHaveBeenCalled();
      });

      it('calls onSubmit from props with success', () => {
        expect(mockOnSubmit).toHaveBeenCalledWith('success');
      });
    });

    context('on error', () => {
      beforeEach((done) => {
        mockOnSubmit = expect.createSpy().andCall(() => done());

        fetchMock.post('/backup-account', 500);
        backupEmail = shallow(<BackupEmail t={mockTranslations} onSubmit={mockOnSubmit} />);
        backupEmail.find('form').simulate('submit', { preventDefault: preventDefaultSpy });
      });

      it('calls onSubmit from props with error', () => {
        expect(mockOnSubmit).toHaveBeenCalledWith('error');
      });
    });
  });

  afterEach(() => {
    fetchMock.restore();
  });
});
