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

  it('renders backup account page title', () => {
    expect(page.props().title).toEqual('backup-account.page-title');
  });

  describe('save backup email', () => {
    let pageInstance;

    beforeEach(() => {
      pageInstance = page.instance();
    });

    it('verify initial state', () => {
      expect(pageInstance.state.status).toEqual('');
    });

    it('changes state', () => {
      pageInstance.saveBackupEmail();
      expect(pageInstance.state.status).toEqual('success');
    });
  });
});
