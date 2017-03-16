import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Page } from 'src/backup_account/page';
import BackupEmail from 'src/backup_account/backup_email/backup_email';
import Confirmation from 'src/backup_account/confirmation/confirmation';

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
      pageInstance.saveBackupEmail();
      expect(pageInstance.state.status).toEqual('success');
    });

    it('renders backup email component', () => {
      expect(page.find(BackupEmail).length).toEqual(1);
    });

    it('renders confirmation component', () => {
      pageInstance.saveBackupEmail();
      expect(page.find(Confirmation).length).toEqual(1);
    });
  });
});
