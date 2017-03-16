import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Confirmation } from 'src/backup_account/confirmation/confirmation';

describe('Confirmation', () => {
  let page;

  beforeEach(() => {
    const mockTranslations = key => key;
    page = shallow(<Confirmation t={mockTranslations} />);
  });

  it('renders confirmation title', () => {
    expect(page.find('h1').text()).toContain('backup-account.confirmation.title1');
  });

  it('renders confirmation submit button', () => {
    expect(page.find('SubmitButton').props().buttonText).toEqual('backup-account.confirmation.button');
  });

  it('renders confirmation retry button', () => {
    expect(page.find('a').text()).toEqual('backup-account.confirmation.retry-button');
  });

  it('retries button redirects to backup account', () => {
    expect(page.find('a').props().href).toEqual('/backup-account');
  });
});
