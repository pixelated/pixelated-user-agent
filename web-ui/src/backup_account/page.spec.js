import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Page } from 'src/backup_account/page';
import BackupEmail from 'src/backup_account/backup_email/backup_email';
import Confirmation from 'src/backup_account/confirmation/confirmation';
import SnackbarNotification from 'src/common/snackbar_notification/snackbar_notification';

describe('BackupAccount', () => {
  let page;

  beforeEach(() => {
    const mockTranslations = key => key;
    page = shallow(<Page t={mockTranslations} />);
  });

  it('renders backup account page title', () => {
    expect(page.props().title).toEqual('backup-account.page-title');
  });

  describe('save backup email', () => {
    let pageInstance;

    beforeEach(() => {
      pageInstance = page.instance();
    });

    it('verifies initial state', () => {
      expect(pageInstance.state.status).toEqual('');
    });

    it('changes state', () => {
      pageInstance.saveBackupEmail('success');
      expect(pageInstance.state.status).toEqual('success');
    });

    it('renders backup email component', () => {
      expect(page.find(BackupEmail).length).toEqual(1);
    });

    it('renders confirmation component', () => {
      pageInstance.saveBackupEmail('success');
      expect(page.find(Confirmation).length).toEqual(1);
    });

    context('on submit error', () => {
      beforeEach(() => {
        pageInstance.saveBackupEmail('error');
      });

      it('returns snackbar component on error', () => {
        const snackbar = pageInstance.showSnackbarOnError(pageInstance.props.t);
        expect(snackbar).toEqual(<SnackbarNotification message='backup-account.error.submit-error' isError />);
      });

      it('returns nothing when there is no error', () => {
        pageInstance.saveBackupEmail('success');
        const snackbar = pageInstance.showSnackbarOnError(pageInstance.props.t);
        expect(snackbar).toEqual(undefined);
      });

      it('renders snackbar notification on error', () => {
        const snackbar = page.find(SnackbarNotification);
        expect(snackbar).toExist();
        expect(snackbar.props().message).toEqual('backup-account.error.submit-error');
        expect(snackbar.props().isError).toEqual(true);
      });
    });
  });
});
