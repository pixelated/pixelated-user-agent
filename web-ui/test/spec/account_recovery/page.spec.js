import {shallow} from 'enzyme'
import expect from 'expect'
import React from 'react'
import Page from '../../../app/js/account_recovery/page'

describe('Page', () => {
  'use strict';
  it('renders backup email page title', () => {
    const page = shallow(<Page />);
    expect(page.find('h1').text()).toEqual('E se você esquecer sua senha?');
  });
});
