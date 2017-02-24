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
});
