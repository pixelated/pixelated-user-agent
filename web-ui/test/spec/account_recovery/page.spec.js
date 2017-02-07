import {shallow} from 'enzyme'
import expect from 'expect'
import React from 'react'
import { Page } from '../../../app/js/account_recovery/page'

describe('Page', () => {
  it('renders backup email page title', () => {
    const mockT = key => key;
    const page = shallow(<Page t={mockT}/>);
    expect(page.find('h1').text()).toEqual('backup-account.title');
  });
});
