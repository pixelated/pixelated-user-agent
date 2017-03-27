import { shallow } from 'enzyme';
import expect from 'expect';
import React from 'react';
import { Page } from 'src/account_recovery/page';

describe('Account Recovery Page', () => {
  let page;

  beforeEach(() => {
    const mockTranslations = key => key;
    page = shallow(<Page t={mockTranslations} />);
  });

  it('renders account recovery page title', () => {
    expect(page.props().title).toEqual('account-recovery.page-title');
  });
});
